import yaml
import glob
import json
import os
import shutil

import subprocess
import sys

from Meta_ForbiddenOptions import ForbiddenOptionNames

# World files per game, as OoTMM's packages/data/build/world.ts loads them for default settings:
# vanilla dungeons (dungeons_mq is the Master Quest variant) and the US Deku Palace (mm/jp is the jpLayouts variant).
WorldSources = {
    "OOT": ["oot/overworld/**/*.yml", "oot/boss/**/*.yml", "oot/dungeons/*.yml"],
    "MM": ["mm/overworld/**/*.yml", "mm/boss/**/*.yml", "mm/dungeons/*.yml", "mm/us/*.yml"],
}

SpawnRegion = "OOT SPAWN"

MacroSources = {
    "common": "macros_common.yml",
    "OOT": "macros_oot.yml",
    "MM": "macros_mm.yml",
}

def LoadYAML(Path):
    with open(Path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file) or {}

def GenerateMetaFiles():
    print("Generating world+macro files from OOTMM data...")

    GreatWorldYAML = {}
    GreatMacroYAML = {}

    # OoT and MM reuse region and location names (shops, GLOBAL, VOID), so every name gets its game
    # as a prefix, the way OoTMM names them internally. An exit that already starts with a game prefix
    # points into the other game.
    for Game, Patterns in WorldSources.items():
        GameWorld = {}
        for Pattern in Patterns:
            for FullPath in sorted(glob.glob(os.path.join("./ootmm/data/world", Pattern), recursive=True)):
                GameWorld.update(LoadYAML(FullPath))
        for Region, RegionData in GameWorld.items():
            if RegionData.get("locations"):
                RegionData["locations"] = {Game + " " + Name: Rule for Name, Rule in RegionData["locations"].items()}
            if RegionData.get("exits"):
                RegionData["exits"] = {
                    (Target if Target.startswith(("OOT ", "MM ")) else Game + " " + Target): Rule
                    for Target, Rule in RegionData["exits"].items()
                }
            GreatWorldYAML[Game + " " + Region] = RegionData

    # Keep only regions some exit chain reaches from OoTMM's spawn. The rest are stubs for the other
    # Deku Palace layout, entrance-randomizer-only sources, or data OoTMM itself never connects.
    Reached = {SpawnRegion}
    Pending = [SpawnRegion]
    while Pending:
        for Target in GreatWorldYAML[Pending.pop()].get("exits") or {}:
            if Target not in Reached:
                Reached.add(Target)
                Pending.append(Target)
    for Region in [Region for Region in GreatWorldYAML if Region not in Reached]:
        print(f"  Dropping unreachable region: {Region}")
        del GreatWorldYAML[Region]

    # Finally, dump the merged YAML structure into a single file
    with open("GreatWorldYMLdump.yaml", 'w') as outfile:
        yaml.dump(GreatWorldYAML, outfile,width=float("inf"))

    # Macros keep their source split (common, OOT, MM), since the same macro name differs per game
    for Section, File in MacroSources.items():
        GreatMacroYAML[Section] = LoadYAML(os.path.join("./ootmm/data/macros", File))

    # Finally, dump the merged YAML structure into a single file
    with open("GreatMacroYMLdump.yaml", 'w') as outfile:
        yaml.dump(GreatMacroYAML, outfile,width=float("inf"))

    # Now, convert both to json (because that's WAY easier to work with)
    # Yes, this is a bit redundant, but it keeps the source data in YAML which is more human readable
    #   and editable, while giving us JSON to work with for the actual code.
    # This takes an extra few cpu cycles, but it's not like this is a performance bottleneck or anything, so who cares.
    with open("GreatWorldYMLdump.yaml", 'r') as file:
        yamldata = yaml.safe_load(file)
        with open("GreatWorldJSONdump.json", 'w') as jsonfile:
            json.dump(yamldata, jsonfile)
    with open("GreatMacroYMLdump.yaml", 'r') as file:
        yamldata = yaml.safe_load(file)
        with open("GreatMacroJSONdump.json", 'w') as jsonfile:
            json.dump(yamldata, jsonfile)


def IsolateRegionData():
    print("Isolating location+entrance data from world files...")
    # As a test of strength, we'll isolate only the needed region data from the world dump.
    # Splitting it into two more files for only the needed data.
    
    IsolatedRegionLocationData = {}
    IsolatedRegionExitData = {}
    
    with open("GreatWorldJSONdump.json", 'r') as file:
        data = json.load(file)
        for region in data.keys():
            for subkey in data[region].keys():
                if subkey == "locations":
                    for sublocation in data[region][subkey].keys():
                        if region not in IsolatedRegionLocationData:
                            IsolatedRegionLocationData[region] = {}
                        IsolatedRegionLocationData[region][sublocation] = data[region][subkey][sublocation]
                if subkey == "exits":
                    for subexit in data[region][subkey].keys():
                        if region not in IsolatedRegionExitData:
                            IsolatedRegionExitData[region] = {}
                        IsolatedRegionExitData[region][subexit] = data[region][subkey][subexit]

    with open("IsolatedRegionLocationData.yaml", 'w') as outfile:
        yaml.dump(IsolatedRegionLocationData, outfile, width=float("inf"))

    with open("IsolatedRegionLocationData.json", 'w') as jsonfile:
        json.dump(IsolatedRegionLocationData, jsonfile)

    with open("IsolatedRegionExitData.yaml", 'w') as outfile:
        yaml.dump(IsolatedRegionExitData, outfile, width=float("inf"))

    with open("IsolatedRegionExitData.json", 'w') as jsonfile:
        json.dump(IsolatedRegionExitData, jsonfile)
        

def GenerateRawOptionsFile():
    print("Generating raw options file from source TypeScript...")
    # Here we invoke node.js to convert the options/setting typescript data into JSON
    
    TypeScriptConverter = r"""
    import fs from 'node:fs';
    import { SETTINGS } from './ootmm/packages/core/src/settings/data.ts';

    function replacer(key, value) {
      if ((key === 'min' || key === 'max') && typeof value === 'function') {
        return value({ mode: 'single' });
      }  
        
      if (typeof value === 'function') {
        return undefined; // Returns functions as undefined
        // return value.toString(); // Returns functions as strings
      }
      return value;
    }

    fs.writeFileSync(
      './GreatSettingsJSONdump.json',
      JSON.stringify(SETTINGS, replacer, 2),
      'utf8'
    );
    """
    
    # npx is a .cmd script on Windows, which needs the shell to launch.
    subprocess.run(
    ["npx", "tsx", "--eval", TypeScriptConverter],
    check=True,
    shell=sys.platform == "win32",
    )
    
def ConvertRawOptions():
    print("Converting raw options JSON to AP/python format...")
    
    # Load in the raw options JSON
    RawOptionsData = json.load(open("GreatSettingsJSONdump.json", 'r'))
    
    # Now, we will convert the raw options data into a python file that can be used by the AP code.
    OptionsFile = []
    ListOfOptions = []
    
    # Write the basic header code directly to the file
    OptionsFile.append("# This file is auto-generated from GenerateMetadata.py. Do not edit directly.")
    OptionsFile.append("")
    OptionsFile.append("from dataclasses import dataclass")
    OptionsFile.append("from Options import OptionGroup, PerGameCommonOptions, Toggle, Choice, Range, OptionSet")
    OptionsFile.append("")
    OptionsFile.append("# Toggle, DefaultOnToggle, Choice, Range, NamedRange")
    OptionsFile.append("# FreeText, TextChoice")
    OptionsFile.append("")
    OptionsFile.append("")

    # Now, we will iterate through the raw options data and convert it into the AP/python format.
    for Option in RawOptionsData:
        # Skip any options that are in the forbidden list
        if Option["key"] in ForbiddenOptionNames:
            continue
        
        # Inilialize the option name and type variables
        OptionName = ""
        OptionType = ""
        
        # Choice / enum
        DescriptionList = []
        ChoiceList = []
        
        # Range / number
        RangeList = {}
        
        # Toggle / boolean
        ToggleList = []
        
        # OptionSet / set
        ValidKeysList = []
        ValidKeyStrings = []
        
        
        # Set the class name based on the category and name of the option. Careful to replace any periods to ensure the class loads properly
        OptionName = "OOTxMM_" + Option["category"].replace(".", "") + "_" + Option["key"]
        
        # Add the OptionName to the list of options for later use
        ListOfOptions.append(OptionName)
        
        # Depending on the type of option, convert this to the appropriate AP/python format.
        if Option["type"] == "enum":
            try:
                OptionType = "Choice"
                for Choice in Option["values"]:
                    # Archipelago reserves "random" on every Choice and rolls it itself.
                    if Choice["value"] == "random":
                        continue
                    if Choice.get("description"):
                        DescriptionList.append("    - **" + Choice["value"] + "**: " + Choice["description"])
                    else:
                        DescriptionList.append("    - **" + Choice["value"] + "**")
                    ChoiceList.append(Choice["value"])
            except Exception as e:
                OptionsFile.append("ERRTYPE: " + str(e))
        elif Option["type"] == "number":
            try:
                OptionType = "Range"
                if Option.get("min"):
                    RangeList["min"] = Option["min"]
                else: 
                    RangeList["min"] = 0
                if Option.get("max"):
                    RangeList["max"] = Option["max"]
                else: 
                    RangeList["max"] = 999
                if Option.get("default"):
                    RangeList["default"] = Option["default"]
                else:
                    RangeList["default"] = 0
            except Exception as e:
                OptionsFile.append("ERRTYPE: " + str(e))
        elif Option["type"] == "boolean":  
            try:
                OptionType = "Toggle"
                ToggleList.append(str(Option["default"]))
            except Exception as e:
                OptionsFile.append("ERRTYPE: " + str(e))
        elif Option["type"] == "set":  
            try:
                OptionType = "OptionSet"
                ValidKeysList = Option["values"]
                for validkey in ValidKeysList:
                    ValidKeyStrings.append(validkey["value"])
                DescriptionList.append("    " + str(ValidKeyStrings))
            except Exception as e:
                OptionsFile.append("ERRTYPE: " + str(e))
        else:
            OptionType = "ERRUNKNOWN"
    
        try:
            OptionsFile.append("class " + OptionName + "(" + OptionType + "):")
            OptionsFile.append("    \"\"\"")
            OptionsFile.append("    " + Option["description"])
            if len(DescriptionList) > 0:
                for Description in DescriptionList:
                    OptionsFile.append(Description)
            OptionsFile.append("    \"\"\"")
            OptionsFile.append("    display_name = \"" + Option["name"] + "\"")
            if len(ChoiceList) > 0:
                for Choice in ChoiceList:
                    OptionsFile.append("    option_"+Choice+" = "+str(ChoiceList.index(Choice)))
                if Option["default"] == "random":
                    OptionsFile.append("    default = \"random\"")
                else:
                    OptionsFile.append("    default = option_" + Option["default"])
            if len(RangeList) > 0:
                OptionsFile.append("    range_start = " + str(RangeList["min"]))
                OptionsFile.append("    range_end = " + str(RangeList["max"]))
                OptionsFile.append("    default = " + str(RangeList["default"]))
            if len(ToggleList) > 0:
                for Toggle in ToggleList:
                    OptionsFile.append("    default = " + Toggle)
            if len(ValidKeysList) > 0:
                OptionsFile.append("    valid_keys = {")
                for ValidKey in ValidKeysList:
                    OptionsFile.append("        \'" + ValidKey["value"] + "\',")
                OptionsFile.append("    }")
                OptionsFile.append("    default = valid_keys.copy()")
            OptionsFile.append("")
            
        except Exception as e:
            OptionsFile.append("ERRWRITE: " + str(e))
            
    # Write the basic footer code directly to the file  
    OptionsFile.append("")
    OptionsFile.append("@dataclass")
    OptionsFile.append("class OOTxMMOptions(PerGameCommonOptions):")
    for Option in ListOfOptions:
        OptionsFile.append("    " + Option + ": " + Option)
    OptionsFile.append("")
    OptionsFile.append("option_groups = []")
    OptionsFile.append("")
    OptionsFile.append("option_presets = {}")
    OptionsFile.append("")
    
    # Finally, write the options file to disk
    with open("GeneratedOptions.py", 'w') as outfile:
        for line in OptionsFile:
            outfile.write(line + "\n")


def main():
    GenerateMetaFiles()
    IsolateRegionData()
    GenerateRawOptionsFile()
    ConvertRawOptions()
    shutil.copyfile("GeneratedOptions.py", "../options.py")

if __name__ == "__main__":
    main()