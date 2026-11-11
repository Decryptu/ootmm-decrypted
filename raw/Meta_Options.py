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
# Each one is offered; test/test_checks.py checks that a runtime handler covers each.

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

# Per-area age switching and clock propagation in logic.py and time_logic.py.
PortedTraversal = ["ageChange"]

PortedShops = ["shopShuffleOot", "shopShuffleMm", "priceOotShops", "priceMmShops"]

# Dungeon placement and removal, ported in prefill.py. Maps can also start in the ROM inventory.
PortedDungeon = ["mapCompassShuffle", "bossKeyShuffleOot", "bossKeyShuffleMm", "smallKeyShuffleOot", "smallKeyShuffleMm", "ganonBossKey", "smallKeyShuffleHideout", "smallKeyShuffleChestGame"]

PortedFairies = ["strayFairyChestShuffle", "strayFairyOtherShuffle"]

PortedSongs = ["songs", "songGoronOot", "sharedSongGoron", "progressiveGoronLullabyOot", "progressiveGoronLullabyMm"]

PortedRewards = ["dungeonRewardShuffle"]

PortedMaps = ["tingleShuffle"]

# Optional vanilla placements from OoTMM's misc/fixer.ts. The normal item pool is unchanged.
PortedFixed = ["shuffleOcarinasOot", "shuffleMasterSword", "shuffleGerudoCard"]

CrossGameSongs = {
    "sharedSongZeldaLullaby": ("songZeldaLullabyMm", "MM_SONG_ZELDA"),
    "sharedSongSarias": ("songSariasMm", "MM_SONG_SARIA"),
    "sharedSongMinuet": ("songMinuetMm", "MM_SONG_TP_FOREST"),
    "sharedSongBolero": ("songBoleroMm", "MM_SONG_TP_FIRE"),
    "sharedSongSerenade": ("songSerenadeMm", "MM_SONG_TP_WATER"),
    "sharedSongRequiem": ("songRequiemMm", "MM_SONG_TP_SPIRIT"),
    "sharedSongNocturne": ("songNocturneMm", "MM_SONG_TP_SHADOW"),
    "sharedSongPrelude": ("songPreludeMm", "MM_SONG_TP_LIGHT"),
    "sharedSongAwakening": ("songAwakeningOot", "OOT_SONG_AWAKENING"),
    "sharedSongZora": ("songZoraOot", "OOT_SONG_ZORA"),
    "sharedSongOrder": ("songOrderOot", "OOT_SONG_ORDER"),
    "sharedSongSun": ("songSunMm", "MM_SONG_SUN"),
    "sharedSongElegy": ("elegyOot", "OOT_SONG_EMPTINESS"),
    "sharedSongHealing": ("songHealingOot", "OOT_SONG_HEALING"),
    "sharedSongSoaring": ("songSoaringOot", "OOT_SONG_SOARING"),
}

CrossGameEquipment = {
    "sharedHammer": ("hammerMm", "MM_HAMMER"),
    "sharedBoomerang": ("boomerangMm", "MM_BOOMERANG"),
}

CrossGameItems = CrossGameSongs | CrossGameEquipment

SharedPoolTransforms = list(CrossGameItems) + ["sharedBows", "sharedBombBags", "sharedMagic",
                        "sharedMagicArrowFire", "sharedMagicArrowIce", "sharedMagicArrowLight",
                        "sharedHookshot", "sharedLens", "sharedSongEpona", "sharedSongStorms", "sharedSongTime",
                        "sharedMaskGoron", "sharedMaskZora", "sharedMaskTruth", "sharedMaskBunny", "sharedMaskKeaton",
                        "sharedWallets"]

PortedPool = SharedPoolTransforms + [enable for enable, _ in CrossGameItems.values()] + ["ocarinaButtonsShuffleOot", "ocarinaButtonsShuffleMm", "sharedOcarinaButtons", "sharedSkeletonKey", "sharedSoulsEnemy", "sharedSoulsNpc", "sharedSoulsAnimal", "sharedSoulsMisc", "soulsEnemyOot", "soulsEnemyMm", "soulsBossOot", "soulsBossMm", "soulsNpcOot", "soulsNpcMm", "soulsAnimalOot", "soulsAnimalMm", "soulsMiscOot", "soulsMiscMm", "skeletonKeyOot", "skeletonKeyMm", "smallKeyRingOot", "smallKeyRingMm"]

Ported = PortedPool + PortedMaps + PortedChecks + PortedGoal + PortedDungeon + PortedFairies + PortedSongs + PortedRewards + PortedFixed + PortedTraversal + PortedShops

# Enum settings offered with only some of their values: the others need what the world doesn't port yet.
# The Triforce goals add Triforce pieces to the pool (makePools in packages/logic/src/world/transform.ts).
OfferedValues = {
    "ganonBossKey": ["removed", "vanilla", "ganon", "anywhere"],
    "dungeonRewardShuffle": ["dungeonBlueWarps", "dungeonsLimited", "dungeons", "anywhere"],
    "songs": ["songLocations", "anywhere"],
    "strayFairyChestShuffle": ["vanilla", "ownDungeon", "anywhere", "starting"],
    "strayFairyOtherShuffle": ["vanilla", "ownDungeon", "anywhere", "starting", "removed"],
    "goal": ["any", "ganon", "majora", "both"],
    "smallKeyShuffleOot": ["ownDungeon", "anywhere", "removed"],
    "smallKeyShuffleMm": ["ownDungeon", "anywhere", "removed"],
    "mapCompassShuffle": ["ownDungeon", "anywhere", "starting", "removed"],
    "bossKeyShuffleOot": ["ownDungeon", "anywhere", "removed"],
    "bossKeyShuffleMm": ["ownDungeon", "anywhere", "removed"],
}
