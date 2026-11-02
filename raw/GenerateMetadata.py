import yaml
import xml.etree.ElementTree as ET
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

# Check files that hold each check's vanilla item, matching WorldSources (no dungeons_mq).
CheckSources = ["oot/overworld/**/*.xml", "oot/boss/**/*.xml", "oot/dungeons/*.xml", "oot/special.xml",
                "mm/overworld/**/*.xml", "mm/boss/**/*.xml", "mm/dungeons/*.xml", "mm/special.xml"]

# Location IDs are part of the multiworld protocol, so they live in a registry that only grows:
# a location keeps its ID across OoTMM releases, a new one gets the next free ID in its game's range,
# and a location OoTMM drops keeps its entry so its ID is never reused.
LocationIDFile = "LocationIDs.json"
LocationIDBase = {"OOT": 100000, "MM": 200000}

# Item IDs work the same way, keyed by OoTMM's item ID (OOT_SWORD): OoT 1001-1999, MM 2001-2999, shared 3001-3999.
ItemIDFile = "ItemIDs.json"
# NOTHING, which has no game prefix, goes in the shared range.
ItemIDBase = {"OOT": 1000, "MM": 2000, "SHARED": 3000}

# Vanilla items the check files name that OoTMM swaps for a real item when it reads them
# (itemByID in packages/logic/src/items/index.ts).
CheckItemAliases = {
    "OOT_FLEXIBLE": "OOT_RUPEE_GREEN", "OOT_RANDOM": "OOT_RUPEE_GREEN",
    "MM_???": "MM_RUPEE_GREEN", "MM_FLEXIBLE": "MM_RUPEE_GREEN", "MM_RANDOM": "MM_RUPEE_GREEN",
    "MM_ARROWS_20": "MM_ARROWS_30",
    "OOT_ICE_TRAP": "OOT_RUPEE_BLUE",
}

def LoadYAML(Path):
    with open(Path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file) or {}

def RunTypeScript(Code):
    # Run from a file, not "tsx --eval": npx is a .cmd script on Windows, which needs the shell to
    # launch, and cmd.exe would cut a multi-line argument and read ">" as a redirect.
    ScriptPath = "_generate.mts"
    with open(ScriptPath, 'w', encoding='utf-8') as file:
        file.write(Code)
    try:
        subprocess.run(["npx", "tsx", ScriptPath], check=True, shell=sys.platform == "win32")
    finally:
        os.remove(ScriptPath)

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


def UpdateLocationIDs():
    print("Updating the location ID registry...")
    with open("GreatWorldJSONdump.json", 'r') as file:
        world = json.load(file)
    LocationIDs = {}
    if os.path.exists(LocationIDFile):
        with open(LocationIDFile, 'r') as file:
            LocationIDs = json.load(file)
    names = sorted({name for regiondata in world.values() for name in (regiondata.get("locations") or {})})
    for name in names:
        if name in LocationIDs:
            continue
        game = name.split(" ", 1)[0]
        base = LocationIDBase[game]
        LocationIDs[name] = max([i for i in LocationIDs.values() if base < i < base + 100000], default=base) + 1
        print(f"  new location {LocationIDs[name]}: {name}")
    if len(set(LocationIDs.values())) != len(LocationIDs):
        raise ValueError(f"{LocationIDFile} has duplicate IDs")
    with open(LocationIDFile, 'w') as file:
        json.dump(dict(sorted(LocationIDs.items(), key=lambda entry: entry[1])), file, indent=1)
        file.write("\n")


def GenerateCheckItemFile():
    # Every check's vanilla item, as OoTMM's packages/data/build/checks.ts reads it: any element with a
    # location and an item. Names get the game prefix unless they already have one (gameId in data/lib/game.ts).
    print("Exporting the vanilla item of every check...")
    def GameID(game, name, sep):
        return name if name.startswith(("OOT" + sep, "MM" + sep, "SHARED" + sep)) else game.upper() + sep + name
    CheckItems = {}
    for pattern in CheckSources:
        for path in sorted(glob.glob(os.path.join("ootmm", "data", "checks", pattern), recursive=True)):
            root = ET.parse(path).getroot()
            game = root.get("game")
            for element in root.iter():
                if element.get("location") is None or element.get("item") is None:
                    continue
                item = element.get("item")
                if item != "NOTHING":
                    item = GameID(game, item, "_")
                CheckItems[GameID(game, element.get("location"), " ")] = CheckItemAliases.get(item, item)
    with open("GreatWorldJSONdump.json", 'r') as file:
        world = json.load(file)
    names = {name for regiondata in world.values() for name in (regiondata.get("locations") or {})}
    missing = sorted(names - CheckItems.keys())
    if missing:
        raise ValueError(f"No vanilla item for {len(missing)} locations: {missing[:10]}")
    with open("GreatCheckItemJSONdump.json", 'w') as file:
        json.dump({name: CheckItems[name] for name in sorted(names)}, file, indent=1)
        file.write("\n")


def GenerateLogicFile():
    # OoTMM's own pipeline parses every condition with default settings: macros are inlined and
    # settings, tricks and the vanilla shop prices and song events are already decided. What is left is
    # written as a node table that logic.py reads. OoTMM tracks time of day per area, which
    # Archipelago's state can't, so time and flag conditions are written as met.
    print("Exporting the world logic...")
    # The world builder imports OoTMM's packages, which need their dependencies and the built data package.
    Shell = sys.platform == "win32"
    subprocess.run(["pnpm", "install", "--filter", "@ootmm/logic...", "--ignore-scripts"], cwd="ootmm", check=True, shell=Shell)
    subprocess.run(["pnpm", "run", "build"], cwd=os.path.join("ootmm", "packages", "data"), check=True, shell=Shell)
    RunTypeScript("""
    import fs from 'node:fs';
    import { Monitor, DEFAULT_SETTINGS } from './ootmm/packages/core/src/index.ts';
    import { worldState } from './ootmm/packages/logic/src/pipeline.ts';
    import { logicPassPrice } from './ootmm/packages/logic/src/price.ts';
    import { logicPassSongEvents } from './ootmm/packages/logic/src/misc/index.ts';
    import { logicPassEntrances } from './ootmm/packages/logic/src/solver/entrances.ts';
    import { logicPassWorld } from './ootmm/packages/logic/src/world/builder.ts';
    import { ItemGroups } from './ootmm/packages/logic/src/items/index.ts';

    // OoTMM's pipeline up to the entrance pass, which links the games (Clock Tower and Mask Shop). The
    // world transform pass in between drops the checks default settings leave out, but this world keeps
    // every check, so the entrance pass runs on the world as built.
    let state: any = await worldState(new Monitor({ onLog: () => {} }), { seed: 'ootxmm', settings: DEFAULT_SETTINGS } as any);
    state = { ...state, ...logicPassWorld(state) };
    for (const pass of [logicPassPrice, logicPassSongEvents, logicPassEntrances] as any[]) {
      state = { ...state, ...pass(state) };
    }
    const world = state.worlds[0];

    const nodes: any[] = [true, false];
    const nodeIds = new Map<string, number>([['true', 0], ['false', 1]]);
    const add = (node: any) => {
      const key = JSON.stringify(node);
      if (!nodeIds.has(key)) { nodeIds.set(key, nodes.length); nodes.push(node); }
      return nodeIds.get(key)!;
    };
    const memo = new Map<number, number>();
    const convert = (e: any): number => {
      if (memo.has(e.id)) return memo.get(e.id)!;
      let id: number;
      switch (e.type) {
      case 'true': case 'time-oot': case 'time-mm': case 'flag-on': case 'flag-off': id = 0; break;
      case 'false': id = 1; break;
      case 'price': id = world.prices[e.slot] <= e.max ? 0 : 1; break;
      case 'song-event-oot': id = world.songEventsOot[e.songId] === e.cmp ? 0 : 1; break;
      case 'song-event-mm': id = world.songEventsMm[e.songId] === e.cmp ? 0 : 1; break;
      case 'age': id = add(['age', e.age === 0 ? 'child' : 'adult']); break;
      case 'item': id = add(['item', e.item.id, e.count]); break;
      case 'renewable': case 'license': id = add(['item', e.item.id, 1]); break;
      case 'event': id = add(['event', e.event]); break;
      case 'masks': id = add(['count_unique', [...ItemGroups.MASKS_REGULAR_VANILLA_MM].map(x => x.id), e.count]); break;
      case 'and': case 'or': {
        const isAnd = e.type === 'and';
        const absorb = isAnd ? 1 : 0, neutral = isAnd ? 0 : 1;
        const children = [...new Set<number>(e.exprs.map(convert))].filter(x => x !== neutral);
        if (children.includes(absorb)) id = absorb;
        else if (children.length === 0) id = neutral;
        else if (children.length === 1) id = children[0];
        else id = add([e.type, children]);
        break;
      }
      default: throw new Error(`Unknown expression type ${e.type}`);
      }
      memo.set(e.id, id);
      return id;
    };
    const mapExprs = (m: any) => Object.fromEntries(Object.entries(m).map(([k, e]) => [k, convert(e)]));
    const areas: any = {};
    for (const [name, area] of Object.entries(world.areas) as any[]) {
      areas[name] = {
        game: area.game,
        age_change: area.ageChange,
        exits: mapExprs(area.exits),
        events: mapExprs(area.events),
        locations: mapExprs(area.locations),
      };
    }
    fs.writeFileSync('GreatLogicJSONdump.json', JSON.stringify({ nodes, areas }) + '\\n');
    """)
    # Exits come from the logic (the entrance pass changes some), but regions and checks come from the
    # world dump, so the logic must have every one of them.
    with open("GreatWorldJSONdump.json", 'r') as file:
        world = json.load(file)
    with open("GreatLogicJSONdump.json", 'r') as file:
        areas = json.load(file)["areas"]
    for region, regiondata in world.items():
        if region not in areas:
            raise ValueError(f"No logic for region {region}")
        missing = set(regiondata.get("locations") or {}) - areas[region]["locations"].keys()
        if missing:
            raise ValueError(f"{region}: no logic for locations {sorted(missing)}")


def GenerateItemFile():
    print("Generating item file from OoTMM item data...")
    # OoTMM's item list (logic/src/items/defs.ts), groups (groups.ts) and display names (generator names.ts).
    TypeScriptConverter = r"""
    import fs from 'node:fs';
    import { Items } from './ootmm/packages/logic/src/items/defs.ts';
    import * as Groups from './ootmm/packages/logic/src/items/groups.ts';
    import { itemName } from './ootmm/packages/generator/lib/combo/names.ts';

    const items = Object.keys(Items).map(id => ({
      id,
      name: itemName(id),
      trap: Groups.TRAPS.has(Items[id]),
      junk: Groups.JUNK.has(Items[id]),
    }));
    fs.writeFileSync('./GreatItemJSONdump.json', JSON.stringify(items, null, 1) + '\n', 'utf8');
    """
    RunTypeScript(TypeScriptConverter)
    with open("GreatItemJSONdump.json", 'r') as file:
        items = json.load(file)
    UniqueItemNames(items)
    with open("GreatItemJSONdump.json", 'w') as file:
        json.dump(items, file, indent=1)
        file.write("\n")


def UniqueItemNames(items):
    # Archipelago needs unique item names; OoTMM reuses some ("Blue Fire" exists for OoT, MM and shared).
    # A reused name gets its game added to the OoT and MM items, leaving the shared one plain;
    # any still reused gets its OoTMM ID added, except the first.
    def Duplicates():
        counts = {}
        for item in items:
            counts[item["name"]] = counts.get(item["name"], 0) + 1
        return {name for name, count in counts.items() if count > 1}
    suffix = {"OOT": " (OoT)", "MM": " (MM)"}
    duplicates = Duplicates()
    for item in items:
        game = item["id"].split("_", 1)[0]
        if item["name"] in duplicates and game in suffix and not item["name"].endswith(suffix[game]):
            item["name"] += suffix[game]
    seen = set()
    for item in sorted(items, key=lambda item: item["id"]):
        if item["name"] in seen:
            item["name"] += f" ({item['id']})"
        seen.add(item["name"])
    if Duplicates():
        raise ValueError(f"Item names still reused: {sorted(Duplicates())}")


def UpdateItemIDs():
    print("Updating the item ID registry...")
    with open("GreatItemJSONdump.json", 'r') as file:
        items = json.load(file)
    ItemIDs = {}
    if os.path.exists(ItemIDFile):
        with open(ItemIDFile, 'r') as file:
            ItemIDs = json.load(file)
    for item in sorted(items, key=lambda item: item["id"]):
        name = item["id"]
        if name in ItemIDs:
            continue
        base = ItemIDBase.get(name.split("_", 1)[0], ItemIDBase["SHARED"])
        ItemIDs[name] = max([i for i in ItemIDs.values() if base < i < base + 1000], default=base) + 1
        print(f"  new item {ItemIDs[name]}: {name}")
    if len(set(ItemIDs.values())) != len(ItemIDs):
        raise ValueError(f"{ItemIDFile} has duplicate IDs")
    with open(ItemIDFile, 'w') as file:
        json.dump(dict(sorted(ItemIDs.items(), key=lambda entry: entry[1])), file, indent=1)
        file.write("\n")


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
    RunTypeScript(TypeScriptConverter)
    
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
    GenerateLogicFile()
    UpdateLocationIDs()
    GenerateCheckItemFile()
    GenerateItemFile()
    UpdateItemIDs()
    IsolateRegionData()
    GenerateRawOptionsFile()
    ConvertRawOptions()
    shutil.copyfile("GeneratedOptions.py", "../options.py")

if __name__ == "__main__":
    main()