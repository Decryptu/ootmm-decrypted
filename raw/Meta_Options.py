# Overrides of what raw/GenerateMetadata.py finds about OoTMM's settings (see "Options" in DEVELOPMENT.md):
# a setting OoTMM's code reads outside conditions is not offered until the world ports its effect.

# Settings the world never offers.

# Meaningless in a multiworld: Archipelago runs the multiworld, writes the spoiler and places the hints.
NotOffered = [
    "games",
    "mode",
    "players",
    "teams",
    "distinctWorlds",
    "triforceSharedMulti",
    "generateSpoilerLog",
    "probabilisticFoolishness",
    "noPlandoHints",
    "noDuplicatePlaythroughHints",
    "extraHintRegions",
    "hintPathDungeons",
    "hintPathBoss",
    "hintPathEndBoss",
    "hintPathEvents",
    "hintImportance",
    # Their "custom" value takes its requirements from specialConds, which is not ported.
    "lacs",
    "rainbowBridge",
    "majoraChild",
]

# Categories whose settings OoTMM reads through computed keys, which the source scan can't see:
# items.mmAgeRequirements (core/src/mm-age-requirements.ts) changes what each age can use in MM.
NotOfferedCategories = [
    "items.mmAgeRequirements",
]

# Settings OoTMM's code reads outside conditions whose effect the world ports (see "Options" in DEVELOPMENT.md).
# Each one is offered; test/test_checks.py checks that logic.py or rules.py handles each.

# Check filters, ported in logic.py. GenerateCheckSamples samples OoTMM's check sets over these.
PortedChecks = [
    # Check filters: which checks exist (filterChecks* and the removals before makePools in run(),
    # packages/logic/src/world/transform.ts), ported in logic.py.
    # pondFishShuffle also adds fish of random weights to the pool, so it is not one of them yet.
    "restoreBrokenActors", "shuffleMaskTrades", "divingGameRupeeShuffle", "shuffleSkulltulaFinalReward",
    # eggShuffle also removes the eggs from the pool, which are the vanilla items of the checks it removes.
    "eggShuffle",
    "shufflePotsOot", "shufflePotsMm", "shuffleCratesOot", "shuffleCratesMm", "shuffleBarrelsMm",
    "shuffleFreeRupeesOot", "shuffleFreeRupeesMm", "shuffleFreeHeartsOot", "shuffleFreeHeartsMm",
    "shuffleHivesOot", "shuffleHivesMm", "shuffleGrassOot", "shuffleGrassMm", "shuffleTFGrassMm",
    "shuffleRocksOot", "shuffleRocksMm", "shuffleTreesOot", "shuffleTreesMm", "shuffleBushOot", "shuffleBushMm",
    "shuffleSoilOot", "shuffleSoilMm",
    "shuffleGossipFairiesOot", "shuffleGossipBigFairiesOot", "shuffleGossipFairiesMm", "shuffleGossipBigFairiesMm",
    "shuffleWonderItemsOot", "shuffleWonderItemsMm", "shuffleButterfliesOot", "shuffleButterfliesMm",
    "shuffleBouldersOot", "shuffleBouldersMm", "shuffleRedBouldersOot", "shuffleRedBouldersMm",
    "shuffleSilverBouldersOot", "shuffleSnowballsMm", "shuffleIciclesOot", "shuffleIciclesMm", "shuffleRedIceOot",
    "fairyFountainFairyShuffleOot", "fairyFountainFairyShuffleMm", "fairySpotShuffleOot",
]

# The completion condition, ported in rules.py.
PortedGoal = ["goal"]

Ported = PortedChecks + PortedGoal

# Enum settings offered with only some of their values: the others need what the world doesn't port yet.
# The Triforce goals add Triforce pieces to the pool (makePools in packages/logic/src/world/transform.ts).
OfferedValues = {
    "goal": ["any", "ganon", "majora", "both"],
}
