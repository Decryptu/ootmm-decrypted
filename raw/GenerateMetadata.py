import yaml
import xml.etree.ElementTree as ET
import glob
import hashlib
import json
import os
import shutil

import subprocess
import sys

import re

from Meta_Options import NotOffered, NotOfferedCategories, OfferedValues, Ported, PortedChecks, PortedFixed, SharedPoolTransforms

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
    # Run from a file, not "tsx --eval": tsx is a .cmd script on Windows, which needs the shell to
    # launch, and cmd.exe would cut a multi-line argument and read ">" as a redirect.
    ScriptPath = "_generate.mts"
    with open(ScriptPath, 'w', encoding='utf-8') as file:
        file.write(Code)
    try:
        tsx = os.path.join("ootmm", "node_modules", ".bin", "tsx.cmd" if sys.platform == "win32" else "tsx")
        subprocess.run([tsx, ScriptPath], check=True, shell=sys.platform == "win32")
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


# OoTMM's lists of checks that run() in packages/logic/src/world/transform.ts removes by name.
CheckLists = {"brokenActors": "BROKEN_ACTORS_CHECKS", "sellMasks": "SELL_MASKS_CHECKS", "mmWaterRocks": "MM_WATER_ROCKS"}

def GenerateCheckInfoFile():
    # What OoTMM's check filters read about each check (see "Options" in DEVELOPMENT.md): its type, its scene
    # and whether that scene is a dungeon, from OoTMM's check data, and the lists it removes checks by name.
    # Also each check's key, and the GIs the goal shows up as, for the client.
    print("Exporting check types...")
    RunTypeScript("""
    import fs from 'node:fs';
    import { CHECKS } from './ootmm/packages/data/lib/checks.ts';
    import { isLocationInDungeon } from './ootmm/packages/logic/src/locations.ts';
    import { GI } from './ootmm/packages/generator/lib/combo/data.ts';
    const checks = Object.fromEntries(CHECKS.map(c => [c.location, [c.type, c.scene, isLocationInDungeon(c.scene)]]));
    const keys = Object.fromEntries(CHECKS.map(c => [c.location, c.key]));
    const goalGi = { OOT_GANON: GI['OOT_TRIFORCE_FULL'].index, MM_MAJORA: GI['MM_MASK_MAJORA'].index };
    fs.writeFileSync('./_checks.json', JSON.stringify({ checks, keys, goalGi }), 'utf8');
    """)
    with open("_checks.json", 'r') as file:
        exported = json.load(file)
    checks = exported["checks"]
    os.remove("_checks.json")
    with open("GreatCheckItemJSONdump.json", 'r') as file:
        names = sorted(json.load(file))
    missing = [name for name in names if name not in checks]
    if missing:
        raise ValueError(f"No check data for {len(missing)} locations: {missing[:10]}")
    with open(os.path.join("ootmm", "packages", "logic", "src", "world", "transform.ts"), 'r', encoding='utf-8') as file:
        transform = file.read()
    # The client reads checks off the game by key (the WAL item packets, "Client" in DEVELOPMENT.md), and the
    # goal off the GIs the game sends itself on beating Ganon (play.c, sendSelfTriforce) and Majora.
    info = {"checks": {name: checks[name] for name in names},
            "keys": {name: exported["keys"][name] for name in names}, "goalGi": exported["goalGi"]}
    for key, const in CheckLists.items():
        match = re.search(rf"const {const} = \[(.*?)\];", transform, re.S)
        if match is None:
            raise ValueError(f"{const} not found in transform.ts")
        info[key] = [json.loads('"' + name.replace("\\'", "'") + '"') for name in re.findall(r"'((?:[^'\\]|\\.)*)'", match.group(1))]
        unknown = [name for name in info[key] if name not in checks]
        if unknown:
            raise ValueError(f"{const} names unknown checks: {unknown}")
    with open("GreatCheckInfoJSONdump.json", 'w') as file:
        json.dump(info, file, indent=1)
        file.write("\n")


def GenerateFillFile():
    # What OoTMM's solver (packages/logic/src/solver/solve.ts) does before its main fill, for its default
    # settings of the item placement settings (see "Placement" in
    # DEVELOPMENT.md): the checks that keep their vanilla item (fixedLocations, from its fixer), the songs and
    # dungeon rewards and the checks they go to (placeSemiShuffled), and each dungeon's checks and the items that
    # stay in it (fixDungeon, DUNGEON_ITEMS). Read from a world with every check filter on, so every check is in.
    print("Exporting OoTMM's pre-fill...")
    with open("GreatSettingsJSONdump.json", 'r') as file:
        types = {s["key"]: s["type"] for s in json.load(file)["settings"]}
    with open("_fill.json", 'w') as file:
        json.dump({key: ("all" if types[key] == "enum" else True) for key in PortedChecks}, file)
    RunTypeScript("""
    import fs from 'node:fs';
    import { Monitor, DEFAULT_SETTINGS } from './ootmm/packages/core/src/index.ts';
    import { worldState } from './ootmm/packages/logic/src/pipeline.ts';
    import { Items, ItemHelpers, ItemGroups, SharedItemGroups } from './ootmm/packages/logic/src/items/index.ts';
    const checkSettings = JSON.parse(fs.readFileSync('_fill.json', 'utf8'));
    const { isLocationChestFairy, isLocationOtherFairy, makeLocation } = await import('./ootmm/packages/logic/src/locations.ts');
    const state: any = await worldState(new Monitor({ onLog: () => {} }), { seed: 'ootxmm', settings: { ...DEFAULT_SETTINGS, ...checkSettings } } as any);
    const world = state.worlds[0];
    const items = Object.values(Items) as any[];
    const fixedKeys = ['shuffleOcarinasOot', 'shuffleMasterSword', 'shuffleGerudoCard'];
    const conditionalFixed: Record<string, string[]> = {};
    const fixedSamples = [];
    for (let mask = 0; mask < (1 << fixedKeys.length); mask++) {
      const toggles = Object.fromEntries(fixedKeys.map((key, i) => [key, !!(mask & (1 << i))]));
      const sample: any = await worldState(new Monitor({ onLog: () => {} }),
        { seed: 'ootxmm', settings: { ...DEFAULT_SETTINGS, ...checkSettings, ...toggles } } as any);
      fixedSamples.push({ settings: { ...checkSettings, ...toggles },
        fixed: [...sample.fixedLocations].map((l: string) => l.split('@')[0]).sort() });
    }
    const allShuffled = new Set(fixedSamples[fixedSamples.length - 1].fixed);
    for (let i = 0; i < fixedKeys.length; i++) {
      conditionalFixed[fixedKeys[i]] = fixedSamples[(fixedSamples.length - 1) ^ (1 << i)].fixed
        .filter((name: string) => !allShuffled.has(name));
      if (!conditionalFixed[fixedKeys[i]].length) throw new Error(`No vanilla placements for ${fixedKeys[i]}`);
    }
    fs.writeFileSync('_fixed_samples.json', JSON.stringify(fixedSamples));
    fs.writeFileSync('_fill.json', JSON.stringify({
      conditionalFixed,
      sharedItems: Object.fromEntries([
        ['sharedSkeletonKey', SharedItemGroups.SKELETON_KEY],
        ['sharedOcarinaButtons', SharedItemGroups.OCARINA_BUTTONS],
        ['sharedSoulsEnemy', SharedItemGroups.SOULS_ENEMY],
        ['sharedSoulsNpc', SharedItemGroups.SOULS_NPC],
        ['sharedSoulsAnimal', SharedItemGroups.SOULS_ANIMAL],
        ['sharedSoulsMisc', SharedItemGroups.SOULS_MISC],
      ].map(([key, defs]: any) => [key, defs.map(d => ({ shared: d.shared.id, oot: d.oot.id, mm: d.mm.id }))])),
      optionalItems: {
        ocarinaButtonsShuffleOot: SharedItemGroups.OCARINA_BUTTONS.map(d => d.oot.id).sort(),
        ocarinaButtonsShuffleMm: SharedItemGroups.OCARINA_BUTTONS.map(d => d.mm.id).sort(),
        soulsEnemyOot: [...ItemGroups.OOT_SOULS_ENEMY].map(i => i.id).sort(),
        soulsEnemyMm: [...ItemGroups.MM_SOULS_ENEMY].map(i => i.id).sort(),
        soulsBossOot: [...ItemGroups.OOT_SOULS_BOSS].map(i => i.id).sort(),
        soulsBossMm: [...ItemGroups.MM_SOULS_BOSS].map(i => i.id).sort(),
        soulsNpcOot: [...ItemGroups.OOT_SOULS_NPC].map(i => i.id).sort(),
        soulsNpcMm: [...ItemGroups.MM_SOULS_NPC].map(i => i.id).sort(),
        soulsAnimalOot: [...ItemGroups.OOT_SOULS_ANIMAL].map(i => i.id).sort(),
        soulsAnimalMm: [...ItemGroups.MM_SOULS_ANIMAL].map(i => i.id).sort(),
        soulsMiscOot: [...ItemGroups.OOT_SOULS_MISC].map(i => i.id).sort(),
        soulsMiscMm: [...ItemGroups.MM_SOULS_MISC].map(i => i.id).sort(),
      },
      fixed: [...state.fixedLocations].map((l: string) => l.split('@')[0]).sort(),
      fairyLocations: {
        strayFairyChestShuffle: [...world.locations].filter(l => isLocationChestFairy(world, makeLocation(l, 0))).sort(),
        strayFairyOtherShuffle: [...world.locations].filter(l => isLocationOtherFairy(world, makeLocation(l, 0))).sort(),
      },
      songLocations: [...world.songLocations].sort(),
      songItems: items.filter(i => ItemHelpers.isSong(i)).map(i => i.id).sort(),
      warpLocations: [...world.warpLocations].sort(),
      rewardItems: items.filter(i => ItemHelpers.isDungeonReward(i)).map(i => i.id).sort(),
      dungeonShuffleItems: {
        smallKeyShuffleHideout: items.filter(i => (ItemHelpers.isSmallKeyHideout(i) || ItemHelpers.isKeyRingHideout(i))).map(i => i.id).sort(),
        smallKeyShuffleChestGame: items.filter(i => (ItemHelpers.isSmallKeyTCG(i) || ItemHelpers.isKeyRingTCG(i))).map(i => i.id).sort(),
        smallKeyShuffleOot: items.filter(i => (ItemHelpers.isSmallKeyRegularOot(i) || ItemHelpers.isKeyRingRegularOot(i))).map(i => i.id).sort(),
        smallKeyShuffleMm: items.filter(i => (ItemHelpers.isSmallKeyRegularMm(i) || ItemHelpers.isKeyRingRegularMm(i))).map(i => i.id).sort(),
        mapCompassShuffle: items.filter(i => ItemHelpers.isMapCompass(i)).map(i => i.id).sort(),
        bossKeyShuffleOot: items.filter(i => ItemHelpers.isRegularBossKeyOot(i)).map(i => i.id).sort(),
        bossKeyShuffleMm: items.filter(i => ItemHelpers.isRegularBossKeyMm(i)).map(i => i.id).sort(),
      },
      dungeons: Object.fromEntries(Object.entries(world.dungeons).map(([k, v]: [string, any]) => [k, [...v].sort()])),
    }), 'utf8');
    """)
    with open("_fill.json", 'r') as file:
        fill = json.load(file)
    os.remove("_fill.json")
    if set(fill["conditionalFixed"]) != set(PortedFixed):
        raise ValueError("Conditional vanilla placements do not match PortedFixed")
    with open("_fixed_samples.json") as file:
        fixed_samples = json.load(file)
    os.remove("_fixed_samples.json")
    for sample in fixed_samples:
        fixed = sample.pop("fixed")
        sample.update(count=len(fixed), sha256=hashlib.sha256("\n".join(fixed).encode()).hexdigest())
    with open("../test/fixed_samples.json", "w") as file:
        json.dump(fixed_samples, file, indent=1)
        file.write("\n")
    with open(os.path.join("ootmm", "packages", "logic", "src", "solver", "solve.ts"), 'r', encoding='utf-8') as file:
        solve = file.read()
    match = re.search(r"const DUNGEON_ITEMS = \{(.*?)\n\};", solve, re.S)
    if match is None:
        raise ValueError("DUNGEON_ITEMS not found in solve.ts")
    fill["dungeonItems"] = {dungeon: re.findall(r"Items\.(\w+)", items)
                            for dungeon, items in re.findall(r"(\w+): \[(.*?)\]", match.group(1), re.S)}
    unknown = set(fill["dungeonItems"]) - set(fill["dungeons"])
    fill["rewardDungeons"] = []
    for game in ("OOT", "MM"):
        rewards = re.search(r"const REWARDS_DUNGEONS_" + game + r" = \[(.*?)\];", solve, re.S)
        if rewards is None:
            raise ValueError(f"REWARDS_DUNGEONS_{game} not found in solve.ts")
        fill["rewardDungeons"].extend(re.findall(r"'([^']+)'", rewards.group(1)))
    unknown |= set(fill["rewardDungeons"]) - set(fill["dungeons"])
    if unknown:
        raise ValueError(f"Solver placement lists name unknown dungeons: {unknown}")
    # Preserve the ordered pool operations, including v33.0's repeated arrow replacement.
    with open(os.path.join("ootmm", "packages", "logic", "src", "world", "transform.ts"), encoding="utf-8") as file:
        transform = file.read()
    fill["poolTransforms"] = {}
    for key in SharedPoolTransforms:
        block = re.search(r"if \(settings\." + key + r"\) \{(.*?)\n    \}", transform, re.S)
        if block is None:
            raise ValueError(f"Missing pool transform: {key}")
        operations = re.findall(r"this\.(replaceItem|removeItem)\(Items\.(\w+),\s*(?:Items\.(\w+)|(\d+))\);", block.group(1))
        if not operations:
            raise ValueError(f"Empty pool transform: {key}")
        fill["poolTransforms"][key] = [[op, source, target if target else int(count)]
                                       for op, source, target, count in operations]
    with open("GreatFillJSONdump.json", 'w') as file:
        json.dump(fill, file, indent=1)
        file.write("\n")

def GenerateEquipmentSamples():
    # Independent pool results from OoTMM's original pipeline, rather than our exported operations.
    RunTypeScript("""
    import fs from 'node:fs';
    import { Monitor, DEFAULT_SETTINGS } from './ootmm/packages/core/src/index.ts';
    import { worldState } from './ootmm/packages/logic/src/pipeline.ts';
    const transforms = JSON.parse(fs.readFileSync('GreatFillJSONdump.json', 'utf8')).poolTransforms;
    const symbols = new Set(Object.values(transforms).flatMap((ops: any) => ops.flatMap(([op, src, dst]: any) =>
      typeof dst === 'string' ? [src, dst] : [src])));
    const samples = [];
    const keys = Object.keys(transforms);
    for (const settings of [{}, ...keys.map(key => ({[key]:true})),
                            Object.fromEntries(keys.map(key => [key,true]))]) {
      const state: any = await worldState(new Monitor({onLog:()=>{}}),
        {seed:'ootxmm', settings:{...DEFAULT_SETTINGS,...settings}} as any);
      samples.push({settings, pool:Object.fromEntries([...state.pool].filter(([i]: any) => symbols.has(i.item.id))
        .map(([i,n]: any) => [i.item.id,n]))});
    }
    fs.writeFileSync('../test/shared_equipment_samples.json', JSON.stringify(samples, null, 1) + '\\n');
    """)


def GenerateCheckSamples():
    # OoTMM's own check set for a few settings of the ported check settings: test/test_checks.py checks that
    # logic.removed_checks leaves the same ones. Hashed, as the lists are long.
    print("Sampling OoTMM's check sets...")
    with open("GreatSettingsJSONdump.json", 'r') as file:
        types = {s["key"]: s["type"] for s in json.load(file)["settings"]}
    samples = [{}] + [{key: (value if types[key] == "enum" else toggle) for key in PortedChecks}
                      for value, toggle in (("all", True), ("overworld", True), ("dungeons", False))]
    with open("_samples.json", 'w') as file:
        json.dump(samples, file)
    RunTypeScript("""
    import fs from 'node:fs';
    import { Monitor, DEFAULT_SETTINGS } from './ootmm/packages/core/src/index.ts';
    import { worldState } from './ootmm/packages/logic/src/pipeline.ts';
    const samples = JSON.parse(fs.readFileSync('_samples.json', 'utf8'));
    const checks = [];
    for (const settings of samples) {
      const state: any = await worldState(new Monitor({ onLog: () => {} }), { seed: 'ootxmm', settings: { ...DEFAULT_SETTINGS, ...settings } } as any);
      checks.push([...state.worlds[0].locations]);
    }
    fs.writeFileSync('_samples.json', JSON.stringify(checks), 'utf8');
    """)
    with open("_samples.json", 'r') as file:
        checks = json.load(file)
    os.remove("_samples.json")
    with open("GreatCheckItemJSONdump.json", 'r') as file:
        names = set(json.load(file))
    with open(os.path.join("..", "test", "check_samples.json"), 'w') as file:
        json.dump([{"settings": settings, "count": len(names & set(found)), "sha256": CheckSetHash(names & set(found))}
                   for settings, found in zip(samples, checks)], file, indent=1)
        file.write("\n")

def CheckSetHash(names):
    # Also in test/test_checks.py.
    return hashlib.sha256("\n".join(sorted(names)).encode("utf-8")).hexdigest()


def GenerateLogicFile():
    # OoTMM's own pipeline parses every condition with default settings: macros are inlined and
    # settings, tricks and the vanilla shop prices and song events are already decided. What is left is
    # written as a node table that logic.py and time_logic.py read, including area time and waiting rules.
    print("Exporting the world logic...")
    # The world builder imports OoTMM's built data package.
    Shell = sys.platform == "win32"
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
    import { MM_TIME_SLICES, OOT_TIME_ALL } from './ootmm/packages/logic/src/expr/data.ts';
    import { ExprParser, exprEvent, exprAnd, exprOr, exprTrue, exprFalse } from './ootmm/packages/logic/src/expr/index.ts';

    // The settings the world offers that conditions read, and every trick, stay symbolic so
    // the world evaluates them per player. The parser resolves them to true or false, so its two methods
    // are wrapped to return a marker event instead, after OoTMM's own checks of the key and value.
    const classes = JSON.parse(fs.readFileSync('SettingsClasses.json', 'utf8'));
    const symbolic = new Set<string>([...classes.logic, ...classes.ported]);
    // The key and value are the identifiers the method reads with expect().
    const P: any = ExprParser.prototype;
    const withIdentifiers = (parse: any, symbol: (ids: string[]) => any) => function (this: any) {
      const ids: string[] = [];
      this.expect = (t: string) => { const v = P.expect.call(this, t); if (t === 'identifier') ids.push(v); return v; };
      try {
        const expr = parse.call(this);
        return expr === undefined ? expr : (symbol(ids) ?? expr);
      } finally {
        delete this.expect;
      }
    };
    const offeredValues: Record<string, string[]> = __OFFERED_VALUES__;
    P.parseExprSetting = withIdentifiers(P.parseExprSetting, ([key, value]) => {
      if (!symbolic.has(key)) return undefined;
      // Excluded enum values cannot occur; discard their branches before exporting expressions.
      if (value && offeredValues[key] && !offeredValues[key].includes(value)) return exprFalse();
      return exprEvent(`@setting ${key} ${value ?? ''}`);
    });
    P.parseExprTrick = withIdentifiers(P.parseExprTrick, ([key]) => exprEvent(`@trick ${key}`));
    // OoTMM only allows "!" and cond() on settings it has already decided. With symbolic settings they
    // apply to markers, so both are parsed here as OoTMM parses them, negating markers (De Morgan on and/or).
    const negate = (e: any): any => {
      if (e === exprTrue()) return exprFalse();
      if (e === exprFalse()) return exprTrue();
      if (e.type === 'event' && e.event.startsWith('@')) return exprEvent(e.event.startsWith('@!') ? '@' + e.event.slice(2) : '@!' + e.event.slice(1));
      if (e.type === 'and') return exprOr(e.exprs.map(negate));
      if (e.type === 'or') return exprAnd(e.exprs.map(negate));
      throw new Error('Expression is not allowed at runtime');
    };
    P.parseExprNot = function (this: any) {
      if (this.accept('!')) {
        const expr = this.parseExprSingle();
        if (expr === undefined) throw this.error('Expected expression');
        return negate(expr);
      }
    };
    P.parseExprCond = function (this: any) {
      if (this.peek('identifier') !== 'cond') return undefined;
      this.accept('identifier');
      this.expect('(');
      const parts = [];
      for (const sep of [',', ',', ')']) {
        const expr = this.parseExpr();
        if (expr === undefined) throw this.error('Expected expression');
        this.expect(sep);
        parts.push(expr);
      }
      const [cond, then, otherwise] = parts;
      return exprOr([exprAnd([cond, then]), exprAnd([negate(cond), otherwise])]);
    };

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
      case 'true': id = 0; break;
      case 'time-oot': id = add(['time-oot', e.flag]); break;
      case 'time-mm': id = add(['time-mm', e.value + e.value2 * 2 ** 32]); break;
      case 'flag-on': case 'flag-off': id = add([e.type, e.flag]); break;
      case 'false': id = 1; break;
      case 'price': id = world.prices[e.slot] <= e.max ? 0 : 1; break;
      case 'song-event-oot': id = world.songEventsOot[e.songId] === e.cmp ? 0 : 1; break;
      case 'song-event-mm': id = world.songEventsMm[e.songId] === e.cmp ? 0 : 1; break;
      case 'age': id = add(['age', e.age === 0 ? 'child' : 'adult']); break;
      case 'item': id = add(['item', e.item.id, e.count]); break;
      case 'renewable': case 'license': id = add(['item', e.item.id, 1]); break;
      case 'event': {
        // Markers: "@setting key value" or "@trick key", "@!" when negated.
        const [marker, key, value] = e.event.replace('@!', '@').split(' ');
        const symbol = marker === '@setting' ? ['setting', key, value || null] : marker === '@trick' ? ['trick', key] : null;
        if (!symbol) id = add(['event', e.event]);
        else id = e.event.startsWith('@!') ? add(['not', add(symbol)]) : add(symbol);
        break;
      }
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
        time: area.time,
        stay: area.stay === null ? null : area.stay.map(convert),
        exits: mapExprs(area.exits),
        events: mapExprs(area.events),
        locations: mapExprs(area.locations),
      };
    }
    fs.writeFileSync('GreatLogicJSONdump.json', JSON.stringify({ nodes, areas, ootTimeAll: OOT_TIME_ALL, mmTimeSlices: MM_TIME_SLICES }) + '\\n');
    """.replace("__OFFERED_VALUES__", json.dumps(OfferedValues)))
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
    # OoTMM's item list (logic/src/items/defs.ts), groups (groups.ts) and display names (generator names.ts),
    # and the GI the game gives each item by (gi() in generator randomizer/util.ts, for OoTMM's defaults of the
    # settings it reads, none of which the world offers; shared items as their OoT version). The client sends
    # received items by GI. Items the game has no GI for (none in the pool) get null.
    TypeScriptConverter = r"""
    import fs from 'node:fs';
    import { Items } from './ootmm/packages/logic/src/items/defs.ts';
    import * as Groups from './ootmm/packages/logic/src/items/groups.ts';
    import { itemName } from './ootmm/packages/generator/lib/combo/names.ts';
    import { gi } from './ootmm/packages/generator/lib/combo/randomizer/util.ts';
    import { DEFAULT_SETTINGS } from './ootmm/packages/core/src/index.ts';

    const giOf = (id: string) => { try { return gi(DEFAULT_SETTINGS, 'oot', Items[id], false); } catch { return null; } };
    const items = Object.keys(Items).map(id => ({
      id,
      name: itemName(id),
      trap: Groups.TRAPS.has(Items[id]),
      junk: Groups.JUNK.has(Items[id]),
      gi: giOf(id),
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
    print("Exporting OoTMM's settings and tricks...")
    RunTypeScript(r"""
    import fs from 'node:fs';
    import { SETTINGS, TRICKS, DEFAULT_SETTINGS } from './ootmm/packages/core/src/index.ts';

    // min and max can be functions of the other settings; take their single-player value.
    const replacer = (key: string, value: any) => {
      if ((key === 'min' || key === 'max') && typeof value === 'function') return value({ mode: 'single' });
      return typeof value === 'function' ? undefined : value;
    };
    const tricks = Object.entries(TRICKS).map(([key, t]) => ({ key, name: t.name, glitch: !!t.glitch }));
    fs.writeFileSync('./GreatSettingsJSONdump.json',
      JSON.stringify({ settings: SETTINGS, tricks, defaults: DEFAULT_SETTINGS }, replacer, 1) + '\n', 'utf8');
    """)

# OoTMM code that reads settings outside conditions: the world must port what a setting does there before
# offering it. expr/builder.ts and expr/parser.ts only evaluate conditions, settings/ defines the settings
# and random-settings.ts only rolls them.
PortSources = ["ootmm/packages/logic/src/**/*.ts", "ootmm/packages/data/build/**/*.ts", "ootmm/packages/core/src/**/*.ts"]
PortSourcesSkipped = ["logic/src/expr/builder.ts", "logic/src/expr/parser.ts", "core/src/settings/", "core/src/random-settings.ts"]

def ClassifySettings():
    # Each setting is offered or not by what OoTMM does with it:
    # - ported: read by OoTMM's code outside conditions, and the world does what that code does
    #   (Ported in Meta_Options.py). Offered, and symbolic in the logic dump.
    # - port: read by OoTMM's code outside conditions (pool, checks, world shape). Not offered until ported.
    # - logic: read only by conditions (setting(...) in data/). Offered, and symbolic in the logic dump.
    # - patch: read by neither, only by the ROM patcher. Offered and passed through.
    print("Classifying OoTMM's settings...")
    with open("GreatSettingsJSONdump.json", 'r') as file:
        settings = json.load(file)["settings"]
    code = ""
    for pattern in PortSources:
        for path in sorted(glob.glob(pattern, recursive=True)):
            if not any(skip in path.replace("\\", "/") for skip in PortSourcesSkipped):
                with open(path, 'r', encoding='utf-8') as file:
                    code += file.read()
    conditions = ""
    for path in sorted(glob.glob("ootmm/data/**/*.yml", recursive=True)):
        with open(path, 'r', encoding='utf-8') as file:
            conditions += file.read()
    classes = {"logic": [], "ported": [], "patch": [], "port": [], "not_offered": []}
    for setting in settings:
        key = setting["key"]
        if key in NotOffered or setting["category"] in NotOfferedCategories:
            kind = "not_offered"
        elif key in Ported:
            kind = "ported"
        elif re.search(rf"\b{key}\b", code):
            kind = "port"
        elif re.search(rf"\bsetting\(\s*{key}\b", conditions):
            kind = "logic"
        else:
            kind = "patch"
        classes[kind].append(key)
    print("  " + ", ".join(f"{kind}: {len(keys)}" for kind, keys in classes.items()))
    with open("SettingsClasses.json", 'w') as file:
        json.dump(classes, file, indent=1)
        file.write("\n")

def Docstring(lines):
    text = "\n".join(lines).replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return ['    """', *("    " + line if line else "" for line in text.split("\n")), '    """']

def ConvertRawOptions():
    # Offered settings become options named by their OoTMM key, so the world can hand them to the patch
    # as they are (OOTMM_SETTINGS). The tricks are one option set.
    print("Converting the offered settings to options...")
    with open("GreatSettingsJSONdump.json", 'r') as file:
        dump = json.load(file)
    with open("SettingsClasses.json", 'r') as file:
        classes = json.load(file)
    offered = set(classes["logic"]) | set(classes["ported"]) | set(classes["patch"])
    lines = [
        "# Generated by raw/GenerateMetadata.py from OoTMM's settings. Do not edit by hand.",
        "",
        "from dataclasses import dataclass",
        "from Options import OptionGroup, PerGameCommonOptions, Toggle, DefaultOnToggle, Choice, Range, OptionSet",
        "",
        "",
    ]
    fields = []
    groups: dict[str, list[str]] = {}
    for setting in dump["settings"]:
        key = setting["key"]
        if key not in offered:
            continue
        cls = f"OOTxMM_{key}"
        doc = [setting.get("description") or setting["name"]]
        body = [f"    display_name = {json.dumps(setting['name'])}"]
        if setting["type"] == "enum":
            # Archipelago reserves "random" on every Choice and rolls it itself.
            values = [v for v in setting["values"] if v["value"] != "random"
                      and v["value"] in OfferedValues.get(key, [v["value"]])]
            doc += [f"- **{v['value']}**: {v['description']}" if v.get("description") else f"- **{v['value']}**" for v in values]
            body += [f"    option_{v['value']} = {i}" for i, v in enumerate(values)]
            # Archipelago lowercases option names; OoTMM's values keep their case.
            body.append(f"    ootmm_values = {[v['value'] for v in values]!r}")
            body.append('    default = "random"' if setting["default"] == "random" else f"    default = option_{setting['default']}")
            base = "Choice"
        elif setting["type"] == "number":
            body += [f"    range_start = {setting.get('min', 0)}", f"    range_end = {setting.get('max', 999)}", f"    default = {setting['default']}"]
            base = "Range"
        elif setting["type"] == "boolean":
            base = "DefaultOnToggle" if setting["default"] else "Toggle"
        elif setting["type"] == "set":
            values = [v["value"] for v in setting["values"]]
            doc.append("Values: " + ", ".join(values))
            default = setting["default"]
            if isinstance(default, str):
                default = values if default == "all" else []
            elif isinstance(default, dict):
                # A set default is {type: all, none or specific, values}.
                default = values if default.get("type") == "all" else default.get("values", [])
            body += [f"    valid_keys = {values!r}", f"    default = frozenset({sorted(default)!r})"]
            base = "OptionSet"
        else:
            raise ValueError(f"Setting {key}: unknown type {setting['type']}")
        lines += [f"class {cls}({base}):", *Docstring(doc), *body, "", ""]
        fields.append((key, cls))
        groups.setdefault(setting["category"], []).append(cls)
    tricks = dump["tricks"]
    doc = ["Tricks the logic may expect."] + [f"- **{t['key']}**: {t['name']}{' (glitch)' if t['glitch'] else ''}" for t in tricks]
    lines += ["class OOTxMM_tricks(OptionSet):", *Docstring(doc),
              '    display_name = "Tricks"',
              f"    valid_keys = {[t['key'] for t in tricks]!r}",
              f"    default = frozenset({sorted(dump['defaults']['tricks'])!r})", "", ""]
    fields.append(("tricks", "OOTxMM_tricks"))
    groups.setdefault("logic.tricks", []).append("OOTxMM_tricks")
    lines += ["@dataclass", "class OOTxMMOptions(PerGameCommonOptions):"]
    lines += [f"    {key}: {cls}" for key, cls in fields]
    lines += ["", "", "# The OoTMM setting keys of the options above: the patch takes their values as they are.",
              f"OOTMM_SETTINGS = {[key for key, _ in fields]!r}", "",
              "# The ones OoTMM's code reads outside conditions, which the world ports (raw/Meta_Options.py).",
              f"PORTED_SETTINGS = {[key for key, _ in fields if key in classes['ported']]!r}", "",
              "# By OoTMM's setting category.", "option_groups = ["]
    # Categories are keys like "cutscenes.bosses.oot": shown as "Cutscenes / Bosses / Oot".
    lines += [f"    OptionGroup({json.dumps(' / '.join(part[:1].upper() + part[1:] for part in category.split('.')))}, [{', '.join(members)}]),"
              for category, members in groups.items()]
    lines += ["]", "", "option_presets = {}", ""]
    with open("GeneratedOptions.py", 'w', encoding='utf-8') as outfile:
        outfile.write("\n".join(lines))


def GenerateTimeSamples():
    # Independent expected area clocks from OoTMM's own pathfinder, without the symbolic parser wrappers.
    print("Sampling OoTMM's area clocks...")
    RunTypeScript("""
    import fs from 'node:fs';
    import { Monitor, DEFAULT_SETTINGS } from './ootmm/packages/core/src/index.ts';
    import { worldState } from './ootmm/packages/logic/src/pipeline.ts';
    import { logicPassWorld } from './ootmm/packages/logic/src/world/builder.ts';
    import { logicPassPrice } from './ootmm/packages/logic/src/price.ts';
    import { logicPassSongEvents } from './ootmm/packages/logic/src/misc/index.ts';
    import { logicPassEntrances } from './ootmm/packages/logic/src/solver/entrances.ts';
    import { Pathfinder } from './ootmm/packages/logic/src/pathfind/pathfind.ts';
    import { Items, makePlayerItem } from './ootmm/packages/logic/src/items/index.ts';
    let state: any = await worldState(new Monitor({ onLog: () => {} }), { seed: 'ootxmm', settings: DEFAULT_SETTINGS } as any);
    for (const pass of [logicPassWorld, logicPassPrice, logicPassSongEvents, logicPassEntrances] as any[]) {
      state = { ...state, ...pass(state) };
    }
    const checks = JSON.parse(fs.readFileSync('GreatCheckItemJSONdump.json', 'utf8'));
    const symbols = [...new Set([...Object.values(checks), 'OOT_MASK_SKULL', 'OOT_MASK_SPOOKY', 'OOT_MASK_GERUDO',
      'OOT_MASK_KEATON', 'OOT_MASK_TRUTH', 'OOT_MASK_BUNNY', 'OOT_MASK_GORON', 'OOT_MASK_ZORA', 'MM_MASK_DEKU', 'MM_SWORD'])] as string[];
    const samples = [];
    for (const removed of [[], ['MM_OCARINA'], ['MM_SONG_TIME'], ['OOT_OCARINA', 'MM_OCARINA']]) {
      const counts = Object.fromEntries(symbols.filter(s => !removed.includes(s)).map(s => [s, 100]));
      const items = new Map(Object.entries(counts).map(([s, n]) => [makePlayerItem(Items[s as keyof typeof Items], 0), n]));
      const result = new Pathfinder(state.worlds, DEFAULT_SETTINGS, items).run(null, { recursive: true });
      const ws = result.ws[0];
      samples.push({ removed, counts, events: [...ws.events].sort(), areas: ws.ages.map(age =>
        Object.fromEntries([...age.areas].map(([name, data]) => [name, [data.ootTime, data.mmTime + data.mmTime2 * 2 ** 32, data.flagsOn, data.flagsOff]]))) });
    }
    fs.writeFileSync('../test/time_samples.json', JSON.stringify(samples) + '\\n');
    """)


def main():
    # Install before the first TypeScript export, including on a fresh OoTMM checkout.
    subprocess.run(["pnpm", "install", "--filter", "@ootmm/logic...", "--filter", "@ootmm/generator...", "--ignore-scripts"],
                   cwd="ootmm", check=True, shell=sys.platform == "win32")
    GenerateMetaFiles()
    GenerateRawOptionsFile()
    ClassifySettings()
    GenerateLogicFile()
    UpdateLocationIDs()
    GenerateCheckItemFile()
    GenerateCheckInfoFile()
    GenerateFillFile()
    GenerateEquipmentSamples()
    GenerateCheckSamples()
    GenerateTimeSamples()
    GenerateItemFile()
    UpdateItemIDs()
    IsolateRegionData()
    ConvertRawOptions()
    shutil.copyfile("GeneratedOptions.py", "../options.py")

if __name__ == "__main__":
    main()
