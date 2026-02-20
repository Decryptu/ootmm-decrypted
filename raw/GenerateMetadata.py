import yaml
import json
import os

def GenerateMetaFiles():
    # Source dumps of location and macro data
    SourceWorld = "./src/world"
    SourceMacro = "./src/macros"

    GreatWorldYAML = {}
    GreatMacroYAML = {}

    # Generate a single merged yaml with all the source world data
    for DirPath, DirName, FileName in os.walk(SourceWorld):
        for File in FileName:
            FullPath = os.path.join(DirPath, File)
            with open(FullPath, 'r') as file:
                print(f"Dumping world {FullPath}...")
                yamldata = yaml.safe_load(file)
                GreatWorldYAML.update(yamldata)

    # Finally, dump the merged YAML structure into a single file
    with open("GreatWorldYMLdump.yaml", 'w') as outfile:
        yaml.dump(GreatWorldYAML, outfile,width=float("inf"))

    # Generate a single merged yaml with all the source macro data
    for DirPath, DirName, FileName in os.walk(SourceMacro):
        for File in FileName:
            FullPath = os.path.join(DirPath, File)
            with open(FullPath, 'r') as file:
                print(f"Dumping macro {FullPath}...")
                yamldata = yaml.safe_load(file)
                GreatMacroYAML.update(yamldata)

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

GenerateMetaFiles()