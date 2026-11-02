# This file is auto-generated from GenerateMetadata.py. Do not edit directly.

from dataclasses import dataclass
from Options import OptionGroup, PerGameCommonOptions, Toggle, Choice, Range, OptionSet

# Toggle, DefaultOnToggle, Choice, Range, NamedRange
# FreeText, TextChoice


class OOTxMM_main_goal(Choice):
    """
    The objective of the seed. The game will end when the specified goal is reached.
    - **any**: You can beat either Ganon or Majora.
    - **ganon**: You must beat Ganon.
    - **majora**: You must beat Majora.
    - **both**: You must beat Ganon AND Majora. You can do so in any order.
    - **triforce**: You must collect Triforce Pieces to win.
    - **triforce3**: You must collect the three parts of the Triforce (Power, Courage and Wisdom) to win. Specific hints will guide you.
    """
    display_name = "Goal"
    option_any = 0
    option_ganon = 1
    option_majora = 2
    option_both = 3
    option_triforce = 4
    option_triforce3 = 5
    default = option_both

class OOTxMM_main_triforceGoal(Range):
    """
    The amount of Triforce Pieces that are required to win.
    """
    display_name = "Triforce Goal"
    range_start = 1
    range_end = 999
    default = 20

class OOTxMM_main_triforcePieces(Range):
    """
    The total amount of Triforce Pieces in the item pool.
    """
    display_name = "Triforce Pieces"
    range_start = 1
    range_end = 999
    default = 30

class OOTxMM_main_logic(Choice):
    """
    The guarantees you have regarding reachability of locations.
    - **allLocations**: Every location in the game can be reached. The seed can always be completed.
    - **beatable**: Some items can be placed in locations that are never reachable. The seed can always be completed.
    - **none**: Items are placed completely at random. The seed might be unbeatable.
    """
    display_name = "Logic"
    option_allLocations = 0
    option_beatable = 1
    option_none = 2
    default = option_allLocations

class OOTxMM_main_itemPool(Choice):
    """
    Change the item pool.
    - **plentiful**: One extra copy of every major item. Heart containers only.
    - **normal**: The regular item count for each game.
    - **scarce**: One less of every major item. No Heart Pieces.
    - **minimal**: Only one of each major item. No Heart Pieces or Containers.
    - **barren**: Minimal item pool, plus every shuffled item that is not strictly required to reach the goal (beatable only) or any location (all locations) gets removed.
    """
    display_name = "Item Pool"
    option_plentiful = 0
    option_normal = 1
    option_scarce = 2
    option_minimal = 3
    option_barren = 4
    default = option_normal

class OOTxMM_hints_probabilisticFoolish(Toggle):
    """
    Adds extra calculations during the generation of the seed to refine Foolish Hints and Hint Importance, making them more useful. It is strongly recommended to leave this option enabled.
    """
    display_name = "Probabilistic Foolish Hints"
    default = True

class OOTxMM_mainshuffle_songs(Choice):
    """
    Controls where songs can be obtained, in both games.
    - **songLocations**: Only locations that contain songs in the vanilla games will have songs.
    - **anywhere**: Songs can be placed anywhere.
    - **notes**: Songs are split into individual notes, which are then placed anywhere.
    """
    display_name = "Song Shuffle"
    option_songLocations = 0
    option_anywhere = 1
    option_notes = 2
    default = option_songLocations

class OOTxMM_mainshuffle_goldSkulltulaTokens(Choice):
    """
    Controls how Gold Skulltulas will be shuffled
    - **none**: All Gold Skulltula Tokens will be vanilla
    - **dungeons**: Only the Gold Skulltulas within dungeons will be shuffled
    - **overworld**: Only the Gold Skulltulas outside of dungeons will be shuffled
    - **all**: Every single Gold Skulltula will be shuffled
    """
    display_name = "Gold Skulltula Tokens Shuffle"
    option_none = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3
    default = option_none

class OOTxMM_mainshuffle_housesSkulltulaTokens(Choice):
    """
    Controls how Swamp and Ocean Skulltulas will be shuffled
    - **none**: Swamp and Ocean Tokens will be vanilla
    - **all**: Swamp and Ocean Tokens can be found anywhere
    """
    display_name = "House Skulltula Tokens Shuffle"
    option_none = 0
    option_all = 1
    default = option_none

class OOTxMM_mainshuffle_tingleShuffle(Choice):
    """
    Controls where Tingle Maps are
    - **vanilla**: Tingle Maps can be bought at Tingle, in their original locations
    - **anywhere**: Tingle Maps will be anywhere
    - **starting**: Tingle Maps are in Link's pocket
    - **removed**: Tingle Maps are fully removed and cannot be obtained
    """
    display_name = "Tingle Maps Shuffle"
    option_vanilla = 0
    option_anywhere = 1
    option_starting = 2
    option_removed = 3
    default = option_vanilla

class OOTxMM_mainshuffle_mapCompassShuffle(Choice):
    """
    Controls where Maps and Compasses can be
    - **ownDungeon**: Maps and Compasses will be in their own dungeons
    - **anywhere**: Maps and Compasses can be on any location
    - **starting**: Maps and Compasses will be in Link's Pocket
    - **removed**: Fully removed and cannot be obtained
    """
    display_name = "Map / Compass Shuffle"
    option_ownDungeon = 0
    option_anywhere = 1
    option_starting = 2
    option_removed = 3
    default = option_ownDungeon

class OOTxMM_mainshuffle_smallKeyShuffleOot(Choice):
    """
    Controls where Small Keys (for Dungeons) can be in OoT
    - **ownDungeon**: Dungeon Small Keys can only be found in their own dungeons
    - **anywhere**: Dungeon Small Keys can be found anywhere
    - **removed**: Small Keys are removed and Small Key doors are unlocked
    - **vanilla**: Dungeon Small Keys are placed in their original chests
    """
    display_name = "Small Key Shuffle (OoT)"
    option_ownDungeon = 0
    option_anywhere = 1
    option_removed = 2
    option_vanilla = 3
    default = option_ownDungeon

class OOTxMM_mainshuffle_smallKeyShuffleMm(Choice):
    """
    Controls where Small Keys (for Dungeons) can be in MM
    - **ownDungeon**: Dungeon Small Keys can only be found in their own dungeons
    - **anywhere**: Dungeon Small Keys can be found anywhere
    - **removed**: Small Keys are removed and Small Key doors are unlocked
    - **vanilla**: Dungeon Small Keys are placed in their original chests
    """
    display_name = "Small Key Shuffle (MM)"
    option_ownDungeon = 0
    option_anywhere = 1
    option_removed = 2
    option_vanilla = 3
    default = option_ownDungeon

class OOTxMM_mainshuffle_smallKeyShuffleHideout(Choice):
    """
    Controls where Hideout (Gerudo Fortress) Small Keys can be
    - **vanilla**: Hideout Small Keys are always on the guards
    - **ownDungeon**: Hideout Small Keys can only be found within Gerudo Fortress INTERIOR
    - **anywhere**: Hideout Small Keys can be found anywhere
    """
    display_name = "Hideout Small Key Shuffle"
    option_vanilla = 0
    option_ownDungeon = 1
    option_anywhere = 2
    default = option_ownDungeon

class OOTxMM_mainshuffle_smallKeyShuffleChestGame(Choice):
    """
    Controls where Chest Game Small Keys can be
    - **vanilla**: Chest Minigame will behave as in vanilla
    - **ownDungeon**: Chest Minigame Keys can be found inside the minigame
    - **anywhere**: Chest Minigame Keys can be found anywhere
    """
    display_name = "Chest Game Small Key Shuffle"
    option_vanilla = 0
    option_ownDungeon = 1
    option_anywhere = 2
    default = option_vanilla

class OOTxMM_mainshuffle_bossKeyShuffleOot(Choice):
    """
    Controls where Boss Keys can be in OoT
    - **ownDungeon**: Boss Keys can only be in their own dungeons
    - **anywhere**: Boss Keys can be found anywhere
    - **removed**: Boss Keys are removed and boss doors are unlocked
    - **vanilla**: Boss Keys are placed in their original chest
    """
    display_name = "Boss Key Shuffle (OoT)"
    option_ownDungeon = 0
    option_anywhere = 1
    option_removed = 2
    option_vanilla = 3
    default = option_ownDungeon

class OOTxMM_mainshuffle_bossKeyShuffleMm(Choice):
    """
    Controls where Boss Keys can be in MM
    - **ownDungeon**: Boss Keys can only be in their own dungeons
    - **anywhere**: Boss Keys can be found anywhere
    - **removed**: Boss Keys are removed and boss doors are unlocked
    - **vanilla**: Boss Keys are placed in their original chest
    """
    display_name = "Boss Key Shuffle (MM)"
    option_ownDungeon = 0
    option_anywhere = 1
    option_removed = 2
    option_vanilla = 3
    default = option_ownDungeon

class OOTxMM_mainshuffle_smallKeyRingOot(OptionSet):
    """
    Controls the grouping of keys into key rings, for OoT
    ['Forest', 'Fire', 'Water', 'Shadow', 'Spirit', 'BotW', 'GTG', 'Ganon', 'GF', 'TCG']
    """
    display_name = "Small Key Ring (OoT)"
    valid_keys = {
        'Forest',
        'Fire',
        'Water',
        'Shadow',
        'Spirit',
        'BotW',
        'GTG',
        'Ganon',
        'GF',
        'TCG',
    }
    default = valid_keys.copy()

class OOTxMM_mainshuffle_smallKeyRingMm(OptionSet):
    """
    Controls the grouping of keys into key rings, for MM
    ['WF', 'SH', 'GB', 'ST']
    """
    display_name = "Small Key Ring (MM)"
    valid_keys = {
        'WF',
        'SH',
        'GB',
        'ST',
    }
    default = valid_keys.copy()

class OOTxMM_mainshuffle_silverRupeeShuffle(Choice):
    """
    Make silver rupees items that can be shuffled.
    - **vanilla**: Silver Rupees are vanilla
    - **ownDungeon**: Silver Rupees are found within their own dungeon
    - **anywhere**: Silver Rupees are shuffled in the item pool
    """
    display_name = "Silver Rupee Shuffle"
    option_vanilla = 0
    option_ownDungeon = 1
    option_anywhere = 2
    default = option_vanilla

class OOTxMM_mainshuffle_silverRupeePouches(OptionSet):
    """
    Controls grouping of silver rupees into a single item.
    ['DC', 'BotW', 'Spirit_Child', 'Spirit_Sun', 'Spirit_Boulders', 'Spirit_Lobby', 'Spirit_Adult', 'Shadow_Scythe', 'Shadow_Pit', 'Shadow_Spikes', 'Shadow_Blades', 'IC_Scythe', 'IC_Block', 'GTG_Slopes', 'GTG_Lava', 'GTG_Water', 'Ganon_Light', 'Ganon_Forest', 'Ganon_Fire', 'Ganon_Water', 'Ganon_Shadow', 'Ganon_Spirit']
    """
    display_name = "Silver Rupee Pouches"
    valid_keys = {
        'DC',
        'BotW',
        'Spirit_Child',
        'Spirit_Sun',
        'Spirit_Boulders',
        'Spirit_Lobby',
        'Spirit_Adult',
        'Shadow_Scythe',
        'Shadow_Pit',
        'Shadow_Spikes',
        'Shadow_Blades',
        'IC_Scythe',
        'IC_Block',
        'GTG_Slopes',
        'GTG_Lava',
        'GTG_Water',
        'Ganon_Light',
        'Ganon_Forest',
        'Ganon_Fire',
        'Ganon_Water',
        'Ganon_Shadow',
        'Ganon_Spirit',
    }
    default = valid_keys.copy()

class OOTxMM_mainshuffle_townFairyShuffle(Choice):
    """
    Controls where the Clock Town Stray Fairy can be
    - **vanilla**: The Clock Town Stray Fairy will be at its original location
    - **anywhere**: The Clock Town Stray Fairy can be found anywhere
    """
    display_name = "Town Stray Fairy Shuffle"
    option_vanilla = 0
    option_anywhere = 1
    default = option_vanilla

class OOTxMM_mainshuffle_strayFairyChestShuffle(Choice):
    """
    Controls where the Dungeon Chest Stray Fairies can be
    - **starting**: Start with the fairies
    - **vanilla**: The Dungeon Chest Stray Fairies will be at their original locations
    - **ownDungeon**: All Dungeon Chest Stray Fairies are shuffled within their own dungeon
    - **anywhere**: All Dungeon Chest Stray Fairies are shuffled anywhere
    """
    display_name = "Dungeon Chest Fairy Shuffle"
    option_starting = 0
    option_vanilla = 1
    option_ownDungeon = 2
    option_anywhere = 3
    default = option_ownDungeon

class OOTxMM_mainshuffle_strayFairyOtherShuffle(Choice):
    """
    Controls where the Dungeon Freestanding Stray Fairies can be
    - **removed**: Start with the fairies, and the bubbles are removed.
    - **starting**: Start with the fairies
    - **vanilla**: The Dungeon Freestanding Stray Fairies will be at their original locations
    - **ownDungeon**: All Dungeon Freestanding Stray Fairies are shuffled within their own dungeon
    - **anywhere**: All Dungeon Freestanding Stray Fairies are shuffled anywhere
    """
    display_name = "Dungeon Freestanding Fairy Shuffle"
    option_removed = 0
    option_starting = 1
    option_vanilla = 2
    option_ownDungeon = 3
    option_anywhere = 4
    default = option_vanilla

class OOTxMM_mainshuffle_ganonBossKey(Choice):
    """
    Controls where Ganon Boss Key should be
    - **removed**: Ganon Boss Key is removed, and so is the lock on the door leading to Ganondorf
    - **vanilla**: Ganon Boss Key will be in its original chest, within Ganon's Castle
    - **ganon**: Ganon Boss Key will be anywhere within Ganon's Castle
    - **anywhere**: Ganon Boss Key can be found anywhere
    - **custom**
    """
    display_name = "Ganon Boss Key Shuffle"
    option_removed = 0
    option_vanilla = 1
    option_ganon = 2
    option_anywhere = 3
    option_custom = 4
    default = option_removed

class OOTxMM_mainshuffle_dungeonRewardShuffle(Choice):
    """
    Controls where the dungeons rewards should be
    - **dungeonBlueWarps**: Only the blue warps will grant the rewards
    - **dungeonsLimited**: Anywhere in dungeons (one max)
    - **dungeons**: Anywhere in dungeons
    - **anywhere**: Can be anywhere
    """
    display_name = "Dungeon Reward Shuffle"
    option_dungeonBlueWarps = 0
    option_dungeonsLimited = 1
    option_dungeons = 2
    option_anywhere = 3
    default = option_dungeonBlueWarps

class OOTxMM_mainshuffle_scrubShuffleOot(Toggle):
    """
    Controls whether or not Business Scrubs are shuffled (OoT).<br>If disabled, the one in Hyrule Field by Lake Hylia's fences, the one by the Bridge in Lost Woods, and the front one in the grotto near Sacred Forest Meadow will still be shuffled
    """
    display_name = "Scrub Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_scrubShuffleMm(Toggle):
    """
    Controls whether or not Business Scrubs are shuffled (MM).<br>If disabled, the one in Termina Field near the Observatory and the one in Goron Village will still be shuffled
    """
    display_name = "Scrub Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_cowShuffleOot(Toggle):
    """
    Controls whether or not playing Epona's Song near cows will give an item (OoT)
    """
    display_name = "Cow Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_cowShuffleMm(Toggle):
    """
    Controls whether or not playing Epona's Song near cows will give an item (MM)
    """
    display_name = "Cow Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_shopShuffleOot(Choice):
    """
    Controls whether or not shops in OoT should have their items shuffled
    - **none**: All the items are vanilla
    - **full**: All 8 items are shuffled
    """
    display_name = "Shop Shuffle (OoT)"
    option_none = 0
    option_full = 1
    default = option_none

class OOTxMM_mainshuffle_shopShuffleMm(Choice):
    """
    Controls whether or not shops in MM should have their items shuffled.<br>If "None" is selected, the Bomb Bag purchases will still be shuffled
    - **none**: All the items are vanilla
    - **full**: All 8 items are shuffled
    """
    display_name = "Shop Shuffle (MM)"
    option_none = 0
    option_full = 1
    default = option_none

class OOTxMM_mainshuffle_owlShuffle(Choice):
    """
    Make Owl Statues items that can be shuffled.
    - **none**: Owl Statues are vanilla
    - **anywhere**: Owl Statues are shuffled in the item pool
    """
    display_name = "Owl Statue Shuffle"
    option_none = 0
    option_anywhere = 1
    default = option_none

class OOTxMM_mainshuffle_shufflePotsOot(Choice):
    """
    Controls whether or not the pots are shuffled (OoT).
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Pots Shuffle (OoT)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shufflePotsMm(Choice):
    """
    Controls whether or not the pots are shuffled (MM).
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Pots Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleCratesOot(Choice):
    """
    Controls whether or not the crates are shuffled (OoT).
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Crates Shuffle (OoT)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleCratesMm(Choice):
    """
    Controls whether or not the crates are shuffled (MM).
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Crates Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleBarrelsMm(Choice):
    """
    Controls whether or not the barrels are shuffled (MM).
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Barrels Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleHivesOot(Toggle):
    """
    Controls whether or not the beehives are shuffled (OoT)
    """
    display_name = "Hives Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleHivesMm(Toggle):
    """
    Controls whether or not the beehives are shuffled (MM)<br>One beehive in the grotto with Bio Babas will always be shuffled regardless of this setting, thus CAMC will not affect it.
    """
    display_name = "Hives Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_shuffleGrassOot(Choice):
    """
    Controls whether or not the grass is shuffled (OoT)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Grass Shuffle (OoT)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleRocksOot(Toggle):
    """
    Controls whether or not the rocks are shuffled (OoT)
    """
    display_name = "Rock Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleRocksMm(Choice):
    """
    Controls whether or not the rocks are shuffled (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Rock Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleGrassMm(Choice):
    """
    Controls whether or not the grass is shuffled (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Grass Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleTFGrassMm(Toggle):
    """
    Controls whether or not the Termina Field grass is shuffled (MM). Grottos do not count towards this
    """
    display_name = "Termina Field Grass Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_shuffleTreesOot(Toggle):
    """
    Controls whether or not the trees are shuffled (OoT)
    """
    display_name = "Tree Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleTreesMm(Choice):
    """
    Controls whether or not the trees are shuffled (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Tree Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleBushOot(Toggle):
    """
    Controls whether or not the bushes are shuffled (OoT)
    """
    display_name = "Bush Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleBushMm(Choice):
    """
    Controls whether or not the bushes are shuffled (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Bush Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleSoilOot(Toggle):
    """
    Controls whether or not the fairies from bean soil spots are shuffled (OoT)
    """
    display_name = "Soil Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleSoilMm(Choice):
    """
    Controls whether or not the items from bean soil spots are shuffled (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Soil Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleFreeRupeesOot(Choice):
    """
    Controls whether or not the freestanding rupees are shuffled (OoT)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Freestanding Rupees Shuffle (OoT)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleFreeRupeesMm(Choice):
    """
    Controls whether or not the freestanding rupees are shuffled (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Freestanding Rupees Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleFreeHeartsOot(Choice):
    """
    Controls whether or not the freestanding hearts are shuffled (OoT)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Freestanding Hearts Shuffle (OoT)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleFreeHeartsMm(Toggle):
    """
    Controls whether or not the freestanding hearts are shuffled (MM)
    """
    display_name = "Freestanding Hearts Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_shuffleGossipFairiesOot(Choice):
    """
    Controls whether or not the gossip stones fairies are shuffled (OoT)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Gossip Fairies Shuffle (OoT)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleGossipBigFairiesOot(Choice):
    """
    Controls whether or not the gossip stones big fairies are shuffled (OoT)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Gossip Big Fairies Shuffle (OoT)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleGossipFairiesMm(Choice):
    """
    Controls whether or not the gossip stones fairies are shuffled (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Gossip Fairies Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleGossipBigFairiesMm(Choice):
    """
    Controls whether or not the gossip stones big fairies are shuffled (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Gossip Big Fairies Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleWonderItemsOot(Choice):
    """
    Controls whether or not the wonder items are shuffled (OoT)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Wonder Items Shuffle (OoT)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleWonderItemsMm(Toggle):
    """
    Controls whether or not the wonder items are shuffled (MM)
    """
    display_name = "Wonder Items Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_shuffleSnowballsMm(Choice):
    """
    Controls whether or not the snowballs are shuffled (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Snowball Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleButterfliesOot(Toggle):
    """
    Controls whether or not the butterflies are shuffled (OoT)
    """
    display_name = "Butterflies Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleButterfliesMm(Toggle):
    """
    Controls whether or not the butterflies are shuffled (MM)
    """
    display_name = "Butterflies Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_shuffleBouldersOot(Choice):
    """
    Controls whether or not the regular boulders drop an item when broken (OoT)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Boulder Drops Shuffle (OoT)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleBouldersMm(Choice):
    """
    Controls whether or not the regular boulders drop an item when broken (MM)
    - **none**
    - **all**
    - **overworld**
    - **dungeons**
    """
    display_name = "Boulder Drops Shuffle (MM)"
    option_none = 0
    option_all = 1
    option_overworld = 2
    option_dungeons = 3
    default = option_none

class OOTxMM_mainshuffle_shuffleRedBouldersOot(Toggle):
    """
    Controls whether or not the red boulders drop an item when broken (OoT)
    """
    display_name = "Red Boulder Drops Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleRedBouldersMm(Toggle):
    """
    Controls whether or not the red boulders drop an item when broken (MM)
    """
    display_name = "Red Boulder Drops Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_shuffleSilverBouldersOot(Toggle):
    """
    Controls whether or not the silver boulders drop an item when broken (OoT)
    """
    display_name = "Silver Boulder Drops Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleFrogsRupeesOot(Toggle):
    """
    Controls whether or not the purple rupees from the Frogs Ocarina Game in Zora's River are shuffled
    """
    display_name = "Frogs Rupees Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleLotteryMm(Toggle):
    """
    Controls whether to shuffle the Lottery. ALL nights will have a different item.
    """
    display_name = "Lottery Shuffle"
    default = False

class OOTxMM_mainshuffle_shuffleIciclesOot(Toggle):
    """
    Controls whether or not grounded icicles drop an item when broken (OoT)
    """
    display_name = "Icicles Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleIciclesMm(Toggle):
    """
    Controls whether or not grounded icicles drop an item when broken (MM)
    """
    display_name = "Icicles Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_shuffleRedIceOot(Toggle):
    """
    Controls whether or not the red ice drop an item for thawing it (OoT)
    """
    display_name = "Red Ice Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleOcarinasOot(Toggle):
    """
    Controls whether or not the two Ocarinas in OoT are shuffled
    """
    display_name = "Ocarina Shuffle (OoT)"
    default = True

class OOTxMM_mainshuffle_shuffleMasterSword(Toggle):
    """
    Controls whether or not the Master Sword is shuffled
    """
    display_name = "Master Sword Shuffle"
    default = True

class OOTxMM_mainshuffle_shuffleGerudoCard(Toggle):
    """
    Controls whether or not the Gerudo Membership Card is shuffled
    """
    display_name = "Gerudo Card Shuffle"
    default = True

class OOTxMM_mainshuffle_shuffleSkulltulaFinalReward(Toggle):
    """
    Controls whether or not the huge rupee obtained by having all 100 gold skulltula tokens is shuffled
    """
    display_name = "Skulltula Final Reward Shuffle"
    default = False

class OOTxMM_mainshuffle_shuffleMaskTrades(Toggle):
    """
    Controls whether or not trading the masks are checks
    """
    display_name = "Mask Trade Shuffle"
    default = False

class OOTxMM_mainshuffle_shuffleMerchantsOot(Toggle):
    """
    Controls whether or not the Old Hag Potion, Talon Milk and Carpet Man Bombchu are shuffled.
    """
    display_name = "Merchants Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_shuffleMerchantsMm(Toggle):
    """
    Controls whether or not the Milk Bar and Gorman milk purchases in MM are shuffled
    """
    display_name = "Merchants Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_pondFishShuffle(Toggle):
    """
    Controls whether or not the Fish (and the Loaches) in the Fishing Pond are shuffled amongst all the items.
    """
    display_name = "Fishing Pond Fish Shuffle"
    default = False

class OOTxMM_mainshuffle_divingGameRupeeShuffle(Toggle):
    """
    Controls whether or not the Zora's Domain Diving Game has 5 random items instead of green, blue, red, purple and 500 rupees.
    """
    display_name = "Diving Game Rupee Shuffle"
    default = False

class OOTxMM_mainshuffle_fairyFountainFairyShuffleOot(Toggle):
    """
    Controls whether or not the fairies in fairy fountains are shuffled (OoT).<br>Includes the fairies in Ganon's Castle behind the invisible wall and in Desert Colossus from the oasis.
    """
    display_name = "Fairy Fountain Fairy Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_fairyFountainFairyShuffleMm(Toggle):
    """
    Controls whether or not the fairies in the Beneath the Well fairy fountain are shuffled (MM).
    """
    display_name = "Fairy Fountain Fairy Shuffle (MM)"
    default = False

class OOTxMM_mainshuffle_fairySpotShuffleOot(Toggle):
    """
    Controls whether or not big fairies in fairy spots are shuffled (OoT). Play either Song of Storms or Sun's Song
    """
    display_name = "Fairy Spot Shuffle (OoT)"
    default = False

class OOTxMM_mainshuffle_eggShuffle(Toggle):
    """
    Fun setting: should using the Weird/Pocket Eggs give an item? If not, they're entirely removed from the game
    """
    display_name = "Weird / Pocket Egg Content Shuffle"
    default = False

class OOTxMM_mainprices_priceOotShops(Choice):
    """
    Sets the price of items inside OoT shops
    - **affordable**: All prices are set to 10 rupees.
    - **vanilla**: All prices are set to their vanilla values.
    - **weighted**: All prices are randomized, but lower prices are favored.
    """
    display_name = "OoT Shop Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    default = option_vanilla

class OOTxMM_mainprices_priceOotScrubs(Choice):
    """
    Sets the price of items sold by OoT scrubs
    - **affordable**: All prices are set to 10 rupees.
    - **vanilla**: All prices are set to their vanilla values.
    - **weighted**: All prices are randomized, but lower prices are favored.
    """
    display_name = "OoT Scrub Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    default = option_vanilla

class OOTxMM_mainprices_priceOotMerchants(Choice):
    """
    Sets the price of items sold by OoT merchants
    - **affordable**: All prices are set to 10 rupees.
    - **vanilla**: All prices are set to their vanilla values.
    - **weighted**: All prices are randomized, but lower prices are favored.
    """
    display_name = "OoT Merchants Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    default = option_vanilla

class OOTxMM_mainprices_priceMmShops(Choice):
    """
    Sets the price of items sold inside MM shops
    - **affordable**: All prices are set to 10 rupees.
    - **vanilla**: All prices are set to their vanilla values.
    - **weighted**: All prices are randomized, but lower prices are favored.
    """
    display_name = "MM Shop Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    default = option_vanilla

class OOTxMM_mainprices_priceMmTingle(Choice):
    """
    Sets the price of items sold by Tingle
    - **affordable**: All prices are set to 10 rupees.
    - **vanilla**: All prices are set to their vanilla values.
    - **weighted**: All prices are randomized, but lower prices are favored.
    """
    display_name = "MM Tingle Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    default = option_vanilla

class OOTxMM_mainevents_songEventsShuffleOot(Toggle):
    """
    Shuffle the various events requiring songs to trigger them (OoT)
    """
    display_name = "Song Events Shuffle (OoT)"
    default = False

class OOTxMM_mainevents_songEventsShuffleMm(Toggle):
    """
    Shuffle the various events requiring songs to trigger them (MM)
    """
    display_name = "Song Events Shuffle (MM)"
    default = False

class OOTxMM_mainevents_ganonTrials(OptionSet):
    """
    Controls which trials in Ganon's Castle are enabled
    ['Light', 'Forest', 'Fire', 'Water', 'Shadow', 'Spirit']
    """
    display_name = "Ganon Trials"
    valid_keys = {
        'Light',
        'Forest',
        'Fire',
        'Water',
        'Shadow',
        'Spirit',
    }
    default = valid_keys.copy()

class OOTxMM_mainevents_moonCrash(Choice):
    """
    Changes the behavior of moon crashing
    - **reset**: When the Moon crashes, all progress made in MM since the last save will be lost. Saving is disabled on the Clock Tower Roof.
    - **cycle**: When the Moon crashes, a new cycle will start, keeping progress. Saving is enabled on the Clock Tower Roof, allowing you to leave by warping back to spawn.
    """
    display_name = "Moon Crash Behavior"
    option_reset = 0
    option_cycle = 1
    default = option_reset

class OOTxMM_mainevents_startingAgeOot(Choice):
    """
    Choose the starting age
    - **child**: Link will start off as Child
    - **adult**: Link will start off as Adult
    """
    display_name = "Starting Age (OoT)"
    option_child = 0
    option_adult = 1
    default = option_child

class OOTxMM_mainevents_startingAgeMm(Choice):
    """
    Choose the starting age in Majora's Mask. If Adult Mask or Cross-Game Age is off, you will be unable to change age in MM.
    - **child**: Link will start off as Child
    - **adult**: Link will start off as Adult
    """
    display_name = "Starting Age (MM)"
    option_child = 0
    option_adult = 1
    default = option_child

class OOTxMM_mainevents_timeTravelSword(Toggle):
    """
    Choose whether or not Link needs the Master Sword to travel through time
    """
    display_name = "Time Travel requires Master Sword"
    default = True

class OOTxMM_mainevents_doorOfTime(Choice):
    """
    Alters the Door of Time state
    - **closed**: The Door will be closed, and you will need to play Song of Time in front of the Temple of Time altar to open it. (The Spiritual Stones and Ocarina of Time are NOT needed)
    - **open**: The Door is already open
    """
    display_name = "Door of Time"
    option_closed = 0
    option_open = 1
    default = option_closed

class OOTxMM_mainevents_ageChange(Choice):
    """
    Allows you to switch ages by playing Song of Time in OoT after you've switched ages once in Temple of Time.<br>Preserves your current position on the scene, which logic can expect you to take advantage of.
    - **none**: Cannot change age by playing Song of Time.
    - **oot**: Can change age by playing Song of Time with the Ocarina of Time specifically.
    - **always**: Can change age by playing Song of Time using any means.
    """
    display_name = "Age Change upon Song of Time"
    option_none = 0
    option_oot = 1
    option_always = 2
    default = option_none

class OOTxMM_mainevents_dekuTree(Choice):
    """
    Controls the behavior of Mido blocking the Deku Tree as Child
    - **closed**: Mido will block the way to the Deku Tree until you have a Deku Shield and the Kokiri Sword.
    - **vanilla**: Mido will block the way to the Deku Tree, but the tree itself will be open as Child.
    - **open**: Mido will not block the way, the Deku Tree will be open from the start
    """
    display_name = "Deku Tree"
    option_closed = 0
    option_vanilla = 1
    option_open = 2
    default = option_open

class OOTxMM_mainevents_openDungeonsOot(OptionSet):
    """
    Opens the entrance to the chosen dungeons
    ['dekuTreeAdult', 'wellAdult', 'fireChild', 'DC', 'BotW', 'JJ', 'Shadow', 'Water']
    """
    display_name = "Open Dungeons (OoT)"
    valid_keys = {
        'dekuTreeAdult',
        'wellAdult',
        'fireChild',
        'DC',
        'BotW',
        'JJ',
        'Shadow',
        'Water',
    }
    default = valid_keys.copy()

class OOTxMM_mainevents_openDungeonsMm(OptionSet):
    """
    Controls whether or not MM dungeons will need their respective song. Takes priority over Clear State
    ['WF', 'SH', 'GB', 'ST']
    """
    display_name = "Open Dungeons (MM)"
    valid_keys = {
        'WF',
        'SH',
        'GB',
        'ST',
    }
    default = valid_keys.copy()

class OOTxMM_mainevents_clearStateDungeonsMm(OptionSet):
    """
    Controls whether or not MM dungeons will need their respective songs in the cleared state
    ['WF', 'GB']
    """
    display_name = "Clear State Dungeons (MM)"
    valid_keys = {
        'WF',
        'GB',
    }
    default = valid_keys.copy()

class OOTxMM_mainevents_beneathWell(Choice):
    """
    Controls the behavior of the Gibdos in Beneath the Well
    - **vanilla**: Nothing changes, Gibdos are back once you reset the cycle.
    - **remorseless**: Once you've given a Gibdo its item, it is permanently gone, also affects the ending ladder and the sun block.
    - **open**: All the Gibdos are already gone, also applies to the ending ladder and the sun block.
    """
    display_name = "Beneath the Well behavior (MM)"
    option_vanilla = 0
    option_remorseless = 1
    option_open = 2
    default = option_vanilla

class OOTxMM_mainevents_kakarikoGate(Choice):
    """
    Controls the behavior of the gate in Kakariko blocking Death Mountain as Child
    - **closed**: The gate will be closed until you show Zelda's Letter to the guard, even as an adult
    - **vanilla**: The gate will be closed until you show Zelda's Letter to the guard
    - **open**: The gate will be open from the start
    """
    display_name = "Kakariko Gate"
    option_closed = 0
    option_vanilla = 1
    option_open = 2
    default = option_vanilla

class OOTxMM_mainevents_openZdShortcut(Toggle):
    """
    Removes the ice blocking Zora's Domain in Lake Hylia as Adult
    """
    display_name = "Open Zora's Domain Shortcut"
    default = False

class OOTxMM_mainevents_zoraKing(Choice):
    """
    Controls the behavior of King Zora in Zora's Domain
    - **vanilla**: You will need to present him Ruto's Letter in order to enter Zora's Fountain as both Child and Adult
    - **adult**: Already on the side as Adult, granting free Zora's Fountain access. Child still needs Ruto's Letter
    - **open**: He will already be on the side for both Child and Adult, and Ruto's Letter is replaced by an empty bottle
    """
    display_name = "King Zora"
    option_vanilla = 0
    option_adult = 1
    option_open = 2
    default = option_vanilla

class OOTxMM_mainevents_gerudoFortress(Choice):
    """
    Controls the behavior of the Carpenters in Gerudo Fortress
    - **vanilla**: You will need to rescue all carpenters.
    - **single**: You will need to rescue only one carpenter.
    - **open**: Carpenters are rescued from the start and the bridge in Gerudo Valley as Adult is repaired.
    """
    display_name = "Gerudo Fortress"
    option_vanilla = 0
    option_single = 1
    option_open = 2
    default = option_vanilla

class OOTxMM_mainevents_skipZelda(Toggle):
    """
    This changes the beginning of the Child trade quest.<br>True means you'll start having already met Zelda and got her item along with the one from Impa.<br>The Chicken is also removed from the game, but Malon will still be at Hyrule Castle
    """
    display_name = "Skip Child Zelda"
    default = False

class OOTxMM_mainevents_openMoon(Toggle):
    """
    Skip playing Oath to Order to reach the Moon, by using a wisp placed on the Clock Tower Roof with this setting
    """
    display_name = "Skip Oath to Order"
    default = False

class OOTxMM_mainevents_moon(Choice):
    """
    Controls how the Moon is accessed
    - **open**: Moon can be accessed as soon as the oath to order can be played
    - **vanilla**: Moon can be accessed when all 4 remains are obtained
    - **custom**: Moon can be accessed when a special condition is met
    """
    display_name = "Moon Access"
    option_open = 0
    option_vanilla = 1
    option_custom = 2
    default = option_vanilla

class OOTxMM_mainevents_lacs(Choice):
    """
    Controls how the Light Arrow Cutscene should be triggered
    - **vanilla**: Triggers at Temple of Time with Shadow and Spirit Medallions
    - **custom**: Triggers at Temple of Time with a special condition
    """
    display_name = "Light Arrow Cutscene"
    option_vanilla = 0
    option_custom = 1
    default = option_vanilla

class OOTxMM_mainevents_rainbowBridge(Choice):
    """
    Controls how the Rainbow Bridge should be triggered
    - **open**: The Rainbow Bridge is always open
    - **vanilla**: Opens when you have the Light Arrows, Shadow Medallion, and Spirit Medallion
    - **medallions**: Opens when you have all Medallions
    - **custom**: You will need to meet a special condition to open the bridge
    """
    display_name = "Rainbow Bridge"
    option_open = 0
    option_vanilla = 1
    option_medallions = 2
    option_custom = 3
    default = option_medallions

class OOTxMM_mainevents_majoraChild(Choice):
    """
    Controls the requirements to enter Majora's arena
    - **none**: As soon as you have satisfied the "Moon Access" special condition you can enter Majora's arena
    - **custom**: You will need to meet the "Majora Child Requirements" special condition to enter Majora's arena
    """
    display_name = "Majora Child Requirements"
    option_none = 0
    option_custom = 1
    default = option_none

class OOTxMM_mainevents_bossWarpPads(Choice):
    """
    Controls the behavior of the MM Boss Warp Pads.
    - **bossBeaten**: Enabled when the boss is beaten
    - **remains**: Enabled when the matching remains are obtained
    """
    display_name = "Boss Warp Pads"
    option_bossBeaten = 0
    option_remains = 1
    default = option_bossBeaten

class OOTxMM_mainevents_regionState(Choice):
    """
    Controls what is required to change the region state.
    - **dungeonBeaten**: Enabled when the dungeon is beaten.
    - **reward**: Enabled when the matching dungeon reward is obtained
    - **free**: Always enabled
    """
    display_name = "Region State Behavior"
    option_dungeonBeaten = 0
    option_reward = 1
    option_free = 2
    default = option_dungeonBeaten

class OOTxMM_mainevents_freeScarecrowOot(Toggle):
    """
    Allows to spawn Pierre the Scarecrow just by pulling the Ocarina out
    """
    display_name = "Free Scarecrow (OoT)"
    default = False

class OOTxMM_mainevents_freeScarecrowMm(Toggle):
    """
    Allows to spawn the Scarecrow just by pulling the Ocarina out
    """
    display_name = "Free Scarecrow (MM)"
    default = False

class OOTxMM_mainevents_strayFairyRewardCount(Range):
    """
    How many stray fairies are required to get the respective Great Fairy reward.
    """
    display_name = "Stray Fairy Reward Count"
    range_start = 0
    range_end = 15
    default = 15

class OOTxMM_mainevents_preCompletedDungeons(Toggle):
    """
    Allow dungeons to be pre-completed depending on rules.<br>Every check in a pre-completed dungeon will be junked, and its boss will be considered defeated, granting clear state access.
    """
    display_name = "Pre-Completed Dungeons"
    default = False

class OOTxMM_mainevents_preCompletedDungeonsMajor(Range):
    """
    How many major dungeons should be pre-completed.<br>Can be combined with other pre-completed dungeon rules.
    """
    display_name = "Pre-Completed Dungeons (Major)"
    range_start = 0
    range_end = 12
    default = 0

class OOTxMM_mainevents_preCompletedDungeonsStones(Range):
    """
    How many OoT Child dungeons containing stones should be pre-completed.<br>Can be combined with other pre-completed dungeon rules.
    """
    display_name = "Pre-Completed Dungeons (Stones)"
    range_start = 0
    range_end = 3
    default = 0

class OOTxMM_mainevents_preCompletedDungeonsMedallions(Range):
    """
    How many OoT Adult dungeons containing medaillons should be pre-completed.<br>Can be combined with other pre-completed dungeon rules.
    """
    display_name = "Pre-Completed Dungeons (Medallions)"
    range_start = 0
    range_end = 6
    default = 0

class OOTxMM_mainevents_preCompletedDungeonsRemains(Range):
    """
    How many MM dungeons containing remains should be pre-completed. Stone Tower Temple and Inverted Stone Tower Temple are considered one dungeon.<br>Can be combined with other pre-completed dungeon rules.
    """
    display_name = "Pre-Completed Dungeons (Remains)"
    range_start = 0
    range_end = 4
    default = 0

class OOTxMM_mainevents_ootPreplantedBeans(Toggle):
    """
    Automatically plants beans in the various soft soils of OoT, as well as removing the beans from the item pool
    """
    display_name = "Pre-Planted Beans (OoT)"
    default = False

class OOTxMM_mainevents_mmPreActivatedOwls(OptionSet):
    """
    Automatically activates Owl Statues on your behalf, and you will also get the items at their location
    ['clocktown', 'milkroad', 'swamp', 'woodfall', 'mountain', 'snowhead', 'greatbay', 'zoracape', 'canyon', 'tower']
    """
    display_name = "Pre-Activated Owl Statues"
    valid_keys = {
        'clocktown',
        'milkroad',
        'swamp',
        'woodfall',
        'mountain',
        'snowhead',
        'greatbay',
        'zoracape',
        'canyon',
        'tower',
    }
    default = valid_keys.copy()

class OOTxMM_maincross_crossAge(Toggle):
    """
    When you enter MM as Adult Link, you will be Adult Link in MM.
    """
    display_name = "Cross-Games Age"
    default = False

class OOTxMM_maincross_crossGameFw(Toggle):
    """
    Controls whether you can use Farore's Wind to warp between OoT and MM.
    """
    display_name = "Cross-Games Farore's Wind"
    default = False

class OOTxMM_maincamc_csmc(Choice):
    """
    Modifies the appearance of chests and other shuffled containers so that they match their content.<br>Other shuffled containers will otherwise always be gold if the item has not been collected.<br>Works for unique items, Small and Boss Keys, Silver Rupees, Stray Fairies, Skulltula Tokens, and Souls
    - **never**: Containers will be vanilla
    - **agony**: Containers will match content when you have the Stone of Agony in OoT
    - **always**: Containers will always match content
    """
    display_name = "Container Appearance Matches Content"
    option_never = 0
    option_agony = 1
    option_always = 2
    default = option_always

class OOTxMM_maincamc_csmcHearts(Toggle):
    """
    Use a specific texture for Heart Pieces/Containers
    """
    display_name = "CAMC for Heart Pieces/Containers"
    default = True

class OOTxMM_maincamc_csmcMapCompass(Toggle):
    """
    Use a specific texture for Maps/Compasses
    """
    display_name = "CAMC for Maps/Compasses"
    default = True

class OOTxMM_maincamc_csmcSkulltula(Toggle):
    """
    Enables CAMC for shuffled Gold, Swamp, and Ocean Skulltulas
    """
    display_name = "Skulltula CAMC"
    default = False

class OOTxMM_maincamc_csmcCow(Toggle):
    """
    Enables CAMC for shuffled Cows
    """
    display_name = "Cow CAMC"
    default = False

class OOTxMM_mainmisc_blastMaskCooldown(Choice):
    """
    Changes the cooldown between each explosion of the Blast Mask
    - **instant**
    - **veryshort**
    - **short**
    - **default**
    - **long**
    - **verylong**
    """
    display_name = "Blast Mask Cooldown"
    option_instant = 0
    option_veryshort = 1
    option_short = 2
    option_default = 3
    option_long = 4
    option_verylong = 5
    default = option_default

class OOTxMM_mainnologic_clockSpeed(Choice):
    """
    Alters the speed of the clock. Some options may render seeds unbeatable due to being unable to do time-related checks
    - **veryslow**: The time will flow 66% slower than usual
    - **slow**: The time will flow 33% slower than usual
    - **default**: The normal clock speed
    - **fast**: The clock speed will be twice as fast than usual
    - **veryfast**: USE AT OWN RISK!! - The clock speed will be 3x faster than usual, even on inverted
    - **superfast**: USE AT OWN RISK!! - The clock speed will be 6x faster than usual, even on inverted
    """
    display_name = "Clock Speed"
    option_veryslow = 0
    option_slow = 1
    option_default = 2
    option_fast = 3
    option_veryfast = 4
    option_superfast = 5
    default = option_default

class OOTxMM_mainnologic_fierceDeityAnywhere(Toggle):
    """
    Controls the ability to use Fierce Deity outside of boss lairs. No logical applications
    """
    display_name = "Fierce Deity Anywhere in MM"
    default = False

class OOTxMM_mainmisc_hookshotAnywhereOot(Choice):
    """
    Modifies all surfaces to be able to be hooked onto and if it is expected in logic
    - **off**
    - **enabled**
    - **logical**
    """
    display_name = "Hookshot Anywhere (OoT)"
    option_off = 0
    option_enabled = 1
    option_logical = 2
    default = option_off

class OOTxMM_mainmisc_hookshotAnywhereMm(Choice):
    """
    Modifies all surfaces to be able to be hooked onto and if it is expected in logic
    - **off**
    - **enabled**
    - **logical**
    """
    display_name = "Hookshot Anywhere (MM)"
    option_off = 0
    option_enabled = 1
    option_logical = 2
    default = option_off

class OOTxMM_mainmisc_climbMostSurfacesOot(Choice):
    """
    Modifies most surfaces to be climbable and if it is expected in logic
    - **off**
    - **enabled**
    - **logical**
    """
    display_name = "Climb Most Surfaces (OoT)"
    option_off = 0
    option_enabled = 1
    option_logical = 2
    default = option_off

class OOTxMM_mainnologic_climbMostSurfacesMm(Toggle):
    """
    Modifies most surfaces to be climbable
    """
    display_name = "Climb Most Surfaces (MM)"
    default = False

class OOTxMM_mainmisc_restoreBrokenActors(Toggle):
    """
    In vanilla OoT, some actors fails to load properly in some rooms due to errors in the room files. When this is on, these actors will load.
    """
    display_name = "Restore Broken Actors"
    default = False

class OOTxMM_mainmisc_alterLostWoodsExits(Toggle):
    """
    There are unused exits in the Lost Woods that return you back to the Lost Woods.<br>When this is on, all the "got lost" exits in the Lost Woods that would normally take you to Kokiri Forest instead take you back to the Lost Woods, keeping your compass direction intact.
    """
    display_name = "Alter Lost Woods Exits"
    default = False

class OOTxMM_mainmisc_voidWarpMm(Toggle):
    """
    In vanilla OoT, various code only checks for transitionTrigger, but in MM it also checks for transitionMode.<br>When this is on, MM will no longer check transitionMode in those circumstances, allowing you to perform the Void Warp glitch in MM.
    """
    display_name = "Void Warp in MM"
    default = False

class OOTxMM_mainnologic_damageMultiplierOot(Choice):
    """
    Modifies the damage dealt to the player. Logic is NOT adjusted for this setting. Use at your own risk.
    - **normal**
    - **double**
    - **quadruple**
    - **octuple**
    - **ohko**
    """
    display_name = "Damage Multiplier (OoT)"
    option_normal = 0
    option_double = 1
    option_quadruple = 2
    option_octuple = 3
    option_ohko = 4
    default = option_normal

class OOTxMM_mainnologic_damageMultiplierMm(Choice):
    """
    Modifies the damage dealt to the player. Logic is NOT adjusted for this setting. Use at your own risk.
    - **normal**
    - **double**
    - **quadruple**
    - **octuple**
    - **ohko**
    """
    display_name = "Damage Multiplier (MM)"
    option_normal = 0
    option_double = 1
    option_quadruple = 2
    option_octuple = 3
    option_ohko = 4
    default = option_normal

class OOTxMM_mainnologic_mmStyleAirMovementOot(Toggle):
    """
    Makes the air movement in OoT more like the air movement in MM.
    """
    display_name = "MM-style air movement in OoT"
    default = False

class OOTxMM_mainnologic_ootHyperEnemies(Toggle):
    """
    Make enemies and most bosses in OoT be twice as fast.
    """
    display_name = "Hyper Enemies (OoT)"
    default = False

class OOTxMM_mainnologic_mmHyperEnemies(Toggle):
    """
    Make enemies and bosses in MM be twice as fast.
    """
    display_name = "Hyper Enemies (MM)"
    default = False

class OOTxMM_itemsprogressive_progressiveShieldsOot(Choice):
    """
    Alters the behavior of the OoT Shields
    - **separate**: They can be found independently from each other
    - **progressive**: Each Progressive Shield will grant you the next one: Deku Shield -> Hylian Shield -> Mirror Shield. Other Deku and Hylian Shields are removed from the item pool.
    """
    display_name = "OoT Shields"
    option_separate = 0
    option_progressive = 1
    default = option_separate

class OOTxMM_itemsprogressive_progressiveSwordsOot(Choice):
    """
    Alters the behavior of the OoT Swords
    - **separate**: They can be found independently from each other
    - **goron**: Kokiri Sword and Master Sword are independent. However, Giant's Knife and Biggoron Sword are progressive.
    - **progressive**: Each Progressive Sword will grant you the next one: Kokiri Sword -> Master Sword -> Giant's Knife -> Biggoron Sword
    """
    display_name = "OoT Swords"
    option_separate = 0
    option_goron = 1
    option_progressive = 2
    default = option_goron

class OOTxMM_itemsprogressive_progressiveShieldsMm(Choice):
    """
    Alters the behavior of the MM Shields
    - **separate**: They can be found independently from each other
    - **progressive**: Each Progressive Shield will grant you the next one: Hero's Shield -> Mirror Shield. Other Hero's Shields are removed from the item pool.
    """
    display_name = "MM Shields"
    option_separate = 0
    option_progressive = 1
    default = option_separate

class OOTxMM_itemsprogressive_progressiveGFS(Choice):
    """
    Controls whether the Great Fairy Sword is included in sword progression
    - **separate**
    - **progressive**
    """
    display_name = "MM Great Fairy Sword"
    option_separate = 0
    option_progressive = 1
    default = option_separate

class OOTxMM_itemsprogressive_progressiveGoronLullabyMm(Choice):
    """
    Alters the behavior of the MM Goron Lullaby
    - **single**: Only the Goron Lullaby can be found, and when playing with Songs on Song Locations, Baby Goron in MM is no longer a Song Location
    - **progressive**: The Lullaby Intro will be received first before getting the full song
    """
    display_name = "MM Goron Lullaby"
    option_single = 0
    option_progressive = 1
    default = option_progressive

class OOTxMM_itemsprogressive_progressiveGoronLullabyOot(Choice):
    """
    Alters the behavior of the OoT Goron Lullaby
    - **single**: Only the Goron Lullaby can be found
    - **progressive**: The Lullaby Intro will be received first before getting the full song
    """
    display_name = "OoT Goron Lullaby"
    option_single = 0
    option_progressive = 1
    default = option_progressive

class OOTxMM_itemsprogressive_progressiveClocks(Choice):
    """
    Alters the behavior of Clocks
    - **separate**: Clocks will be independent of each other. If you don't select a starting clock, you start with a random clock.
    - **ascending**: Clocks will be received in ascending order, with Day 1 already unlocked.
    - **descending**: Clocks will be received in descending order, with Night 3 already unlocked.
    """
    display_name = "Clocks"
    option_separate = 0
    option_ascending = 1
    option_descending = 2
    default = option_ascending

class OOTxMM_itemsextensionsgeneral_fillWallets(Toggle):
    """
    Fills the wallet upon finding a new one
    """
    display_name = "Fill Wallets"
    default = False

class OOTxMM_itemsextensionsgeneral_bottleContentShuffle(Toggle):
    """
    Randomize what bottles from both games contain upon finding them in the world
    """
    display_name = "Random Bottle Contents"
    default = False

class OOTxMM_itemsextensionscrossGameitems_stoneAgonyMm(Toggle):
    """
    Enables Stone of Agony in MM
    """
    display_name = "Stone of Agony in MM"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sticksNutsUpgradesMm(Toggle):
    """
    Enables Deku Stick and Nut upgrades in MM
    """
    display_name = "Deku Stick & Nut Upgrades in MM"
    default = False

class OOTxMM_itemsextensionsgeneral_sticksNutsUpgradesInitial(Toggle):
    """
    Shuffle the initial stick & nuts.
    """
    display_name = "Shuffle Initial Deku Stick & Nut Upgrades"
    default = False

class OOTxMM_itemsextensionscrossGameitems_fairyOcarinaMm(Toggle):
    """
    Functionally identical as the Ocarina of Time, but now there's 2 Ocarinas for Majora's Mask!
    """
    display_name = "Fairy Ocarina in MM"
    default = False

class OOTxMM_itemsextensionsoot_blueFireArrows(Toggle):
    """
    Gives the OoT Ice Arrows the properties of Blue Fire
    """
    display_name = "Blue Fire Arrows"
    default = False

class OOTxMM_itemsextensionsoot_iceArrowPlatformsOot(Toggle):
    """
    Allow ice arrows in OoT to create walkable ice platforms on water
    """
    display_name = "Ice Arrow Platforms (OoT)"
    default = False

class OOTxMM_itemsextensionsoot_sunlightArrows(Toggle):
    """
    Gives the OoT Light Arrows the ability to activate most sun switches
    """
    display_name = "Sunlight Arrows"
    default = False

class OOTxMM_itemsextensionscrossGameitems_shortHookshotMm(Toggle):
    """
    Adds a short Hookshot in MM, which logic accounts for. A trick is also there for some of the harder spots
    """
    display_name = "Short Hookshot in MM"
    default = False

class OOTxMM_itemsextensionsgeneral_bronzeScale(Toggle):
    """
    Add an extra scale item, that is required to enter deep water.
    """
    display_name = "Bronze Scale"
    default = False

class OOTxMM_itemsextensionsgeneral_childWallets(Toggle):
    """
    Shuffles the starting wallet in each game... making it so you have to find it to hold anything!
    """
    display_name = "Child Wallets"
    default = False

class OOTxMM_itemsextensionsgeneral_colossalWallets(Toggle):
    """
    Adds a Wallet that can hold up to 999 rupees in each game
    """
    display_name = "Colossal Wallets"
    default = False

class OOTxMM_itemsextensionsgeneral_bottomlessWallets(Toggle):
    """
    Adds a Wallet that can hold up to 9999 rupees in each game
    """
    display_name = "Bottomless Wallets"
    default = False

class OOTxMM_itemsextensionsgeneral_rupeeScaling(Toggle):
    """
    Makes rupees worth twice as much with the Colossal Wallet, and twenty times as much with the Bottomless Wallet.
    """
    display_name = "Rupee Scaling"
    default = False

class OOTxMM_itemsextensionssystems_skeletonKeyOot(Toggle):
    """
    Adds a Skeleton Key that can open every small-key-locked door in OoT.
    """
    display_name = "Skeleton Key (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_skeletonKeyMm(Toggle):
    """
    Adds a Skeleton Key that can open every small-key-locked door in MM.
    """
    display_name = "Skeleton Key (MM)"
    default = False

class OOTxMM_itemsextensionsoot_magicalRupee(Toggle):
    """
    Adds a Magical Rupee that can trigger every silver-rupee event in OoT dungeons.
    """
    display_name = "Magical Rupee"
    default = False

class OOTxMM_itemsextensionsmm_transcendentFairy(Toggle):
    """
    Adds a Transcendent Fairy that counts as every Stray Fairy in MM.
    """
    display_name = "Transcendent Fairy"
    default = False

class OOTxMM_itemsextensionssystems_platinumTokenOot(Toggle):
    """
    Adds a Platinum Token that counts as every Gold Skulltula Token.
    """
    display_name = "Platinum Token (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_platinumTokenMm(Toggle):
    """
    Adds a Platinum Token that counts as every House Token.
    """
    display_name = "Platinum Token (MM)"
    default = False

class OOTxMM_itemsextensionssystems_bombchuBehaviorOot(Choice):
    """
    Controls the behavior of bombchu.
    - **free**: Bombchu can be used as soon as a pack is obtained. No bombchu drops. Max ammo is 50.
    - **bombBag**: Bombchu can be used when you have the Bomb Bag. No bombchu drops. Max ammo is the Bomb Bag maximum.
    - **bagFirst**: The first non-purchased pack you find will turn into a Bombchu Bag, which adds bombchu drops alongside non-randomized ammo drops. Bombchu Bags make bombchu logical, replacing Bomb Bags. Max ammo is 50.
    - **bagSeparate**: Bombchu Bags separate from bombchu packs are added to the item pool, which add bombchu drops alongside non-randomized ammo drops. Bombchu are only usable with a Bombchu Bag, replacing Bomb Bags in logic. Max ammo is 20/30/40 each.
    """
    display_name = "Bombchu Behavior (OoT)"
    option_free = 0
    option_bombBag = 1
    option_bagFirst = 2
    option_bagSeparate = 3
    default = option_free

class OOTxMM_itemsextensionssystems_bombchuBehaviorMm(Choice):
    """
    Controls the behavior of bombchu.
    - **free**: Bombchu can be used as soon as a pack is obtained. No bombchu drops. Max ammo is 50.
    - **bombBag**: Bombchu can be used when you have the Bomb Bag. No bombchu drops. Max ammo is the Bomb Bag maximum.
    - **bagFirst**: The first non-purchased pack you find will turn into a Bombchu Bag, which adds bombchu drops alongside non-randomized ammo drops. Bombchu Bags make bombchu logical, replacing Bomb Bags. Max ammo is 50.
    - **bagSeparate**: Bombchu Bags separate from bombchu packs are added to the item pool, which add bombchu drops alongside non-randomized ammo drops. Bombchu are only usable with a Bombchu Bag, replacing Bomb Bags in logic. Max ammo is 20/30/40 each.
    """
    display_name = "Bombchu Behavior (MM)"
    option_free = 0
    option_bombBag = 1
    option_bagFirst = 2
    option_bagSeparate = 3
    default = option_bombBag

class OOTxMM_itemsextensionscrossGameitems_spellFireMm(Toggle):
    """
    Adds Din's Fire in Majora's Mask.
    """
    display_name = "Din's Fire (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_spellWindMm(Toggle):
    """
    Adds Farore's Wind in Majora's Mask.
    """
    display_name = "Farore's Wind (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_spellLoveMm(Toggle):
    """
    Adds Nayru's Love in Majora's Mask.
    """
    display_name = "Nayru's Love (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_bootsIronMm(Toggle):
    """
    Adds Iron Boots in Majora's Mask.
    """
    display_name = "Iron Boots (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_bootsHoverMm(Toggle):
    """
    Adds Hover Boots in Majora's Mask.
    """
    display_name = "Hover Boots (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_tunicGoronMm(Toggle):
    """
    Adds the Goron Tunic in Majora's Mask.
    """
    display_name = "Goron Tunic (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_tunicZoraMm(Toggle):
    """
    Adds the Zora Tunic in Majora's Mask.
    """
    display_name = "Zora Tunic (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_scalesMm(Toggle):
    """
    Adds the Silver Scale and Golden Scale in Majora's Mask.
    """
    display_name = "Scales (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_strengthMm(Toggle):
    """
    Adds the Goron's Bracelet, Silver Gauntlets and Golden Gauntlets in Majora's Mask.
    """
    display_name = "Strength (MM)"
    default = False

class OOTxMM_itemsextensionsmm_kegStrength3(Toggle):
    """
    If you have the Golden Gauntlets in Majora's Mask, this allows you to purchase and use Powder Kegs, and attempt the Keg Trial.
    """
    display_name = "Use Keg With Golden Gauntlets"
    default = False

class OOTxMM_itemsextensionscrossGameitems_hammerMm(Toggle):
    """
    Adds the Megaton Hammer in Majora's Mask.
    """
    display_name = "Megaton Hammer (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_boomerangMm(Toggle):
    """
    Adds the Boomerang in Majora's Mask.
    """
    display_name = "Boomerang (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_gfsOot(Toggle):
    """
    Adds the Great Fairy's Sword in Ocarina of Time.
    """
    display_name = "Great Fairy's Sword (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_slingshotMm(Toggle):
    """
    Adds the Slingshot in Majora's Mask.
    """
    display_name = "Slingshot (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_spinUpgradeOot(Toggle):
    """
    Add the Spin Attack upgrade as an item in OoT.
    """
    display_name = "Spin Attack Upgrade (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_extraChildSwordsOot(Toggle):
    """
    Add the Razor and Gilded Swords in OoT, as upgrades to the Kokiri Sword.
    """
    display_name = "Extra Child Swords (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_dekuShieldMm(Toggle):
    """
    Add the Deku Shield in Majora's Mask.
    """
    display_name = "Deku Shield (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_blastMaskOot(Toggle):
    """
    Add the Blast Mask in Ocarina of Time.
    """
    display_name = "Blast Mask (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_stoneMaskOot(Toggle):
    """
    Add the Stone Mask in Ocarina of Time.
    """
    display_name = "Stone Mask (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_kamaroMaskOot(Toggle):
    """
    Add the Kamaro Mask in Ocarina of Time.
    """
    display_name = "Kamaro Mask (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_gerudoMaskMm(Toggle):
    """
    Add the Gerudo Mask in Majora's Mask which can be used as a disguise to enter Pirates Fortress.
    """
    display_name = "Gerudo Mask (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_skullMaskMm(Toggle):
    """
    Add the Skull Mask in Majora's Mask which can be used as a disguise to enter the Deku Palace.
    """
    display_name = "Skull Mask (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_spookyMaskMm(Toggle):
    """
    Add the Spooky Mask in Majora's Mask. The spooky mask functions like the Gibdo mask but only at night.
    """
    display_name = "Spooky Mask (MM)"
    default = False

class OOTxMM_itemsextensionsmm_adultMaskMm(Toggle):
    """
    Add the Adult Mask in Majora's Mask. The Adult mask allows you to change age in Majora's Mask.
    """
    display_name = "Adult Mask"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_elegyOot(Toggle):
    """
    Add the Elegy of Emptiness in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Elegy of Emptiness (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songSoaringOot(Toggle):
    """
    Add the Song of Soaring in Ocarina of Time. Usable only as child. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Song of Soaring (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songHealingOot(Toggle):
    """
    Add the Song of Healing in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Song of Healing (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songAwakeningOot(Toggle):
    """
    Add the Sonata of Awakening in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Sonata of Awakening (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songGoronOot(Toggle):
    """
    Add the Goron Lullaby in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Goron Lullaby (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songZoraOot(Toggle):
    """
    Add the New Wave Bossa Nova in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "New Wave Bossa Nova (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songOrderOot(Toggle):
    """
    Add the Oath to Order in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Oath to Order (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songSunMm(Toggle):
    """
    Add Sun's Song in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Sun's Song (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songZeldaLullabyMm(Toggle):
    """
    Add Zelda's Lullaby in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Zelda's Lullaby (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songSariasMm(Toggle):
    """
    Add Saria's Song in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Saria's Song (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songMinuetMm(Toggle):
    """
    Add the Minuet of Forest in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Minuet of Forest (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songBoleroMm(Toggle):
    """
    Add the Bolero of Fire in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Bolero of Fire (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songSerenadeMm(Toggle):
    """
    Add the Serenade of Water in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Serenade of Water (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songRequiemMm(Toggle):
    """
    Add the Requiem of Spirit in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Requiem of Spirit (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songNocturneMm(Toggle):
    """
    Add the Nocturne of Shadow in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Nocturne of Shadow (MM)"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_songPreludeMm(Toggle):
    """
    Add the Prelude of Light in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Prelude of Light (MM)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_powderKegOot(Toggle):
    """
    Add the Powder Keg in Ocarina of Time. Once found, Medigoron in Goron City will sell Powder Kegs after you buy his item.
    """
    display_name = "Powder Keg (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_extraBottlesOot(Toggle):
    """
    Allows Ocarina of Time to have up to six bottles by using the Adult and Child trade slots for the fifth and sixth bottles.
    """
    display_name = "Extra Bottles (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_ocarinaButtonsShuffleOot(Toggle):
    """
    Add the Ocarina Buttons for OoT into the item pool. Ocarina notes cannot be played until the corresponding button is obtained.
    """
    display_name = "Ocarina Buttons (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_ocarinaButtonsShuffleMm(Toggle):
    """
    Add the Ocarina Buttons for MM into the item pool. Ocarina notes cannot be played until the corresponding button is obtained.
    """
    display_name = "Ocarina Buttons (MM)"
    default = False

class OOTxMM_itemsextensionssystems_shovelOot(Toggle):
    """
    Add a shovel to the item pool. The shovel is required to access grottos.
    """
    display_name = "Shovel (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_shovelMm(Toggle):
    """
    Add a shovel to the item pool. The shovel is required to access grottos.
    """
    display_name = "Shovel (MM)"
    default = False

class OOTxMM_itemsextensionssystems_soulsEnemyOot(Toggle):
    """
    Add Souls for OoT enemies into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Enemy Souls (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_soulsEnemyMm(Toggle):
    """
    Add Souls for MM enemies into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Enemy Souls (MM)"
    default = False

class OOTxMM_itemsextensionssystems_soulsBossOot(Toggle):
    """
    Add Souls for OoT bosses into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Boss Souls (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_soulsBossMm(Toggle):
    """
    Add Souls for MM bosses into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Boss Souls (MM)"
    default = False

class OOTxMM_itemsextensionssystems_soulsNpcOot(Toggle):
    """
    Add Souls for OoT NPCs into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "NPC Souls (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_soulsNpcMm(Toggle):
    """
    Add Souls for MM NPCs into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "NPC Souls (MM)"
    default = False

class OOTxMM_itemsextensionssystems_soulsAnimalOot(Toggle):
    """
    Add Souls for OoT animals into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Animal Souls (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_soulsAnimalMm(Toggle):
    """
    Add Souls for MM animals into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Animal Souls (MM)"
    default = False

class OOTxMM_itemsextensionssystems_soulsMiscOot(Toggle):
    """
    Add Souls for OoT Business Scrubs and Gold Skulltulas into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Misc. Souls (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_soulsMiscMm(Toggle):
    """
    Add Souls for MM Business Scrubs and Gold Skulltulas into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Misc. Souls (MM)"
    default = False

class OOTxMM_itemsextensionssystems_rustyKeysOot(Toggle):
    """
    Add rusty keys to the item pool. Every rusty key locks a single overworld door.
    """
    display_name = "Rusty Keys (OoT)"
    default = False

class OOTxMM_itemsextensionssystems_rustyKeysMm(Toggle):
    """
    Add rusty keys to the item pool. Every rusty key locks a single overworld door.
    """
    display_name = "Rusty Keys (MM)"
    default = False

class OOTxMM_itemsextensionssystems_clocksMm(Toggle):
    """
    Add items representing every Majora's Mask day and night into the pool. The moon will crash early unless you collect these items.
    """
    display_name = "Clocks as Items (MM)"
    default = False

class OOTxMM_itemsextensionssystems_clocksOot(Choice):
    """
    Add an item representing the flow of time in Ocarina of Time into the pool. You will be locked at either noon or midnight unless you collect this item.
    - **none**: Disabled
    - **day**: The world will allways experience daytime until you find the clock.
    - **night**: The world will allways experience nighttime until you find the clock.
    """
    display_name = "Clock as Item (OoT)"
    option_none = 0
    option_day = 1
    option_night = 2
    default = option_none

class OOTxMM_itemsextensionsmm_menuNotebook(Toggle):
    """
    Locks the in-game tracker behind the Bombers' Notebook
    """
    display_name = "Bombers' Tracker"
    default = False

class OOTxMM_itemsextensionscoins_coins(Toggle):
    """
    Enable the leftover Coin items. These can be used for special conditions
    """
    display_name = "Coins"
    default = False

class OOTxMM_itemsextensionscoins_coinsRed(Range):
    """
    How many Red Coins to add to the item pool
    """
    display_name = "Red Coins"
    range_start = 0
    range_end = 999
    default = 0

class OOTxMM_itemsextensionscoins_coinsGreen(Range):
    """
    How many Green Coins to add to the item pool
    """
    display_name = "Green Coins"
    range_start = 0
    range_end = 999
    default = 0

class OOTxMM_itemsextensionscoins_coinsBlue(Range):
    """
    How many Blue Coins to add to the item pool
    """
    display_name = "Blue Coins"
    range_start = 0
    range_end = 999
    default = 0

class OOTxMM_itemsextensionscoins_coinsYellow(Range):
    """
    How many Yellow Coins to add to the item pool
    """
    display_name = "Yellow Coins"
    range_start = 0
    range_end = 999
    default = 0

class OOTxMM_itemsextensionstraps_trapIce(Toggle):
    """
    Add Ice Traps to the item pool. They freeze you when collected.
    """
    display_name = "Ice Traps"
    default = True

class OOTxMM_itemsextensionstraps_trapFire(Toggle):
    """
    Add Fire Traps to the item pool. They burn you when collected.
    """
    display_name = "Fire Traps"
    default = False

class OOTxMM_itemsextensionstraps_trapShock(Toggle):
    """
    Add Shock Traps to the item pool. They shock you when collected.
    """
    display_name = "Shock Traps"
    default = False

class OOTxMM_itemsextensionstraps_trapDrain(Toggle):
    """
    Add Drain Traps to the item pool. They drain your life when collected.
    """
    display_name = "Drain Traps"
    default = False

class OOTxMM_itemsextensionstraps_trapAntiMagic(Toggle):
    """
    Add Anti-Magic Traps to the item pool. They drain magic from you when collected.
    """
    display_name = "Anti-Magic Traps"
    default = False

class OOTxMM_itemsextensionstraps_trapKnockback(Toggle):
    """
    Add Knockback Traps to the item pool. They throw you in a random direction.
    """
    display_name = "Knockback Traps"
    default = False

class OOTxMM_itemsextensionstraps_trapRupoor(Toggle):
    """
    Add Rupoors to the item pool. They remove 10 rupees when collected.
    """
    display_name = "Rupoors"
    default = False

class OOTxMM_itemsextensionstraps_cloakTraps(Toggle):
    """
    Makes traps look like different items.
    """
    display_name = "Cloak Traps"
    default = True

class OOTxMM_itemsextensionstraps_trapsQuantity(Choice):
    """
    Controls the number of traps relative to the number of junk items in the pool.
    - **small**: 5 traps per 100 junk items
    - **medium**: 10 traps per 100 junk items
    - **large**: 20 traps per 100 junk items
    - **verylarge**: 50 traps per 100 junk items
    - **extreme**: 100 traps per 100 junk items
    - **insane**: 500 traps per 100 junk items
    - **obnoxious**: 1000 traps per 100 junk items
    - **absurd**: 5000 traps per 100 junk items
    """
    display_name = "Traps Quantity"
    option_small = 0
    option_medium = 1
    option_large = 2
    option_verylarge = 3
    option_extreme = 4
    option_insane = 5
    option_obnoxious = 6
    option_absurd = 7
    default = option_small

class OOTxMM_main_trapsLink(Toggle):
    """
    If enabled, traps are shared between players. If disabled, each player has it's own set of traps.
    """
    display_name = "Linked Multiworld Traps"
    default = False

class OOTxMM_itemsextensionsoot_songOfDoubleTimeOot(Toggle):
    """
    Enables using Song of Double Time in OoT when you have the Song of Time in OoT
    """
    display_name = "Song of Double Time (OoT)"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedStoneAgony(Toggle):
    """
    Combines the Stones of Agony from OoT and MM into one item for both games
    """
    display_name = "Shared Stone of Agony"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedSpinUpgrade(Toggle):
    """
    Combines the Spin Attack Upgrades from OoT and MM into one item for both games
    """
    display_name = "Shared Spin Attack Upgrade"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedNutsSticks(Toggle):
    """
    Combines the Deku Stick and Nut Upgrades from OoT and MM into two items each for both games
    """
    display_name = "Shared Deku Sticks & Nuts"
    default = False

class OOTxMM_itemsextensionsshared_sharedBows(Toggle):
    """
    Combines the Bows from OoT and MM into three progressive items for both games
    """
    display_name = "Shared Bows"
    default = False

class OOTxMM_itemsextensionsshared_sharedBombBags(Toggle):
    """
    Combines the Bomb Bags from OoT and MM into three progressive items for both games
    """
    display_name = "Shared Bomb Bags"
    default = False

class OOTxMM_itemsextensionsshared_sharedMagic(Toggle):
    """
    Combines the Magic Upgrades from OoT and MM into two progressive items for both games
    """
    display_name = "Shared Magic"
    default = False

class OOTxMM_itemsextensionsshared_sharedMagicArrowFire(Toggle):
    """
    Combines the Fire Arrows from OoT and MM into one item for both games
    """
    display_name = "Shared Fire Arrows"
    default = False

class OOTxMM_itemsextensionsshared_sharedMagicArrowIce(Toggle):
    """
    Combines the Ice Arrows from OoT and MM into one item for both games
    """
    display_name = "Shared Ice Arrows"
    default = False

class OOTxMM_itemsextensionsshared_sharedMagicArrowLight(Toggle):
    """
    Combines the Light Arrows from OoT and MM into one item for both games
    """
    display_name = "Shared Light Arrows"
    default = False

class OOTxMM_itemsextensionsshared_sharedSongEpona(Toggle):
    """
    Combines Epona's Song from OoT and MM into one item for both games
    """
    display_name = "Shared Epona's Song"
    default = False

class OOTxMM_itemsextensionsshared_sharedSongStorms(Toggle):
    """
    Combines Song of Storms from OoT and MM into one item for both games
    """
    display_name = "Shared Song of Storms"
    default = False

class OOTxMM_itemsextensionsshared_sharedSongTime(Toggle):
    """
    Combines Song of Time from OoT and MM into one item for both games
    """
    display_name = "Shared Song of Time"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongSun(Toggle):
    """
    Combines Sun's Song from OoT and MM into one item for both games
    """
    display_name = "Shared Sun's Song"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedHookshot(Toggle):
    """
    Combines the Hookshots from OoT and MM into two progressive items for both games.<br>If "Short Hookshot in MM" is disabled, the MM Hookshot will be given along with the first progressive item.
    """
    display_name = "Shared Hookshots"
    default = False

class OOTxMM_itemsextensionsshared_sharedLens(Toggle):
    """
    Combines the Lenses of Truth from OoT and MM into one item for both games
    """
    display_name = "Shared Lens of Truth"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedOcarina(Toggle):
    """
    Combines the Ocarinas from OoT and MM into two progressive items for both games.<br>If "Fairy Ocarina in MM" is disabled, the MM Ocarina will be given along with the second progressive item.
    """
    display_name = "Shared Ocarinas"
    default = False

class OOTxMM_itemsextensionsshared_sharedMaskGoron(Toggle):
    """
    Combines the Goron Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Goron Mask"
    default = False

class OOTxMM_itemsextensionsshared_sharedMaskZora(Toggle):
    """
    Combines the Zora Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Zora Mask"
    default = False

class OOTxMM_itemsextensionsshared_sharedMaskBunny(Toggle):
    """
    Combines the Bunny Hoods from OoT and MM into one item for both games
    """
    display_name = "Shared Bunny Hood"
    default = False

class OOTxMM_itemsextensionsshared_sharedMaskKeaton(Toggle):
    """
    Combines the Keaton Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Keaton Mask"
    default = False

class OOTxMM_itemsextensionsshared_sharedMaskTruth(Toggle):
    """
    Combines the Masks of Truth from OoT and MM into one item for both games
    """
    display_name = "Shared Mask of Truth"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_sharedMaskBlast(Toggle):
    """
    Combines the Blast Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Blast Mask"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_sharedMaskStone(Toggle):
    """
    Combines the Stone Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Stone Mask"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_sharedMaskKamaro(Toggle):
    """
    Combines the Kamaro Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Kamaro Mask"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongElegy(Toggle):
    """
    Combines the Elegies of Emptiness from OoT and MM into one item for both games
    """
    display_name = "Shared Elegy of Emptiness"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongHealing(Toggle):
    """
    Combines the Songs of Healing from OoT and MM into one item for both games
    """
    display_name = "Shared Song of Healing"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongSoaring(Toggle):
    """
    Combines the Songs of Song from OoT and MM into one item for both games
    """
    display_name = "Shared Song of Soaring"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongAwakening(Toggle):
    """
    Combines the Sonata of Awakening from OoT and MM into one item for both games
    """
    display_name = "Shared Sonata of Awakening"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongGoron(Toggle):
    """
    Combines the Goron Lullaby from OoT and MM into one item for both games
    """
    display_name = "Shared Goron Lullaby"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongZora(Toggle):
    """
    Combines the New Wave Bossa Nova from OoT and MM into one item for both games
    """
    display_name = "Shared New Wave Bossa Nova"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongOrder(Toggle):
    """
    Combines the Oath to Order from OoT and MM into one item for both games
    """
    display_name = "Shared Oath to Order"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongZeldaLullaby(Toggle):
    """
    Combines Zelda's Lullaby from OoT and MM into one item for both games
    """
    display_name = "Shared Zelda's Lullaby"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongSarias(Toggle):
    """
    Combines Saria's Song from OoT and MM into one item for both games
    """
    display_name = "Shared Saria's Song"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongMinuet(Toggle):
    """
    Combines the Minuet of Forest from OoT and MM into one item for both games
    """
    display_name = "Shared Minuet of Forest"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongBolero(Toggle):
    """
    Combines the Bolero of Fire from OoT and MM into one item for both games
    """
    display_name = "Shared Bolero of Fire"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongSerenade(Toggle):
    """
    Combines the Serenade of Water from OoT and MM into one item for both games
    """
    display_name = "Shared Serenade of Water"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongRequiem(Toggle):
    """
    Combines the Requiem of Spirit from OoT and MM into one item for both games
    """
    display_name = "Shared Requiem of Spirit"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongNocturne(Toggle):
    """
    Combines the Nocturne of Shadow from OoT and MM into one item for both games
    """
    display_name = "Shared Nocturne of Shadow"
    default = False

class OOTxMM_itemsextensionscrossGamesongs_sharedSongPrelude(Toggle):
    """
    Combines the Prelude of Light from OoT and MM into one item for both games
    """
    display_name = "Shared Prelude of Light"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedPowderKeg(Toggle):
    """
    Combines the Powder Kegs from OoT and MM into one item for both games.
    """
    display_name = "Shared Powder Keg"
    default = False

class OOTxMM_itemsextensionsshared_sharedWallets(Toggle):
    """
    Combines the Wallets from OoT and MM into multiple progressive items for both games, depending on settings
    """
    display_name = "Shared Wallets"
    default = False

class OOTxMM_itemsextensionsshared_sharedHealth(Toggle):
    """
    Combines the Heart Pieces, Heart Containers and Double Defenses from OoT and MM into 44 Heart Pieces, 6 Heart Containers and one Double Defense for both games
    """
    display_name = "Shared Health"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedSwords(Toggle):
    """
    Combines the Kokiri, Razor and Gilded Swords from OoT and MM into three progressive items for both games
    """
    display_name = "Shared Child Swords"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedShields(Toggle):
    """
    When you obtain a shield, the opposite game's equivalent is given to you as well. With this, the Hylian and Hero's Shields are considered equivalent.<br>If Shields are Progressive, all Shields are combined into three progressive items: Deku Shield -> Hylian/Hero's Shield -> Mirror Shield
    """
    display_name = "Shared Shields"
    default = False

class OOTxMM_itemsextensionssystems_sharedSoulsEnemy(Toggle):
    """
    Combines the OoT and MM Souls for a specific enemy into one item, for all enemies present in both games
    """
    display_name = "Shared Enemy Souls"
    default = False

class OOTxMM_itemsextensionssystems_sharedSoulsNpc(Toggle):
    """
    Combines the OoT and MM Souls for a specific NPC into one item, for all NPCs present in both games
    """
    display_name = "Shared NPC Souls"
    default = False

class OOTxMM_itemsextensionssystems_sharedSoulsAnimal(Toggle):
    """
    Combines the OoT and MM Souls for a specific animal into one item, for all animals present in both games
    """
    display_name = "Shared Animal Souls"
    default = False

class OOTxMM_itemsextensionssystems_sharedSoulsMisc(Toggle):
    """
    Combines the OoT and MM Souls for Business Scrubs and Gold Skulltulas into two items for both games
    """
    display_name = "Shared Misc. Souls"
    default = False

class OOTxMM_itemsextensionssystems_sharedOcarinaButtons(Toggle):
    """
    Combines the Ocarina Buttons from OoT and MM into five items for both games
    """
    display_name = "Shared Ocarina Buttons"
    default = False

class OOTxMM_itemsextensionssystems_sharedShovel(Toggle):
    """
    Combines the Shovels from OoT and MM into a single item for both games
    """
    display_name = "Shared Shovel"
    default = False

class OOTxMM_itemsextensionssystems_sharedSkeletonKey(Toggle):
    """
    Combines the Skeleton Key from OoT and MM into one item for both games
    """
    display_name = "Shared Skeleton Key"
    default = False

class OOTxMM_itemsextensionssystems_sharedPlatinumToken(Toggle):
    """
    Combines the Platinum Token from OoT and MM into one item for both games
    """
    display_name = "Shared Platinum Token"
    default = False

class OOTxMM_itemsextensionssystems_sharedBombchu(Toggle):
    """
    Combines either Bombchu or the Bombchu Bags from OoT and MM into items for both games, depending on settings
    """
    display_name = "Shared Bombchu"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedSpellFire(Toggle):
    """
    Combines Din's Fire from OoT and MM into one item for both games
    """
    display_name = "Shared Din's Fire"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedSpellWind(Toggle):
    """
    Combines Farore's Wind from OoT and MM into one item for both games
    """
    display_name = "Shared Farore's Wind"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedSpellLove(Toggle):
    """
    Combines Nayru's Love from OoT and MM into one item for both games
    """
    display_name = "Shared Nayru's Love"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedBootsIron(Toggle):
    """
    Combines the Iron Boots from OoT and MM into one item for both games
    """
    display_name = "Shared Iron Boots"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedBootsHover(Toggle):
    """
    Combines the Hover Boots from OoT and MM into one item for both games
    """
    display_name = "Shared Hover Boots"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedTunicGoron(Toggle):
    """
    Combines the Goron Tunics from OoT and MM into two items for both games
    """
    display_name = "Shared Goron Tunic"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedTunicZora(Toggle):
    """
    Combines the Zora Tunics from OoT and MM into two items for both games
    """
    display_name = "Shared Zora Tunic"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedScales(Toggle):
    """
    Combines the Scales from OoT and MM into multiple progressive items for both games, depending on settings
    """
    display_name = "Shared Scales"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedStrength(Toggle):
    """
    Combines the Strength Upgrades from OoT and MM into three progressive items for both games
    """
    display_name = "Shared Strength"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedHammer(Toggle):
    """
    Combines the Megaton Hammers from OoT and MM into one item for both games
    """
    display_name = "Shared Megaton Hammer"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedBoomerang(Toggle):
    """
    Combines the Boomerangs from OoT and MM into one item for both games
    """
    display_name = "Shared Boomerang"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedGFS(Toggle):
    """
    Combines the Great Fairy's Sword from OoT and MM into one item for both games
    """
    display_name = "Shared Great Fairy's Sword"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedSlingshot(Toggle):
    """
    Combines the Slingshots from OoT and MM into one item for both games
    """
    display_name = "Shared Slingshot"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_sharedMaskGerudo(Toggle):
    """
    Combines the Gerudo Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Gerudo Mask"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_sharedMaskSkull(Toggle):
    """
    Combines the Skull Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Skull Mask"
    default = False

class OOTxMM_itemsextensionscrossGamemasks_sharedMaskSpooky(Toggle):
    """
    Combines the Spooky Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Spooky Mask"
    default = False

class OOTxMM_itemsextensionscrossGameitems_sharedBottles(Toggle):
    """
    Combines the bottles from OoT and MM into six items for both games. The six bottles are: Red Potion, Gold Dust, Chateau, Milk, Ruto's Letter and an Empty Bottle. Bottle refills are also shared.
    """
    display_name = "Shared Bottles"
    default = False

class OOTxMM_itemsageless_agelessSwords(Toggle):
    """
    Allows Link to use swords independently of his age
    """
    display_name = "Ageless Swords"
    default = False

class OOTxMM_itemsageless_agelessShields(Toggle):
    """
    Allows Link to use shields independently of his age
    """
    display_name = "Ageless Shields"
    default = False

class OOTxMM_itemsageless_agelessTunics(Toggle):
    """
    Allows Link to use tunics independently of his age
    """
    display_name = "Ageless Tunics"
    default = False

class OOTxMM_itemsageless_agelessBoots(Toggle):
    """
    Allows Link to use boots independently of his age
    """
    display_name = "Ageless Boots"
    default = False

class OOTxMM_itemsageless_agelessSticks(Toggle):
    """
    Allows Link to use Deku Sticks independently of his age
    """
    display_name = "Ageless Sticks"
    default = False

class OOTxMM_itemsageless_agelessBoomerang(Toggle):
    """
    Allows Link to use the Boomerang independently of his age
    """
    display_name = "Ageless Boomerang"
    default = False

class OOTxMM_itemsageless_agelessHammer(Toggle):
    """
    Allows Link to use the Hammer independently of his age
    """
    display_name = "Ageless Hammer"
    default = False

class OOTxMM_itemsageless_agelessGFS(Toggle):
    """
    Allows Link to use the Great Fairy Sword independently of his age
    """
    display_name = "Ageless Great Fairy Sword"
    default = False

class OOTxMM_itemsageless_agelessHookshot(Toggle):
    """
    Allows Link to use the Hookshot independently of his age
    """
    display_name = "Ageless Hookshot"
    default = False

class OOTxMM_itemsageless_agelessSlingshot(Toggle):
    """
    Allows Link to use the Slingshot independently of his age
    """
    display_name = "Ageless Slingshot"
    default = False

class OOTxMM_itemsageless_agelessBow(Toggle):
    """
    Allows Link to use the Bow independently of his age
    """
    display_name = "Ageless Bow"
    default = False

class OOTxMM_itemsageless_agelessChildTrade(Toggle):
    """
    Allows Link to use the Child trade items independently of his age
    """
    display_name = "Ageless Child Trade"
    default = False

class OOTxMM_itemsageless_agelessStrength(Toggle):
    """
    Allows Child Link to use the Adult Strength upgrades
    """
    display_name = "Ageless Strength"
    default = False

class OOTxMM_itemsageless_agelessSoaring(Toggle):
    """
    Allows Link to use the Song of Soaring in OoT independently of his age
    """
    display_name = "Ageless Song of Soaring"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildHookshot(Toggle):
    """
    Requires Child Link to equip Hookshot in MM.
    """
    display_name = "Hookshot requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultHookshot(Toggle):
    """
    Requires Adult Link to equip Hookshot in MM.
    """
    display_name = "Hookshot requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildHookshotShort(Toggle):
    """
    Requires Child Link to equip Short Hookshot in MM.
    """
    display_name = "Short Hookshot requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultHookshotShort(Toggle):
    """
    Requires Adult Link to equip Short Hookshot in MM.
    """
    display_name = "Short Hookshot requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBow(Toggle):
    """
    Requires Child Link to equip Bow in MM.
    """
    display_name = "Bow requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBow(Toggle):
    """
    Requires Adult Link to equip Bow in MM.
    """
    display_name = "Bow requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildOcarinaOfTime(Toggle):
    """
    Requires Child Link to equip Ocarina of Time in MM.
    """
    display_name = "Ocarina of Time requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultOcarinaOfTime(Toggle):
    """
    Requires Adult Link to equip Ocarina of Time in MM.
    """
    display_name = "Ocarina of Time requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildOcarinaFairy(Toggle):
    """
    Requires Child Link to equip Fairy Ocarina in MM.
    """
    display_name = "Fairy Ocarina requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultOcarinaFairy(Toggle):
    """
    Requires Adult Link to equip Fairy Ocarina in MM.
    """
    display_name = "Fairy Ocarina requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBomb(Toggle):
    """
    Requires Child Link to equip Bombs in MM.
    """
    display_name = "Bombs requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBomb(Toggle):
    """
    Requires Adult Link to equip Bombs in MM.
    """
    display_name = "Bombs requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBombchu(Toggle):
    """
    Requires Child Link to equip Bombchu in MM.
    """
    display_name = "Bombchu requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBombchu(Toggle):
    """
    Requires Adult Link to equip Bombchu in MM.
    """
    display_name = "Bombchu requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildArrowFire(Toggle):
    """
    Requires Child Link to equip Fire Arrow in MM.
    """
    display_name = "Fire Arrow requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultArrowFire(Toggle):
    """
    Requires Adult Link to equip Fire Arrow in MM.
    """
    display_name = "Fire Arrow requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildArrowIce(Toggle):
    """
    Requires Child Link to equip Ice Arrow in MM.
    """
    display_name = "Ice Arrow requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultArrowIce(Toggle):
    """
    Requires Adult Link to equip Ice Arrow in MM.
    """
    display_name = "Ice Arrow requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildArrowLight(Toggle):
    """
    Requires Child Link to equip Light Arrow in MM.
    """
    display_name = "Light Arrow requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultArrowLight(Toggle):
    """
    Requires Adult Link to equip Light Arrow in MM.
    """
    display_name = "Light Arrow requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildHammer(Toggle):
    """
    Requires Child Link to equip Megaton Hammer in MM.
    """
    display_name = "Megaton Hammer requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultHammer(Toggle):
    """
    Requires Adult Link to equip Megaton Hammer in MM.
    """
    display_name = "Megaton Hammer requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSpellWind(Toggle):
    """
    Requires Child Link to equip Farore's Wind in MM.
    """
    display_name = "Farore's Wind requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSpellWind(Toggle):
    """
    Requires Adult Link to equip Farore's Wind in MM.
    """
    display_name = "Farore's Wind requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSpellLove(Toggle):
    """
    Requires Child Link to equip Nayru's Love in MM.
    """
    display_name = "Nayru's Love requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSpellLove(Toggle):
    """
    Requires Adult Link to equip Nayru's Love in MM.
    """
    display_name = "Nayru's Love requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSpellFire(Toggle):
    """
    Requires Child Link to equip Din's Fire in MM.
    """
    display_name = "Din's Fire requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSpellFire(Toggle):
    """
    Requires Adult Link to equip Din's Fire in MM.
    """
    display_name = "Din's Fire requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBootsIron(Toggle):
    """
    Requires Child Link to equip Iron Boots in MM.
    """
    display_name = "Iron Boots requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBootsIron(Toggle):
    """
    Requires Adult Link to equip Iron Boots in MM.
    """
    display_name = "Iron Boots requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBootsHover(Toggle):
    """
    Requires Child Link to equip Hover Boots in MM.
    """
    display_name = "Hover Boots requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBootsHover(Toggle):
    """
    Requires Adult Link to equip Hover Boots in MM.
    """
    display_name = "Hover Boots requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildTunicGoron(Toggle):
    """
    Requires Child Link to equip Goron Tunic in MM.
    """
    display_name = "Goron Tunic requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultTunicGoron(Toggle):
    """
    Requires Adult Link to equip Goron Tunic in MM.
    """
    display_name = "Goron Tunic requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildTunicZora(Toggle):
    """
    Requires Child Link to equip Zora Tunic in MM.
    """
    display_name = "Zora Tunic requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultTunicZora(Toggle):
    """
    Requires Adult Link to equip Zora Tunic in MM.
    """
    display_name = "Zora Tunic requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildGreatFairySword(Toggle):
    """
    Requires Child Link to equip Great Fairy Sword in MM.
    """
    display_name = "Great Fairy Sword requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultGreatFairySword(Toggle):
    """
    Requires Adult Link to equip Great Fairy Sword in MM.
    """
    display_name = "Great Fairy Sword requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBoomerang(Toggle):
    """
    Requires Child Link to equip Boomerang in MM.
    """
    display_name = "Boomerang requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBoomerang(Toggle):
    """
    Requires Adult Link to equip Boomerang in MM.
    """
    display_name = "Boomerang requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSlingshot(Toggle):
    """
    Requires Child Link to equip Slingshot in MM.
    """
    display_name = "Slingshot requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSlingshot(Toggle):
    """
    Requires Adult Link to equip Slingshot in MM.
    """
    display_name = "Slingshot requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildStick(Toggle):
    """
    Requires Child Link to equip Deku Stick in MM.
    """
    display_name = "Deku Stick requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultStick(Toggle):
    """
    Requires Adult Link to equip Deku Stick in MM.
    """
    display_name = "Deku Stick requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskDeku(Toggle):
    """
    Requires Child Link to equip Deku Mask in MM.
    """
    display_name = "Deku Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskDeku(Toggle):
    """
    Requires Adult Link to equip Deku Mask in MM.
    """
    display_name = "Deku Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDekuNuts(Toggle):
    """
    Requires Child Link to equip Deku Nuts in MM.
    """
    display_name = "Deku Nuts requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDekuNuts(Toggle):
    """
    Requires Adult Link to equip Deku Nuts in MM.
    """
    display_name = "Deku Nuts requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMagicBean(Toggle):
    """
    Requires Child Link to equip Magic Bean in MM.
    """
    display_name = "Magic Bean requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMagicBean(Toggle):
    """
    Requires Adult Link to equip Magic Bean in MM.
    """
    display_name = "Magic Bean requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildPowderKeg(Toggle):
    """
    Requires Child Link to equip Powder Keg in MM.
    """
    display_name = "Powder Keg requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultPowderKeg(Toggle):
    """
    Requires Adult Link to equip Powder Keg in MM.
    """
    display_name = "Powder Keg requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildPictographBox(Toggle):
    """
    Requires Child Link to equip Pictograph Box in MM.
    """
    display_name = "Pictograph Box requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultPictographBox(Toggle):
    """
    Requires Adult Link to equip Pictograph Box in MM.
    """
    display_name = "Pictograph Box requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildLensOfTruth(Toggle):
    """
    Requires Child Link to equip Lens of Truth in MM.
    """
    display_name = "Lens of Truth requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultLensOfTruth(Toggle):
    """
    Requires Adult Link to equip Lens of Truth in MM.
    """
    display_name = "Lens of Truth requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGoron(Toggle):
    """
    Requires Child Link to equip Goron Mask in MM.
    """
    display_name = "Goron Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGoron(Toggle):
    """
    Requires Adult Link to equip Goron Mask in MM.
    """
    display_name = "Goron Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskZora(Toggle):
    """
    Requires Child Link to equip Zora Mask in MM.
    """
    display_name = "Zora Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskZora(Toggle):
    """
    Requires Adult Link to equip Zora Mask in MM.
    """
    display_name = "Zora Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskFierceDeity(Toggle):
    """
    Requires Child Link to equip Fierce Deity Mask in MM.
    """
    display_name = "Fierce Deity Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskFierceDeity(Toggle):
    """
    Requires Adult Link to equip Fierce Deity Mask in MM.
    """
    display_name = "Fierce Deity Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskPostman(Toggle):
    """
    Requires Child Link to equip Postman Hat in MM.
    """
    display_name = "Postman Hat requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskPostman(Toggle):
    """
    Requires Adult Link to equip Postman Hat in MM.
    """
    display_name = "Postman Hat requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskAllNight(Toggle):
    """
    Requires Child Link to equip All-Night Mask in MM.
    """
    display_name = "All-Night Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskAllNight(Toggle):
    """
    Requires Adult Link to equip All-Night Mask in MM.
    """
    display_name = "All-Night Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskBlast(Toggle):
    """
    Requires Child Link to equip Blast Mask in MM.
    """
    display_name = "Blast Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskBlast(Toggle):
    """
    Requires Adult Link to equip Blast Mask in MM.
    """
    display_name = "Blast Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskStone(Toggle):
    """
    Requires Child Link to equip Stone Mask in MM.
    """
    display_name = "Stone Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskStone(Toggle):
    """
    Requires Adult Link to equip Stone Mask in MM.
    """
    display_name = "Stone Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGreatFairy(Toggle):
    """
    Requires Child Link to equip Great Fairy Mask in MM.
    """
    display_name = "Great Fairy Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGreatFairy(Toggle):
    """
    Requires Adult Link to equip Great Fairy Mask in MM.
    """
    display_name = "Great Fairy Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskKeaton(Toggle):
    """
    Requires Child Link to equip Keaton Mask in MM.
    """
    display_name = "Keaton Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskKeaton(Toggle):
    """
    Requires Adult Link to equip Keaton Mask in MM.
    """
    display_name = "Keaton Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskBremen(Toggle):
    """
    Requires Child Link to equip Bremen Mask in MM.
    """
    display_name = "Bremen Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskBremen(Toggle):
    """
    Requires Adult Link to equip Bremen Mask in MM.
    """
    display_name = "Bremen Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskBunny(Toggle):
    """
    Requires Child Link to equip Bunny Hood in MM.
    """
    display_name = "Bunny Hood requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskBunny(Toggle):
    """
    Requires Adult Link to equip Bunny Hood in MM.
    """
    display_name = "Bunny Hood requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskDonGero(Toggle):
    """
    Requires Child Link to equip Don Gero Mask in MM.
    """
    display_name = "Don Gero Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskDonGero(Toggle):
    """
    Requires Adult Link to equip Don Gero Mask in MM.
    """
    display_name = "Don Gero Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskScents(Toggle):
    """
    Requires Child Link to equip Mask of Scents in MM.
    """
    display_name = "Mask of Scents requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskScents(Toggle):
    """
    Requires Adult Link to equip Mask of Scents in MM.
    """
    display_name = "Mask of Scents requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskRomani(Toggle):
    """
    Requires Child Link to equip Romani Mask in MM.
    """
    display_name = "Romani Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskRomani(Toggle):
    """
    Requires Adult Link to equip Romani Mask in MM.
    """
    display_name = "Romani Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskTroupeLeader(Toggle):
    """
    Requires Child Link to equip Troupe Leader Mask in MM.
    """
    display_name = "Troupe Leader Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskTroupeLeader(Toggle):
    """
    Requires Adult Link to equip Troupe Leader Mask in MM.
    """
    display_name = "Troupe Leader Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskKafei(Toggle):
    """
    Requires Child Link to equip Kafei Mask in MM.
    """
    display_name = "Kafei Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskKafei(Toggle):
    """
    Requires Adult Link to equip Kafei Mask in MM.
    """
    display_name = "Kafei Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskCouple(Toggle):
    """
    Requires Child Link to equip Couple's Mask in MM.
    """
    display_name = "Couple's Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskCouple(Toggle):
    """
    Requires Adult Link to equip Couple's Mask in MM.
    """
    display_name = "Couple's Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskTruth(Toggle):
    """
    Requires Child Link to equip Mask of Truth in MM.
    """
    display_name = "Mask of Truth requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskTruth(Toggle):
    """
    Requires Adult Link to equip Mask of Truth in MM.
    """
    display_name = "Mask of Truth requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskKamaro(Toggle):
    """
    Requires Child Link to equip Kamaro Mask in MM.
    """
    display_name = "Kamaro Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskKamaro(Toggle):
    """
    Requires Adult Link to equip Kamaro Mask in MM.
    """
    display_name = "Kamaro Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGibdo(Toggle):
    """
    Requires Child Link to equip Gibdo Mask in MM.
    """
    display_name = "Gibdo Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGibdo(Toggle):
    """
    Requires Adult Link to equip Gibdo Mask in MM.
    """
    display_name = "Gibdo Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGaro(Toggle):
    """
    Requires Child Link to equip Garo Mask in MM.
    """
    display_name = "Garo Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGaro(Toggle):
    """
    Requires Adult Link to equip Garo Mask in MM.
    """
    display_name = "Garo Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskCaptain(Toggle):
    """
    Requires Child Link to equip Captain's Hat in MM.
    """
    display_name = "Captain's Hat requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskCaptain(Toggle):
    """
    Requires Adult Link to equip Captain's Hat in MM.
    """
    display_name = "Captain's Hat requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGiant(Toggle):
    """
    Requires Child Link to equip Giant's Mask in MM.
    """
    display_name = "Giant's Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGiant(Toggle):
    """
    Requires Adult Link to equip Giant's Mask in MM.
    """
    display_name = "Giant's Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGerudo(Toggle):
    """
    Requires Child Link to equip Gerudo Mask in MM.
    """
    display_name = "Gerudo Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGerudo(Toggle):
    """
    Requires Adult Link to equip Gerudo Mask in MM.
    """
    display_name = "Gerudo Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskSkull(Toggle):
    """
    Requires Child Link to equip Skull Mask in MM.
    """
    display_name = "Skull Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskSkull(Toggle):
    """
    Requires Adult Link to equip Skull Mask in MM.
    """
    display_name = "Skull Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskSpooky(Toggle):
    """
    Requires Child Link to equip Spooky Mask in MM.
    """
    display_name = "Spooky Mask requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskSpooky(Toggle):
    """
    Requires Adult Link to equip Spooky Mask in MM.
    """
    display_name = "Spooky Mask requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMoonTear(Toggle):
    """
    Requires Child Link to equip Moon's Tear in MM.
    """
    display_name = "Moon's Tear requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMoonTear(Toggle):
    """
    Requires Adult Link to equip Moon's Tear in MM.
    """
    display_name = "Moon's Tear requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedLand(Toggle):
    """
    Requires Child Link to equip Land Title Deed in MM.
    """
    display_name = "Land Title Deed requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedLand(Toggle):
    """
    Requires Adult Link to equip Land Title Deed in MM.
    """
    display_name = "Land Title Deed requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedSwamp(Toggle):
    """
    Requires Child Link to equip Swamp Title Deed in MM.
    """
    display_name = "Swamp Title Deed requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedSwamp(Toggle):
    """
    Requires Adult Link to equip Swamp Title Deed in MM.
    """
    display_name = "Swamp Title Deed requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedMountain(Toggle):
    """
    Requires Child Link to equip Mountain Title Deed in MM.
    """
    display_name = "Mountain Title Deed requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedMountain(Toggle):
    """
    Requires Adult Link to equip Mountain Title Deed in MM.
    """
    display_name = "Mountain Title Deed requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedOcean(Toggle):
    """
    Requires Child Link to equip Ocean Title Deed in MM.
    """
    display_name = "Ocean Title Deed requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedOcean(Toggle):
    """
    Requires Adult Link to equip Ocean Title Deed in MM.
    """
    display_name = "Ocean Title Deed requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildLetterToMama(Toggle):
    """
    Requires Child Link to equip Priority Mail to Mama in MM.
    """
    display_name = "Priority Mail to Mama requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultLetterToMama(Toggle):
    """
    Requires Adult Link to equip Priority Mail to Mama in MM.
    """
    display_name = "Priority Mail to Mama requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildLetterToKafei(Toggle):
    """
    Requires Child Link to equip Letter to Kafei in MM.
    """
    display_name = "Letter to Kafei requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultLetterToKafei(Toggle):
    """
    Requires Adult Link to equip Letter to Kafei in MM.
    """
    display_name = "Letter to Kafei requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildPendantOfMemories(Toggle):
    """
    Requires Child Link to equip Pendant of Memories in MM.
    """
    display_name = "Pendant of Memories requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultPendantOfMemories(Toggle):
    """
    Requires Adult Link to equip Pendant of Memories in MM.
    """
    display_name = "Pendant of Memories requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqChildStrength(Toggle):
    """
    Requires Child Link to equip Silver/Golden Gauntlets in MM.
    """
    display_name = "Silver/Golden Gauntlets requires Child Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultStrength(Toggle):
    """
    Requires Adult Link to equip Silver/Golden Gauntlets in MM.
    """
    display_name = "Silver/Golden Gauntlets requires Adult Link"
    default = False

class OOTxMM_itemsmmAgeRequirements_mmAgeReqRandom(OptionSet):
    """
    Items whose MM age requirement is chosen randomly from the seed.
    ['hookshot', 'hookshotShort', 'bow', 'ocarinaOfTime', 'ocarinaFairy', 'bomb', 'bombchu', 'arrowFire', 'arrowIce', 'arrowLight', 'hammer', 'spellWind', 'spellLove', 'spellFire', 'bootsIron', 'bootsHover', 'tunicGoron', 'tunicZora', 'greatFairySword', 'boomerang', 'slingshot', 'stick', 'maskDeku', 'nut', 'magicBean', 'powderKeg', 'pictographBox', 'lensOfTruth', 'maskGoron', 'maskZora', 'maskFierceDeity', 'maskPostman', 'maskAllNight', 'maskBlast', 'maskStone', 'maskGreatFairy', 'maskKeaton', 'maskBremen', 'maskBunny', 'maskDonGero', 'maskScents', 'maskRomani', 'maskTroupeLeader', 'maskKafei', 'maskCouple', 'maskTruth', 'maskKamaro', 'maskGibdo', 'maskGaro', 'maskCaptain', 'maskGiant', 'maskGerudo', 'maskSkull', 'maskSpooky', 'moonTear', 'deedLand', 'deedSwamp', 'deedMountain', 'deedOcean', 'letterToMama', 'letterToKafei', 'pendantOfMemories', 'strength']
    """
    display_name = "Random MM Age Requirements"
    valid_keys = {
        'hookshot',
        'hookshotShort',
        'bow',
        'ocarinaOfTime',
        'ocarinaFairy',
        'bomb',
        'bombchu',
        'arrowFire',
        'arrowIce',
        'arrowLight',
        'hammer',
        'spellWind',
        'spellLove',
        'spellFire',
        'bootsIron',
        'bootsHover',
        'tunicGoron',
        'tunicZora',
        'greatFairySword',
        'boomerang',
        'slingshot',
        'stick',
        'maskDeku',
        'nut',
        'magicBean',
        'powderKeg',
        'pictographBox',
        'lensOfTruth',
        'maskGoron',
        'maskZora',
        'maskFierceDeity',
        'maskPostman',
        'maskAllNight',
        'maskBlast',
        'maskStone',
        'maskGreatFairy',
        'maskKeaton',
        'maskBremen',
        'maskBunny',
        'maskDonGero',
        'maskScents',
        'maskRomani',
        'maskTroupeLeader',
        'maskKafei',
        'maskCouple',
        'maskTruth',
        'maskKamaro',
        'maskGibdo',
        'maskGaro',
        'maskCaptain',
        'maskGiant',
        'maskGerudo',
        'maskSkull',
        'maskSpooky',
        'moonTear',
        'deedLand',
        'deedSwamp',
        'deedMountain',
        'deedOcean',
        'letterToMama',
        'letterToKafei',
        'pendantOfMemories',
        'strength',
    }
    default = valid_keys.copy()

class OOTxMM_entrances_erSelfLoops(Toggle):
    """
    Allow entrances to loop back to the same map. Might make the topology of the world very confusing.
    """
    display_name = "Allow Self-Loops"
    default = False

class OOTxMM_entrances_erNoPolarity(Toggle):
    """
    Some entrances have a polarity, for example dungeon entrances and exits.<br>Normally, they're shuffled respecting that polarity, so a dungeon entrance will always lead to the inside of a dungeon, never to a dungeon exit. This option disables that.
    """
    display_name = "No Entrance Polarity"
    default = False

class OOTxMM_entrances_erDecoupled(Toggle):
    """
    Makes the entrances decoupled from the exits.<br>This means that entering and exiting an area does not lead you back to where you came from, but to a different location instead.
    """
    display_name = "Decoupled Entrances"
    default = False

class OOTxMM_entrances_erBoss(Choice):
    """
    Shuffle bosses either within their own game or across both
    - **none**
    - **ownGame**
    - **full**
    """
    display_name = "Boss Entrance Shuffle"
    option_none = 0
    option_ownGame = 1
    option_full = 2
    default = option_none

class OOTxMM_entrances_erDungeons(Choice):
    """
    Shuffle dungeons either within their own game or across both
    - **none**
    - **ownGame**
    - **full**
    """
    display_name = "Dungeon Entrance Shuffle"
    option_none = 0
    option_ownGame = 1
    option_full = 2
    default = option_none

class OOTxMM_entrances_erMajorDungeons(Toggle):
    """
    If turned on, the boss-containing dungeons and uninverted Stone Tower Temple will be shuffled among dungeons.
    """
    display_name = "Shuffle Major Dungeons with Dungeons"
    default = False

class OOTxMM_entrances_erMinorDungeons(Toggle):
    """
    If turned on, Bottom of the Well, Ice Cavern and Gerudo Training Grounds will be shuffled among dungeons.
    """
    display_name = "Shuffle OoT Minor Dungeons with Dungeons"
    default = False

class OOTxMM_entrances_erGanonCastle(Toggle):
    """
    If turned on, Ganon's Castle will be shuffled among dungeons.
    """
    display_name = "Shuffle Ganon's Castle with Dungeons"
    default = False

class OOTxMM_entrances_erGanonTower(Toggle):
    """
    If turned on, Ganon's Tower will be shuffled among dungeons.
    """
    display_name = "Shuffle Ganon's Tower with Dungeons"
    default = False

class OOTxMM_entrances_erMoon(Toggle):
    """
    If turned on, Clock Tower Roof will be shuffled among dungeons.<br>When paired with another dungeon shuffle, saving is enabled on the Clock Tower Roof, allowing you to leave by warping back to spawn.
    """
    display_name = "Shuffle Clock Tower Roof with Dungeons"
    default = False

class OOTxMM_entrances_erSpiderHouses(Toggle):
    """
    If turned on, the Swamp and Ocean Spider Houses will be shuffled among dungeons.
    """
    display_name = "Shuffle Spider Houses with Dungeons"
    default = False

class OOTxMM_entrances_erPirateFortress(Toggle):
    """
    If turned on, the main Pirates' Fortress entrance will be shuffled among dungeons.<br>This setting is disabled if the other entrances are shuffled among the overworld.
    """
    display_name = "Shuffle Pirates' Fortress with Dungeons"
    default = False

class OOTxMM_entrances_erBeneathWell(Toggle):
    """
    If turned on, the entrance in Ikana Canyon and the exit in Ikana Castle Exterior will be shuffled among dungeons.
    """
    display_name = "Shuffle Beneath The Well with Dungeons"
    default = False

class OOTxMM_entrances_erIkanaCastle(Toggle):
    """
    If turned on, the main entrance leading into Ikana Castle's Interior will be shuffled among dungeons.
    """
    display_name = "Shuffle Ikana Castle's Interior with Dungeons"
    default = False

class OOTxMM_entrances_erSecretShrine(Toggle):
    """
    If turned on, Secret Shrine will be shuffled among dungeons.
    """
    display_name = "Shuffle Secret Shrine with Dungeons"
    default = False

class OOTxMM_entrances_erGrottos(Choice):
    """
    Shuffle grottos and graves either within their own game or across both
    - **none**
    - **ownGame**
    - **full**
    """
    display_name = "Grotto Shuffle"
    option_none = 0
    option_ownGame = 1
    option_full = 2
    default = option_none

class OOTxMM_entrances_erIndoors(Choice):
    """
    Shuffle interiors either within their own game or across both
    - **none**
    - **ownGame**
    - **full**
    """
    display_name = "Interiors Shuffle"
    option_none = 0
    option_ownGame = 1
    option_full = 2
    default = option_none

class OOTxMM_entrances_erIndoorsMajor(Toggle):
    """
    Shuffle most interiors with each other.
    """
    display_name = "Shuffle Most Interiors"
    default = False

class OOTxMM_entrances_erIndoorsExtra(Toggle):
    """
    Shuffle additional, more complex interiors. These include:<br>- OoT: Link's House, Temple of Time, Windmill, Kak Potion Shop<br>- MM: Stock Pot Inn, Astral Observatory/Bombers' Hideout, Swamp Tourist Hut, Ikana Spring Cave, Music Box House<br>- Pirate's Fortress Sewers Exit if Shuffle Pirate Fortress Entrances is enabled
    """
    display_name = "Shuffle Extra Interiors"
    default = False

class OOTxMM_entrances_erIndoorsTelescopes(Toggle):
    """
    Shuffle Telescopes (Astral Observatory, Kafei Hideout, Pirate Fortress Sewers) among the interiors.
    """
    display_name = "Shuffle Telescopes"
    default = False

class OOTxMM_entrances_erIndoorsGameLinks(Toggle):
    """
    Shuffle the Mask Shop & Clock Tower entrances among the other indoors.
    """
    display_name = "Shuffle Mask Shop/Clock Tower Entrances"
    default = False

class OOTxMM_entrances_erRegions(Choice):
    """
    Shuffle major regions either within their own game or across both. These include:<br>- Every entrance to Hyrule Field except Market<br>- The entrance to Gerudo Fortress from Gerudo Valley<br>- The entrance to Death Mountain from Kakariko<br>- The entrances to the four main regions in MM<br>- The entrance to Romani Ranch
    - **none**
    - **ownGame**
    - **full**
    """
    display_name = "Major Regions Shuffle"
    option_none = 0
    option_ownGame = 1
    option_full = 2
    default = option_none

class OOTxMM_entrances_erRegionsExtra(Toggle):
    """
    Shuffle the entrance from Hyrule Field to Market among the regions.
    """
    display_name = "Shuffle Market Entrance"
    default = False

class OOTxMM_entrances_erRegionsShortcuts(Toggle):
    """
    Shuffles the various shortcuts between regions. These include:<br>- Lost Woods/Goron City<br>- Lost Woods/Zora's River<br>- Zora's Domain/Lake Hylia
    """
    display_name = "Shuffle Regional Shortcuts"
    default = False

class OOTxMM_entrances_erOverworld(Choice):
    """
    Shuffle every overworld entrance either within their own game or across both
    - **none**
    - **ownGame**
    - **full**
    """
    display_name = "Overworld Shuffle"
    option_none = 0
    option_ownGame = 1
    option_full = 2
    default = option_none

class OOTxMM_entrances_erPiratesWorld(Toggle):
    """
    Shuffle some entrances within Pirates' Fortress, including the main entrance if Overworld ER is enabled.<br>Shuffle the Sewers exit door if Extra Interiors are enabled.
    """
    display_name = "Shuffle Pirates' Fortress Entrances"
    default = False

class OOTxMM_entrances_erMixed(Choice):
    """
    Allow shuffling multiple pools together.
    - **none**
    - **ownGame**
    - **full**
    """
    display_name = "Mixed Pools"
    option_none = 0
    option_ownGame = 1
    option_full = 2
    default = option_none

class OOTxMM_entrances_erMixedDungeons(Toggle):
    """
    If turned on, dungeons will be shuffled with other mixed pools.
    """
    display_name = "Mixed Pools - Dungeons"
    default = False

class OOTxMM_entrances_erMixedGrottos(Toggle):
    """
    If turned on, grottos will be shuffled with other mixed pools.
    """
    display_name = "Mixed Pools - Grottos"
    default = False

class OOTxMM_entrances_erMixedIndoors(Toggle):
    """
    If turned on, interiors will be shuffled with other mixed pools.
    """
    display_name = "Mixed Pools - Interiors"
    default = False

class OOTxMM_entrances_erMixedRegions(Toggle):
    """
    If turned on, regions will be shuffled with other mixed pools.
    """
    display_name = "Mixed Pools - Regions"
    default = False

class OOTxMM_entrances_erMixedOverworld(Toggle):
    """
    If turned on, overworld entrances will be shuffled with other mixed pools.
    """
    display_name = "Mixed Pools - Overworld"
    default = False

class OOTxMM_entrances_erSpawns(Choice):
    """
    Shuffle the starting positions of the player in OoT.
    - **none**
    - **child**
    - **adult**
    - **both**
    """
    display_name = "Spawn Shuffle"
    option_none = 0
    option_child = 1
    option_adult = 2
    option_both = 3
    default = option_none

class OOTxMM_entrances_erWallmasters(Choice):
    """
    Enables the ability for Wallmasters to take you to random locations within their own game or across both games, based on other entrance settings
    - **none**
    - **ownGame**
    - **full**
    """
    display_name = "Wallmaster Shuffle"
    option_none = 0
    option_ownGame = 1
    option_full = 2
    default = option_none

class OOTxMM_entrances_erWarps(Choice):
    """
    Allows separate shuffling of the warp songs and soaring spots. This setting is disabled if both are selected in "One-Ways Shuffle".
    - **none**: Warp songs and soaring spots are not shuffled.
    - **ootOnly**: Shuffles only OoT's warp songs among each other.
    - **mmOnly**: Shuffles only MM's soaring spots among each other.
    - **ownGame**: Shuffles both warp songs and soaring spots within their own game.
    - **full**: Shuffles both warp songs and soaring spots together.
    """
    display_name = "Warp Songs and Soaring Spots Shuffle"
    option_none = 0
    option_ootOnly = 1
    option_mmOnly = 2
    option_ownGame = 3
    option_full = 4
    default = option_none

class OOTxMM_entrances_erOneWays(Choice):
    """
    Enables the option of shuffling various one-way entrances.
    - **none**: One-way entrances are not shuffled.
    - **ownGame**: One-way entrances are only shuffled among their own game.
    - **full**: One-way entrances can be shuffled among both games.
    """
    display_name = "One-Ways Shuffle"
    option_none = 0
    option_ownGame = 1
    option_full = 2
    default = option_none

class OOTxMM_entrances_erOneWaysMajor(Toggle):
    """
    Shuffles the Gerudo Valley to Lake Hylia and Ikana Canyon to Southern Swamp entrances.
    """
    display_name = "Shuffle Standard One-Ways"
    default = False

class OOTxMM_entrances_erOneWaysIkana(Toggle):
    """
    Shuffles the one-way entrances in Ikana Castle among the others. This is the keg-blocked entrance and the block moved by the switch.
    """
    display_name = "Shuffle Ikana Castle One-Ways"
    default = False

class OOTxMM_entrances_erOneWaysSongs(Toggle):
    """
    Shuffles the warp songs from OoT among one-way entrances. This setting is disabled if the warp songs are shuffled with "Warp Songs and Soaring Spots Shuffle".
    """
    display_name = "Shuffle Warp Songs with One-Ways"
    default = False

class OOTxMM_entrances_erOneWaysStatues(Toggle):
    """
    Shuffles the soaring spots from MM among one-way entrances. This setting is disabled if the soaring spots are shuffled with "Warp Songs and Soaring Spots Shuffle".
    """
    display_name = "Shuffle Soaring Spots with One-Ways"
    default = False

class OOTxMM_entrances_erOneWaysOwls(Toggle):
    """
    Shuffle the two owl flights among one-way entrances.
    """
    display_name = "Shuffle Child Owl Flights"
    default = False

class OOTxMM_entrances_erOneWaysWoods(Toggle):
    """
    Shuffle the Lost Woods exits added by the "Alter Lost Woods Exits" setting among one-way entrances. 
    """
    display_name = "Shuffle Altered Lost Woods Exits"
    default = False

class OOTxMM_entrances_erOneWaysWaterVoids(Toggle):
    """
    Shuffle the Water Void points among one-way entrances. These can be found at:<br>- Zora Cape<br>- Great Bay Coast, south of the Pinnacle Rock entrance<br>- Great Bay Coast, north of the Pinnacle Rock entrance<br>- Pinnacle Rock
    """
    display_name = "Shuffle the Water Void Points in MM"
    default = False

class OOTxMM_entrances_erOneWaysAnywhere(Toggle):
    """
    Makes it so one-ways can take you to any place also shuffled.<br>This also affects warp songs and soaring spots if they are included in one-ways.
    """
    display_name = "Allow One-Ways to take you elsewhere than other one-ways"
    default = False

class OOTxMM_mainworld_mqDungeons(OptionSet):
    """
    Controls which OoT dungeons use the Master Quest layout.
    ['DT', 'DC', 'JJ', 'Forest', 'Fire', 'Water', 'Spirit', 'Shadow', 'BotW', 'IC', 'GTG', 'Ganon']
    """
    display_name = "Master Quest Dungeons"
    valid_keys = {
        'DT',
        'DC',
        'JJ',
        'Forest',
        'Fire',
        'Water',
        'Spirit',
        'Shadow',
        'BotW',
        'IC',
        'GTG',
        'Ganon',
    }
    default = valid_keys.copy()

class OOTxMM_mainworld_jpLayouts(OptionSet):
    """
    Choose which parts of Majora's Mask use their Japanese version, when different.
    ['DekuPalace', 'StoneTower', 'ST', 'GreatBayCoast']
    """
    display_name = "Majora's Mask JP Layouts"
    valid_keys = {
        'DekuPalace',
        'StoneTower',
        'ST',
        'GreatBayCoast',
    }
    default = valid_keys.copy()

class OOTxMM_mainqol_mmEasierLightblock(Toggle):
    """
    Makes the sun blocks slightly easier to remove.
    """
    display_name = "Easier Sun Blocks"
    default = False

class OOTxMM_mainqol_shadowFastBoat(Toggle):
    """
    Speeds up the Shadow Temple Boat before the last part of the dungeon
    """
    display_name = "Fast Shadow Temple Boat"
    default = False

class OOTxMM_mainqol_openMaskShop(Toggle):
    """
    Makes the Mask Shop in Market open during the night
    """
    display_name = "Open Mask Shop at night"
    default = False

class OOTxMM_mainqol_lenientSpikes(Toggle):
    """
    Goron Spikes can charge midair and keep their charge. Minimum speed for Goron Spikes is removed.
    """
    display_name = "Lenient Goron Spikes"
    default = True

class OOTxMM_mainqol_fastBunnyHood(Toggle):
    """
    Modifies the Bunny Hood in OoT to give a speed increase
    """
    display_name = "Fast Bunny Hood"
    default = True

class OOTxMM_mainqol_bowSlingshotBreakHives(Toggle):
    """
    Allows the Bow and Slingshot to break beehives in OoT, matching MM behavior
    """
    display_name = "Bow/Slingshot Break Hives"
    default = False

class OOTxMM_mainqol_critWiggleDisable(Toggle):
    """
    Disables the camera zoom-in and weird movements when low on health
    """
    display_name = "Disable Crit Wiggle"
    default = True

class OOTxMM_mainqol_fastMasks(Toggle):
    """
    Makes the mask transitions very fast
    """
    display_name = "Fast Form Transitions"
    default = False

class OOTxMM_mainqol_keepItemsReset(Toggle):
    """
    Keeps ammo & rupees through a cycle reset
    """
    display_name = "Keep Items on Cycle Reset"
    default = False

class OOTxMM_mainqol_keepBottlesReset(Toggle):
    """
    Keeps bottle contents through a cycle reset
    """
    display_name = "Keep Bottles on Cycle Reset"
    default = False

class OOTxMM_mainqol_mmSongOfDoubleTimeTimeSelector(Toggle):
    """
    Changes the Song of Double Time in MM to allow selecting time, similar to the Song of Double Time in Majoras Mask 3D.
    """
    display_name = "Song of Double Time - Time Selector"
    default = False

class OOTxMM_mainqol_autoInvert(Choice):
    """
    Auto-inverts time at the start of a cycle
    - **never**
    - **firstCycle**
    - **always**
    """
    display_name = "Auto-Invert Time (MM)"
    option_never = 0
    option_firstCycle = 1
    option_always = 2
    default = option_never

class OOTxMM_cutscenesmain_cutsceneSkipOoT(Toggle):
    """
    Skips a lot of mundane cutscenes in OoT, such as chests appearing, barred doors opening, etc.
    """
    display_name = "Skip Mundane Cutscenes (OoT)"
    default = False

class OOTxMM_cutscenesmain_cutsceneSkipMM(Toggle):
    """
    Skips a lot of mundane cutscenes in MM, such as chests appearing, barred doors opening, etc.
    """
    display_name = "Skip Mundane Cutscenes (MM)"
    default = False

class OOTxMM_cutscenesglitches_cutsceneGlitchOoT(Toggle):
    """
    Enables glitch-aiding cutscenes, such as Poe Sisters, Darunia, and some other chests/switches in dungeons.
    """
    display_name = "Glitch Aiding Cutscenes (OoT)"
    default = False

class OOTxMM_cutscenesbossesoot_cutsceneIntroGohma(Toggle):
    """
    Skips the intro cutscene for Gohma.
    """
    display_name = "Skip Gohma Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesoot_cutsceneIntroKingDodongo(Toggle):
    """
    Skips the intro cutscene for King Dodongo.
    """
    display_name = "Skip King Dodongo Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesoot_cutsceneIntroBarinade(Toggle):
    """
    Skips the intro cutscene for Barinade.
    """
    display_name = "Skip Barinade Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesoot_cutsceneIntroPhantomGanon(Toggle):
    """
    Skips the intro cutscene for Phantom Ganon.
    """
    display_name = "Skip Phantom Ganon Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesoot_cutsceneIntroVolvagia(Toggle):
    """
    Skips the intro cutscene for Volvagia.
    """
    display_name = "Skip Volvagia Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesoot_cutsceneIntroMorpha(Toggle):
    """
    Skips the intro cutscene for Morpha.
    """
    display_name = "Skip Morpha Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesoot_cutsceneIntroBongoBongo(Toggle):
    """
    Skips the intro cutscene for Bongo Bongo.
    """
    display_name = "Skip Bongo Bongo Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesoot_cutsceneIntroTwinrova(Toggle):
    """
    Skips the intro cutscene for Twinrova.
    """
    display_name = "Skip Twinrova Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesoot_cutsceneIntroGanondorf(Toggle):
    """
    Skips the intro cutscene for Ganondorf.
    """
    display_name = "Skip Ganondorf Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesmm_cutsceneIntroOdolwa(Toggle):
    """
    Skips the intro cutscene for Odolwa.
    """
    display_name = "Skip Odolwa Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesmm_cutsceneIntroGoht(Toggle):
    """
    Skips the intro cutscene for Goht.
    """
    display_name = "Skip Goht Intro Cutscene"
    default = True

class OOTxMM_cutscenesminibossesmm_cutsceneIntroWart(Toggle):
    """
    Skips the intro cutscene for Wart.
    """
    display_name = "Skip Wart Intro Cutscene"
    default = False

class OOTxMM_cutscenesbossesmm_cutsceneIntroGyorg(Toggle):
    """
    Skips the intro cutscene for Gyorg.
    """
    display_name = "Skip Gyorg Intro Cutscene"
    default = True

class OOTxMM_cutscenesminibossesmm_cutsceneIntroIgos(Toggle):
    """
    Skips the intro cutscene for Igos du Ikana.
    """
    display_name = "Skip Igos du Ikana Intro Cutscene"
    default = True

class OOTxMM_cutscenesminibossesmm_cutsceneIntroGomess(Toggle):
    """
    Skips the intro cutscene for Gomess.
    """
    display_name = "Skip Gomess Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesmm_cutsceneIntroTwinmold(Toggle):
    """
    Skips the intro cutscene for Twinmold.
    """
    display_name = "Skip Twinmold Intro Cutscene"
    default = True

class OOTxMM_cutscenesbossesmm_cutsceneIntroMajora(Toggle):
    """
    Skips the intro cutscene for Majora.
    """
    display_name = "Skip Majora Intro Cutscene"
    default = False


@dataclass
class OOTxMMOptions(PerGameCommonOptions):
    OOTxMM_main_goal: OOTxMM_main_goal
    OOTxMM_main_triforceGoal: OOTxMM_main_triforceGoal
    OOTxMM_main_triforcePieces: OOTxMM_main_triforcePieces
    OOTxMM_main_logic: OOTxMM_main_logic
    OOTxMM_main_itemPool: OOTxMM_main_itemPool
    OOTxMM_hints_probabilisticFoolish: OOTxMM_hints_probabilisticFoolish
    OOTxMM_mainshuffle_songs: OOTxMM_mainshuffle_songs
    OOTxMM_mainshuffle_goldSkulltulaTokens: OOTxMM_mainshuffle_goldSkulltulaTokens
    OOTxMM_mainshuffle_housesSkulltulaTokens: OOTxMM_mainshuffle_housesSkulltulaTokens
    OOTxMM_mainshuffle_tingleShuffle: OOTxMM_mainshuffle_tingleShuffle
    OOTxMM_mainshuffle_mapCompassShuffle: OOTxMM_mainshuffle_mapCompassShuffle
    OOTxMM_mainshuffle_smallKeyShuffleOot: OOTxMM_mainshuffle_smallKeyShuffleOot
    OOTxMM_mainshuffle_smallKeyShuffleMm: OOTxMM_mainshuffle_smallKeyShuffleMm
    OOTxMM_mainshuffle_smallKeyShuffleHideout: OOTxMM_mainshuffle_smallKeyShuffleHideout
    OOTxMM_mainshuffle_smallKeyShuffleChestGame: OOTxMM_mainshuffle_smallKeyShuffleChestGame
    OOTxMM_mainshuffle_bossKeyShuffleOot: OOTxMM_mainshuffle_bossKeyShuffleOot
    OOTxMM_mainshuffle_bossKeyShuffleMm: OOTxMM_mainshuffle_bossKeyShuffleMm
    OOTxMM_mainshuffle_smallKeyRingOot: OOTxMM_mainshuffle_smallKeyRingOot
    OOTxMM_mainshuffle_smallKeyRingMm: OOTxMM_mainshuffle_smallKeyRingMm
    OOTxMM_mainshuffle_silverRupeeShuffle: OOTxMM_mainshuffle_silverRupeeShuffle
    OOTxMM_mainshuffle_silverRupeePouches: OOTxMM_mainshuffle_silverRupeePouches
    OOTxMM_mainshuffle_townFairyShuffle: OOTxMM_mainshuffle_townFairyShuffle
    OOTxMM_mainshuffle_strayFairyChestShuffle: OOTxMM_mainshuffle_strayFairyChestShuffle
    OOTxMM_mainshuffle_strayFairyOtherShuffle: OOTxMM_mainshuffle_strayFairyOtherShuffle
    OOTxMM_mainshuffle_ganonBossKey: OOTxMM_mainshuffle_ganonBossKey
    OOTxMM_mainshuffle_dungeonRewardShuffle: OOTxMM_mainshuffle_dungeonRewardShuffle
    OOTxMM_mainshuffle_scrubShuffleOot: OOTxMM_mainshuffle_scrubShuffleOot
    OOTxMM_mainshuffle_scrubShuffleMm: OOTxMM_mainshuffle_scrubShuffleMm
    OOTxMM_mainshuffle_cowShuffleOot: OOTxMM_mainshuffle_cowShuffleOot
    OOTxMM_mainshuffle_cowShuffleMm: OOTxMM_mainshuffle_cowShuffleMm
    OOTxMM_mainshuffle_shopShuffleOot: OOTxMM_mainshuffle_shopShuffleOot
    OOTxMM_mainshuffle_shopShuffleMm: OOTxMM_mainshuffle_shopShuffleMm
    OOTxMM_mainshuffle_owlShuffle: OOTxMM_mainshuffle_owlShuffle
    OOTxMM_mainshuffle_shufflePotsOot: OOTxMM_mainshuffle_shufflePotsOot
    OOTxMM_mainshuffle_shufflePotsMm: OOTxMM_mainshuffle_shufflePotsMm
    OOTxMM_mainshuffle_shuffleCratesOot: OOTxMM_mainshuffle_shuffleCratesOot
    OOTxMM_mainshuffle_shuffleCratesMm: OOTxMM_mainshuffle_shuffleCratesMm
    OOTxMM_mainshuffle_shuffleBarrelsMm: OOTxMM_mainshuffle_shuffleBarrelsMm
    OOTxMM_mainshuffle_shuffleHivesOot: OOTxMM_mainshuffle_shuffleHivesOot
    OOTxMM_mainshuffle_shuffleHivesMm: OOTxMM_mainshuffle_shuffleHivesMm
    OOTxMM_mainshuffle_shuffleGrassOot: OOTxMM_mainshuffle_shuffleGrassOot
    OOTxMM_mainshuffle_shuffleRocksOot: OOTxMM_mainshuffle_shuffleRocksOot
    OOTxMM_mainshuffle_shuffleRocksMm: OOTxMM_mainshuffle_shuffleRocksMm
    OOTxMM_mainshuffle_shuffleGrassMm: OOTxMM_mainshuffle_shuffleGrassMm
    OOTxMM_mainshuffle_shuffleTFGrassMm: OOTxMM_mainshuffle_shuffleTFGrassMm
    OOTxMM_mainshuffle_shuffleTreesOot: OOTxMM_mainshuffle_shuffleTreesOot
    OOTxMM_mainshuffle_shuffleTreesMm: OOTxMM_mainshuffle_shuffleTreesMm
    OOTxMM_mainshuffle_shuffleBushOot: OOTxMM_mainshuffle_shuffleBushOot
    OOTxMM_mainshuffle_shuffleBushMm: OOTxMM_mainshuffle_shuffleBushMm
    OOTxMM_mainshuffle_shuffleSoilOot: OOTxMM_mainshuffle_shuffleSoilOot
    OOTxMM_mainshuffle_shuffleSoilMm: OOTxMM_mainshuffle_shuffleSoilMm
    OOTxMM_mainshuffle_shuffleFreeRupeesOot: OOTxMM_mainshuffle_shuffleFreeRupeesOot
    OOTxMM_mainshuffle_shuffleFreeRupeesMm: OOTxMM_mainshuffle_shuffleFreeRupeesMm
    OOTxMM_mainshuffle_shuffleFreeHeartsOot: OOTxMM_mainshuffle_shuffleFreeHeartsOot
    OOTxMM_mainshuffle_shuffleFreeHeartsMm: OOTxMM_mainshuffle_shuffleFreeHeartsMm
    OOTxMM_mainshuffle_shuffleGossipFairiesOot: OOTxMM_mainshuffle_shuffleGossipFairiesOot
    OOTxMM_mainshuffle_shuffleGossipBigFairiesOot: OOTxMM_mainshuffle_shuffleGossipBigFairiesOot
    OOTxMM_mainshuffle_shuffleGossipFairiesMm: OOTxMM_mainshuffle_shuffleGossipFairiesMm
    OOTxMM_mainshuffle_shuffleGossipBigFairiesMm: OOTxMM_mainshuffle_shuffleGossipBigFairiesMm
    OOTxMM_mainshuffle_shuffleWonderItemsOot: OOTxMM_mainshuffle_shuffleWonderItemsOot
    OOTxMM_mainshuffle_shuffleWonderItemsMm: OOTxMM_mainshuffle_shuffleWonderItemsMm
    OOTxMM_mainshuffle_shuffleSnowballsMm: OOTxMM_mainshuffle_shuffleSnowballsMm
    OOTxMM_mainshuffle_shuffleButterfliesOot: OOTxMM_mainshuffle_shuffleButterfliesOot
    OOTxMM_mainshuffle_shuffleButterfliesMm: OOTxMM_mainshuffle_shuffleButterfliesMm
    OOTxMM_mainshuffle_shuffleBouldersOot: OOTxMM_mainshuffle_shuffleBouldersOot
    OOTxMM_mainshuffle_shuffleBouldersMm: OOTxMM_mainshuffle_shuffleBouldersMm
    OOTxMM_mainshuffle_shuffleRedBouldersOot: OOTxMM_mainshuffle_shuffleRedBouldersOot
    OOTxMM_mainshuffle_shuffleRedBouldersMm: OOTxMM_mainshuffle_shuffleRedBouldersMm
    OOTxMM_mainshuffle_shuffleSilverBouldersOot: OOTxMM_mainshuffle_shuffleSilverBouldersOot
    OOTxMM_mainshuffle_shuffleFrogsRupeesOot: OOTxMM_mainshuffle_shuffleFrogsRupeesOot
    OOTxMM_mainshuffle_shuffleLotteryMm: OOTxMM_mainshuffle_shuffleLotteryMm
    OOTxMM_mainshuffle_shuffleIciclesOot: OOTxMM_mainshuffle_shuffleIciclesOot
    OOTxMM_mainshuffle_shuffleIciclesMm: OOTxMM_mainshuffle_shuffleIciclesMm
    OOTxMM_mainshuffle_shuffleRedIceOot: OOTxMM_mainshuffle_shuffleRedIceOot
    OOTxMM_mainshuffle_shuffleOcarinasOot: OOTxMM_mainshuffle_shuffleOcarinasOot
    OOTxMM_mainshuffle_shuffleMasterSword: OOTxMM_mainshuffle_shuffleMasterSword
    OOTxMM_mainshuffle_shuffleGerudoCard: OOTxMM_mainshuffle_shuffleGerudoCard
    OOTxMM_mainshuffle_shuffleSkulltulaFinalReward: OOTxMM_mainshuffle_shuffleSkulltulaFinalReward
    OOTxMM_mainshuffle_shuffleMaskTrades: OOTxMM_mainshuffle_shuffleMaskTrades
    OOTxMM_mainshuffle_shuffleMerchantsOot: OOTxMM_mainshuffle_shuffleMerchantsOot
    OOTxMM_mainshuffle_shuffleMerchantsMm: OOTxMM_mainshuffle_shuffleMerchantsMm
    OOTxMM_mainshuffle_pondFishShuffle: OOTxMM_mainshuffle_pondFishShuffle
    OOTxMM_mainshuffle_divingGameRupeeShuffle: OOTxMM_mainshuffle_divingGameRupeeShuffle
    OOTxMM_mainshuffle_fairyFountainFairyShuffleOot: OOTxMM_mainshuffle_fairyFountainFairyShuffleOot
    OOTxMM_mainshuffle_fairyFountainFairyShuffleMm: OOTxMM_mainshuffle_fairyFountainFairyShuffleMm
    OOTxMM_mainshuffle_fairySpotShuffleOot: OOTxMM_mainshuffle_fairySpotShuffleOot
    OOTxMM_mainshuffle_eggShuffle: OOTxMM_mainshuffle_eggShuffle
    OOTxMM_mainprices_priceOotShops: OOTxMM_mainprices_priceOotShops
    OOTxMM_mainprices_priceOotScrubs: OOTxMM_mainprices_priceOotScrubs
    OOTxMM_mainprices_priceOotMerchants: OOTxMM_mainprices_priceOotMerchants
    OOTxMM_mainprices_priceMmShops: OOTxMM_mainprices_priceMmShops
    OOTxMM_mainprices_priceMmTingle: OOTxMM_mainprices_priceMmTingle
    OOTxMM_mainevents_songEventsShuffleOot: OOTxMM_mainevents_songEventsShuffleOot
    OOTxMM_mainevents_songEventsShuffleMm: OOTxMM_mainevents_songEventsShuffleMm
    OOTxMM_mainevents_ganonTrials: OOTxMM_mainevents_ganonTrials
    OOTxMM_mainevents_moonCrash: OOTxMM_mainevents_moonCrash
    OOTxMM_mainevents_startingAgeOot: OOTxMM_mainevents_startingAgeOot
    OOTxMM_mainevents_startingAgeMm: OOTxMM_mainevents_startingAgeMm
    OOTxMM_mainevents_timeTravelSword: OOTxMM_mainevents_timeTravelSword
    OOTxMM_mainevents_doorOfTime: OOTxMM_mainevents_doorOfTime
    OOTxMM_mainevents_ageChange: OOTxMM_mainevents_ageChange
    OOTxMM_mainevents_dekuTree: OOTxMM_mainevents_dekuTree
    OOTxMM_mainevents_openDungeonsOot: OOTxMM_mainevents_openDungeonsOot
    OOTxMM_mainevents_openDungeonsMm: OOTxMM_mainevents_openDungeonsMm
    OOTxMM_mainevents_clearStateDungeonsMm: OOTxMM_mainevents_clearStateDungeonsMm
    OOTxMM_mainevents_beneathWell: OOTxMM_mainevents_beneathWell
    OOTxMM_mainevents_kakarikoGate: OOTxMM_mainevents_kakarikoGate
    OOTxMM_mainevents_openZdShortcut: OOTxMM_mainevents_openZdShortcut
    OOTxMM_mainevents_zoraKing: OOTxMM_mainevents_zoraKing
    OOTxMM_mainevents_gerudoFortress: OOTxMM_mainevents_gerudoFortress
    OOTxMM_mainevents_skipZelda: OOTxMM_mainevents_skipZelda
    OOTxMM_mainevents_openMoon: OOTxMM_mainevents_openMoon
    OOTxMM_mainevents_moon: OOTxMM_mainevents_moon
    OOTxMM_mainevents_lacs: OOTxMM_mainevents_lacs
    OOTxMM_mainevents_rainbowBridge: OOTxMM_mainevents_rainbowBridge
    OOTxMM_mainevents_majoraChild: OOTxMM_mainevents_majoraChild
    OOTxMM_mainevents_bossWarpPads: OOTxMM_mainevents_bossWarpPads
    OOTxMM_mainevents_regionState: OOTxMM_mainevents_regionState
    OOTxMM_mainevents_freeScarecrowOot: OOTxMM_mainevents_freeScarecrowOot
    OOTxMM_mainevents_freeScarecrowMm: OOTxMM_mainevents_freeScarecrowMm
    OOTxMM_mainevents_strayFairyRewardCount: OOTxMM_mainevents_strayFairyRewardCount
    OOTxMM_mainevents_preCompletedDungeons: OOTxMM_mainevents_preCompletedDungeons
    OOTxMM_mainevents_preCompletedDungeonsMajor: OOTxMM_mainevents_preCompletedDungeonsMajor
    OOTxMM_mainevents_preCompletedDungeonsStones: OOTxMM_mainevents_preCompletedDungeonsStones
    OOTxMM_mainevents_preCompletedDungeonsMedallions: OOTxMM_mainevents_preCompletedDungeonsMedallions
    OOTxMM_mainevents_preCompletedDungeonsRemains: OOTxMM_mainevents_preCompletedDungeonsRemains
    OOTxMM_mainevents_ootPreplantedBeans: OOTxMM_mainevents_ootPreplantedBeans
    OOTxMM_mainevents_mmPreActivatedOwls: OOTxMM_mainevents_mmPreActivatedOwls
    OOTxMM_maincross_crossAge: OOTxMM_maincross_crossAge
    OOTxMM_maincross_crossGameFw: OOTxMM_maincross_crossGameFw
    OOTxMM_maincamc_csmc: OOTxMM_maincamc_csmc
    OOTxMM_maincamc_csmcHearts: OOTxMM_maincamc_csmcHearts
    OOTxMM_maincamc_csmcMapCompass: OOTxMM_maincamc_csmcMapCompass
    OOTxMM_maincamc_csmcSkulltula: OOTxMM_maincamc_csmcSkulltula
    OOTxMM_maincamc_csmcCow: OOTxMM_maincamc_csmcCow
    OOTxMM_mainmisc_blastMaskCooldown: OOTxMM_mainmisc_blastMaskCooldown
    OOTxMM_mainnologic_clockSpeed: OOTxMM_mainnologic_clockSpeed
    OOTxMM_mainnologic_fierceDeityAnywhere: OOTxMM_mainnologic_fierceDeityAnywhere
    OOTxMM_mainmisc_hookshotAnywhereOot: OOTxMM_mainmisc_hookshotAnywhereOot
    OOTxMM_mainmisc_hookshotAnywhereMm: OOTxMM_mainmisc_hookshotAnywhereMm
    OOTxMM_mainmisc_climbMostSurfacesOot: OOTxMM_mainmisc_climbMostSurfacesOot
    OOTxMM_mainnologic_climbMostSurfacesMm: OOTxMM_mainnologic_climbMostSurfacesMm
    OOTxMM_mainmisc_restoreBrokenActors: OOTxMM_mainmisc_restoreBrokenActors
    OOTxMM_mainmisc_alterLostWoodsExits: OOTxMM_mainmisc_alterLostWoodsExits
    OOTxMM_mainmisc_voidWarpMm: OOTxMM_mainmisc_voidWarpMm
    OOTxMM_mainnologic_damageMultiplierOot: OOTxMM_mainnologic_damageMultiplierOot
    OOTxMM_mainnologic_damageMultiplierMm: OOTxMM_mainnologic_damageMultiplierMm
    OOTxMM_mainnologic_mmStyleAirMovementOot: OOTxMM_mainnologic_mmStyleAirMovementOot
    OOTxMM_mainnologic_ootHyperEnemies: OOTxMM_mainnologic_ootHyperEnemies
    OOTxMM_mainnologic_mmHyperEnemies: OOTxMM_mainnologic_mmHyperEnemies
    OOTxMM_itemsprogressive_progressiveShieldsOot: OOTxMM_itemsprogressive_progressiveShieldsOot
    OOTxMM_itemsprogressive_progressiveSwordsOot: OOTxMM_itemsprogressive_progressiveSwordsOot
    OOTxMM_itemsprogressive_progressiveShieldsMm: OOTxMM_itemsprogressive_progressiveShieldsMm
    OOTxMM_itemsprogressive_progressiveGFS: OOTxMM_itemsprogressive_progressiveGFS
    OOTxMM_itemsprogressive_progressiveGoronLullabyMm: OOTxMM_itemsprogressive_progressiveGoronLullabyMm
    OOTxMM_itemsprogressive_progressiveGoronLullabyOot: OOTxMM_itemsprogressive_progressiveGoronLullabyOot
    OOTxMM_itemsprogressive_progressiveClocks: OOTxMM_itemsprogressive_progressiveClocks
    OOTxMM_itemsextensionsgeneral_fillWallets: OOTxMM_itemsextensionsgeneral_fillWallets
    OOTxMM_itemsextensionsgeneral_bottleContentShuffle: OOTxMM_itemsextensionsgeneral_bottleContentShuffle
    OOTxMM_itemsextensionscrossGameitems_stoneAgonyMm: OOTxMM_itemsextensionscrossGameitems_stoneAgonyMm
    OOTxMM_itemsextensionscrossGameitems_sticksNutsUpgradesMm: OOTxMM_itemsextensionscrossGameitems_sticksNutsUpgradesMm
    OOTxMM_itemsextensionsgeneral_sticksNutsUpgradesInitial: OOTxMM_itemsextensionsgeneral_sticksNutsUpgradesInitial
    OOTxMM_itemsextensionscrossGameitems_fairyOcarinaMm: OOTxMM_itemsextensionscrossGameitems_fairyOcarinaMm
    OOTxMM_itemsextensionsoot_blueFireArrows: OOTxMM_itemsextensionsoot_blueFireArrows
    OOTxMM_itemsextensionsoot_iceArrowPlatformsOot: OOTxMM_itemsextensionsoot_iceArrowPlatformsOot
    OOTxMM_itemsextensionsoot_sunlightArrows: OOTxMM_itemsextensionsoot_sunlightArrows
    OOTxMM_itemsextensionscrossGameitems_shortHookshotMm: OOTxMM_itemsextensionscrossGameitems_shortHookshotMm
    OOTxMM_itemsextensionsgeneral_bronzeScale: OOTxMM_itemsextensionsgeneral_bronzeScale
    OOTxMM_itemsextensionsgeneral_childWallets: OOTxMM_itemsextensionsgeneral_childWallets
    OOTxMM_itemsextensionsgeneral_colossalWallets: OOTxMM_itemsextensionsgeneral_colossalWallets
    OOTxMM_itemsextensionsgeneral_bottomlessWallets: OOTxMM_itemsextensionsgeneral_bottomlessWallets
    OOTxMM_itemsextensionsgeneral_rupeeScaling: OOTxMM_itemsextensionsgeneral_rupeeScaling
    OOTxMM_itemsextensionssystems_skeletonKeyOot: OOTxMM_itemsextensionssystems_skeletonKeyOot
    OOTxMM_itemsextensionssystems_skeletonKeyMm: OOTxMM_itemsextensionssystems_skeletonKeyMm
    OOTxMM_itemsextensionsoot_magicalRupee: OOTxMM_itemsextensionsoot_magicalRupee
    OOTxMM_itemsextensionsmm_transcendentFairy: OOTxMM_itemsextensionsmm_transcendentFairy
    OOTxMM_itemsextensionssystems_platinumTokenOot: OOTxMM_itemsextensionssystems_platinumTokenOot
    OOTxMM_itemsextensionssystems_platinumTokenMm: OOTxMM_itemsextensionssystems_platinumTokenMm
    OOTxMM_itemsextensionssystems_bombchuBehaviorOot: OOTxMM_itemsextensionssystems_bombchuBehaviorOot
    OOTxMM_itemsextensionssystems_bombchuBehaviorMm: OOTxMM_itemsextensionssystems_bombchuBehaviorMm
    OOTxMM_itemsextensionscrossGameitems_spellFireMm: OOTxMM_itemsextensionscrossGameitems_spellFireMm
    OOTxMM_itemsextensionscrossGameitems_spellWindMm: OOTxMM_itemsextensionscrossGameitems_spellWindMm
    OOTxMM_itemsextensionscrossGameitems_spellLoveMm: OOTxMM_itemsextensionscrossGameitems_spellLoveMm
    OOTxMM_itemsextensionscrossGameitems_bootsIronMm: OOTxMM_itemsextensionscrossGameitems_bootsIronMm
    OOTxMM_itemsextensionscrossGameitems_bootsHoverMm: OOTxMM_itemsextensionscrossGameitems_bootsHoverMm
    OOTxMM_itemsextensionscrossGameitems_tunicGoronMm: OOTxMM_itemsextensionscrossGameitems_tunicGoronMm
    OOTxMM_itemsextensionscrossGameitems_tunicZoraMm: OOTxMM_itemsextensionscrossGameitems_tunicZoraMm
    OOTxMM_itemsextensionscrossGameitems_scalesMm: OOTxMM_itemsextensionscrossGameitems_scalesMm
    OOTxMM_itemsextensionscrossGameitems_strengthMm: OOTxMM_itemsextensionscrossGameitems_strengthMm
    OOTxMM_itemsextensionsmm_kegStrength3: OOTxMM_itemsextensionsmm_kegStrength3
    OOTxMM_itemsextensionscrossGameitems_hammerMm: OOTxMM_itemsextensionscrossGameitems_hammerMm
    OOTxMM_itemsextensionscrossGameitems_boomerangMm: OOTxMM_itemsextensionscrossGameitems_boomerangMm
    OOTxMM_itemsextensionscrossGameitems_gfsOot: OOTxMM_itemsextensionscrossGameitems_gfsOot
    OOTxMM_itemsextensionscrossGameitems_slingshotMm: OOTxMM_itemsextensionscrossGameitems_slingshotMm
    OOTxMM_itemsextensionscrossGameitems_spinUpgradeOot: OOTxMM_itemsextensionscrossGameitems_spinUpgradeOot
    OOTxMM_itemsextensionscrossGameitems_extraChildSwordsOot: OOTxMM_itemsextensionscrossGameitems_extraChildSwordsOot
    OOTxMM_itemsextensionscrossGameitems_dekuShieldMm: OOTxMM_itemsextensionscrossGameitems_dekuShieldMm
    OOTxMM_itemsextensionscrossGamemasks_blastMaskOot: OOTxMM_itemsextensionscrossGamemasks_blastMaskOot
    OOTxMM_itemsextensionscrossGamemasks_stoneMaskOot: OOTxMM_itemsextensionscrossGamemasks_stoneMaskOot
    OOTxMM_itemsextensionscrossGamemasks_kamaroMaskOot: OOTxMM_itemsextensionscrossGamemasks_kamaroMaskOot
    OOTxMM_itemsextensionscrossGamemasks_gerudoMaskMm: OOTxMM_itemsextensionscrossGamemasks_gerudoMaskMm
    OOTxMM_itemsextensionscrossGamemasks_skullMaskMm: OOTxMM_itemsextensionscrossGamemasks_skullMaskMm
    OOTxMM_itemsextensionscrossGamemasks_spookyMaskMm: OOTxMM_itemsextensionscrossGamemasks_spookyMaskMm
    OOTxMM_itemsextensionsmm_adultMaskMm: OOTxMM_itemsextensionsmm_adultMaskMm
    OOTxMM_itemsextensionscrossGamesongs_elegyOot: OOTxMM_itemsextensionscrossGamesongs_elegyOot
    OOTxMM_itemsextensionscrossGamesongs_songSoaringOot: OOTxMM_itemsextensionscrossGamesongs_songSoaringOot
    OOTxMM_itemsextensionscrossGamesongs_songHealingOot: OOTxMM_itemsextensionscrossGamesongs_songHealingOot
    OOTxMM_itemsextensionscrossGamesongs_songAwakeningOot: OOTxMM_itemsextensionscrossGamesongs_songAwakeningOot
    OOTxMM_itemsextensionscrossGamesongs_songGoronOot: OOTxMM_itemsextensionscrossGamesongs_songGoronOot
    OOTxMM_itemsextensionscrossGamesongs_songZoraOot: OOTxMM_itemsextensionscrossGamesongs_songZoraOot
    OOTxMM_itemsextensionscrossGamesongs_songOrderOot: OOTxMM_itemsextensionscrossGamesongs_songOrderOot
    OOTxMM_itemsextensionscrossGamesongs_songSunMm: OOTxMM_itemsextensionscrossGamesongs_songSunMm
    OOTxMM_itemsextensionscrossGamesongs_songZeldaLullabyMm: OOTxMM_itemsextensionscrossGamesongs_songZeldaLullabyMm
    OOTxMM_itemsextensionscrossGamesongs_songSariasMm: OOTxMM_itemsextensionscrossGamesongs_songSariasMm
    OOTxMM_itemsextensionscrossGamesongs_songMinuetMm: OOTxMM_itemsextensionscrossGamesongs_songMinuetMm
    OOTxMM_itemsextensionscrossGamesongs_songBoleroMm: OOTxMM_itemsextensionscrossGamesongs_songBoleroMm
    OOTxMM_itemsextensionscrossGamesongs_songSerenadeMm: OOTxMM_itemsextensionscrossGamesongs_songSerenadeMm
    OOTxMM_itemsextensionscrossGamesongs_songRequiemMm: OOTxMM_itemsextensionscrossGamesongs_songRequiemMm
    OOTxMM_itemsextensionscrossGamesongs_songNocturneMm: OOTxMM_itemsextensionscrossGamesongs_songNocturneMm
    OOTxMM_itemsextensionscrossGamesongs_songPreludeMm: OOTxMM_itemsextensionscrossGamesongs_songPreludeMm
    OOTxMM_itemsextensionscrossGameitems_powderKegOot: OOTxMM_itemsextensionscrossGameitems_powderKegOot
    OOTxMM_itemsextensionscrossGameitems_extraBottlesOot: OOTxMM_itemsextensionscrossGameitems_extraBottlesOot
    OOTxMM_itemsextensionssystems_ocarinaButtonsShuffleOot: OOTxMM_itemsextensionssystems_ocarinaButtonsShuffleOot
    OOTxMM_itemsextensionssystems_ocarinaButtonsShuffleMm: OOTxMM_itemsextensionssystems_ocarinaButtonsShuffleMm
    OOTxMM_itemsextensionssystems_shovelOot: OOTxMM_itemsextensionssystems_shovelOot
    OOTxMM_itemsextensionssystems_shovelMm: OOTxMM_itemsextensionssystems_shovelMm
    OOTxMM_itemsextensionssystems_soulsEnemyOot: OOTxMM_itemsextensionssystems_soulsEnemyOot
    OOTxMM_itemsextensionssystems_soulsEnemyMm: OOTxMM_itemsextensionssystems_soulsEnemyMm
    OOTxMM_itemsextensionssystems_soulsBossOot: OOTxMM_itemsextensionssystems_soulsBossOot
    OOTxMM_itemsextensionssystems_soulsBossMm: OOTxMM_itemsextensionssystems_soulsBossMm
    OOTxMM_itemsextensionssystems_soulsNpcOot: OOTxMM_itemsextensionssystems_soulsNpcOot
    OOTxMM_itemsextensionssystems_soulsNpcMm: OOTxMM_itemsextensionssystems_soulsNpcMm
    OOTxMM_itemsextensionssystems_soulsAnimalOot: OOTxMM_itemsextensionssystems_soulsAnimalOot
    OOTxMM_itemsextensionssystems_soulsAnimalMm: OOTxMM_itemsextensionssystems_soulsAnimalMm
    OOTxMM_itemsextensionssystems_soulsMiscOot: OOTxMM_itemsextensionssystems_soulsMiscOot
    OOTxMM_itemsextensionssystems_soulsMiscMm: OOTxMM_itemsextensionssystems_soulsMiscMm
    OOTxMM_itemsextensionssystems_rustyKeysOot: OOTxMM_itemsextensionssystems_rustyKeysOot
    OOTxMM_itemsextensionssystems_rustyKeysMm: OOTxMM_itemsextensionssystems_rustyKeysMm
    OOTxMM_itemsextensionssystems_clocksMm: OOTxMM_itemsextensionssystems_clocksMm
    OOTxMM_itemsextensionssystems_clocksOot: OOTxMM_itemsextensionssystems_clocksOot
    OOTxMM_itemsextensionsmm_menuNotebook: OOTxMM_itemsextensionsmm_menuNotebook
    OOTxMM_itemsextensionscoins_coins: OOTxMM_itemsextensionscoins_coins
    OOTxMM_itemsextensionscoins_coinsRed: OOTxMM_itemsextensionscoins_coinsRed
    OOTxMM_itemsextensionscoins_coinsGreen: OOTxMM_itemsextensionscoins_coinsGreen
    OOTxMM_itemsextensionscoins_coinsBlue: OOTxMM_itemsextensionscoins_coinsBlue
    OOTxMM_itemsextensionscoins_coinsYellow: OOTxMM_itemsextensionscoins_coinsYellow
    OOTxMM_itemsextensionstraps_trapIce: OOTxMM_itemsextensionstraps_trapIce
    OOTxMM_itemsextensionstraps_trapFire: OOTxMM_itemsextensionstraps_trapFire
    OOTxMM_itemsextensionstraps_trapShock: OOTxMM_itemsextensionstraps_trapShock
    OOTxMM_itemsextensionstraps_trapDrain: OOTxMM_itemsextensionstraps_trapDrain
    OOTxMM_itemsextensionstraps_trapAntiMagic: OOTxMM_itemsextensionstraps_trapAntiMagic
    OOTxMM_itemsextensionstraps_trapKnockback: OOTxMM_itemsextensionstraps_trapKnockback
    OOTxMM_itemsextensionstraps_trapRupoor: OOTxMM_itemsextensionstraps_trapRupoor
    OOTxMM_itemsextensionstraps_cloakTraps: OOTxMM_itemsextensionstraps_cloakTraps
    OOTxMM_itemsextensionstraps_trapsQuantity: OOTxMM_itemsextensionstraps_trapsQuantity
    OOTxMM_main_trapsLink: OOTxMM_main_trapsLink
    OOTxMM_itemsextensionsoot_songOfDoubleTimeOot: OOTxMM_itemsextensionsoot_songOfDoubleTimeOot
    OOTxMM_itemsextensionscrossGameitems_sharedStoneAgony: OOTxMM_itemsextensionscrossGameitems_sharedStoneAgony
    OOTxMM_itemsextensionscrossGameitems_sharedSpinUpgrade: OOTxMM_itemsextensionscrossGameitems_sharedSpinUpgrade
    OOTxMM_itemsextensionscrossGameitems_sharedNutsSticks: OOTxMM_itemsextensionscrossGameitems_sharedNutsSticks
    OOTxMM_itemsextensionsshared_sharedBows: OOTxMM_itemsextensionsshared_sharedBows
    OOTxMM_itemsextensionsshared_sharedBombBags: OOTxMM_itemsextensionsshared_sharedBombBags
    OOTxMM_itemsextensionsshared_sharedMagic: OOTxMM_itemsextensionsshared_sharedMagic
    OOTxMM_itemsextensionsshared_sharedMagicArrowFire: OOTxMM_itemsextensionsshared_sharedMagicArrowFire
    OOTxMM_itemsextensionsshared_sharedMagicArrowIce: OOTxMM_itemsextensionsshared_sharedMagicArrowIce
    OOTxMM_itemsextensionsshared_sharedMagicArrowLight: OOTxMM_itemsextensionsshared_sharedMagicArrowLight
    OOTxMM_itemsextensionsshared_sharedSongEpona: OOTxMM_itemsextensionsshared_sharedSongEpona
    OOTxMM_itemsextensionsshared_sharedSongStorms: OOTxMM_itemsextensionsshared_sharedSongStorms
    OOTxMM_itemsextensionsshared_sharedSongTime: OOTxMM_itemsextensionsshared_sharedSongTime
    OOTxMM_itemsextensionscrossGamesongs_sharedSongSun: OOTxMM_itemsextensionscrossGamesongs_sharedSongSun
    OOTxMM_itemsextensionscrossGameitems_sharedHookshot: OOTxMM_itemsextensionscrossGameitems_sharedHookshot
    OOTxMM_itemsextensionsshared_sharedLens: OOTxMM_itemsextensionsshared_sharedLens
    OOTxMM_itemsextensionscrossGameitems_sharedOcarina: OOTxMM_itemsextensionscrossGameitems_sharedOcarina
    OOTxMM_itemsextensionsshared_sharedMaskGoron: OOTxMM_itemsextensionsshared_sharedMaskGoron
    OOTxMM_itemsextensionsshared_sharedMaskZora: OOTxMM_itemsextensionsshared_sharedMaskZora
    OOTxMM_itemsextensionsshared_sharedMaskBunny: OOTxMM_itemsextensionsshared_sharedMaskBunny
    OOTxMM_itemsextensionsshared_sharedMaskKeaton: OOTxMM_itemsextensionsshared_sharedMaskKeaton
    OOTxMM_itemsextensionsshared_sharedMaskTruth: OOTxMM_itemsextensionsshared_sharedMaskTruth
    OOTxMM_itemsextensionscrossGamemasks_sharedMaskBlast: OOTxMM_itemsextensionscrossGamemasks_sharedMaskBlast
    OOTxMM_itemsextensionscrossGamemasks_sharedMaskStone: OOTxMM_itemsextensionscrossGamemasks_sharedMaskStone
    OOTxMM_itemsextensionscrossGamemasks_sharedMaskKamaro: OOTxMM_itemsextensionscrossGamemasks_sharedMaskKamaro
    OOTxMM_itemsextensionscrossGamesongs_sharedSongElegy: OOTxMM_itemsextensionscrossGamesongs_sharedSongElegy
    OOTxMM_itemsextensionscrossGamesongs_sharedSongHealing: OOTxMM_itemsextensionscrossGamesongs_sharedSongHealing
    OOTxMM_itemsextensionscrossGamesongs_sharedSongSoaring: OOTxMM_itemsextensionscrossGamesongs_sharedSongSoaring
    OOTxMM_itemsextensionscrossGamesongs_sharedSongAwakening: OOTxMM_itemsextensionscrossGamesongs_sharedSongAwakening
    OOTxMM_itemsextensionscrossGamesongs_sharedSongGoron: OOTxMM_itemsextensionscrossGamesongs_sharedSongGoron
    OOTxMM_itemsextensionscrossGamesongs_sharedSongZora: OOTxMM_itemsextensionscrossGamesongs_sharedSongZora
    OOTxMM_itemsextensionscrossGamesongs_sharedSongOrder: OOTxMM_itemsextensionscrossGamesongs_sharedSongOrder
    OOTxMM_itemsextensionscrossGamesongs_sharedSongZeldaLullaby: OOTxMM_itemsextensionscrossGamesongs_sharedSongZeldaLullaby
    OOTxMM_itemsextensionscrossGamesongs_sharedSongSarias: OOTxMM_itemsextensionscrossGamesongs_sharedSongSarias
    OOTxMM_itemsextensionscrossGamesongs_sharedSongMinuet: OOTxMM_itemsextensionscrossGamesongs_sharedSongMinuet
    OOTxMM_itemsextensionscrossGamesongs_sharedSongBolero: OOTxMM_itemsextensionscrossGamesongs_sharedSongBolero
    OOTxMM_itemsextensionscrossGamesongs_sharedSongSerenade: OOTxMM_itemsextensionscrossGamesongs_sharedSongSerenade
    OOTxMM_itemsextensionscrossGamesongs_sharedSongRequiem: OOTxMM_itemsextensionscrossGamesongs_sharedSongRequiem
    OOTxMM_itemsextensionscrossGamesongs_sharedSongNocturne: OOTxMM_itemsextensionscrossGamesongs_sharedSongNocturne
    OOTxMM_itemsextensionscrossGamesongs_sharedSongPrelude: OOTxMM_itemsextensionscrossGamesongs_sharedSongPrelude
    OOTxMM_itemsextensionscrossGameitems_sharedPowderKeg: OOTxMM_itemsextensionscrossGameitems_sharedPowderKeg
    OOTxMM_itemsextensionsshared_sharedWallets: OOTxMM_itemsextensionsshared_sharedWallets
    OOTxMM_itemsextensionsshared_sharedHealth: OOTxMM_itemsextensionsshared_sharedHealth
    OOTxMM_itemsextensionscrossGameitems_sharedSwords: OOTxMM_itemsextensionscrossGameitems_sharedSwords
    OOTxMM_itemsextensionscrossGameitems_sharedShields: OOTxMM_itemsextensionscrossGameitems_sharedShields
    OOTxMM_itemsextensionssystems_sharedSoulsEnemy: OOTxMM_itemsextensionssystems_sharedSoulsEnemy
    OOTxMM_itemsextensionssystems_sharedSoulsNpc: OOTxMM_itemsextensionssystems_sharedSoulsNpc
    OOTxMM_itemsextensionssystems_sharedSoulsAnimal: OOTxMM_itemsextensionssystems_sharedSoulsAnimal
    OOTxMM_itemsextensionssystems_sharedSoulsMisc: OOTxMM_itemsextensionssystems_sharedSoulsMisc
    OOTxMM_itemsextensionssystems_sharedOcarinaButtons: OOTxMM_itemsextensionssystems_sharedOcarinaButtons
    OOTxMM_itemsextensionssystems_sharedShovel: OOTxMM_itemsextensionssystems_sharedShovel
    OOTxMM_itemsextensionssystems_sharedSkeletonKey: OOTxMM_itemsextensionssystems_sharedSkeletonKey
    OOTxMM_itemsextensionssystems_sharedPlatinumToken: OOTxMM_itemsextensionssystems_sharedPlatinumToken
    OOTxMM_itemsextensionssystems_sharedBombchu: OOTxMM_itemsextensionssystems_sharedBombchu
    OOTxMM_itemsextensionscrossGameitems_sharedSpellFire: OOTxMM_itemsextensionscrossGameitems_sharedSpellFire
    OOTxMM_itemsextensionscrossGameitems_sharedSpellWind: OOTxMM_itemsextensionscrossGameitems_sharedSpellWind
    OOTxMM_itemsextensionscrossGameitems_sharedSpellLove: OOTxMM_itemsextensionscrossGameitems_sharedSpellLove
    OOTxMM_itemsextensionscrossGameitems_sharedBootsIron: OOTxMM_itemsextensionscrossGameitems_sharedBootsIron
    OOTxMM_itemsextensionscrossGameitems_sharedBootsHover: OOTxMM_itemsextensionscrossGameitems_sharedBootsHover
    OOTxMM_itemsextensionscrossGameitems_sharedTunicGoron: OOTxMM_itemsextensionscrossGameitems_sharedTunicGoron
    OOTxMM_itemsextensionscrossGameitems_sharedTunicZora: OOTxMM_itemsextensionscrossGameitems_sharedTunicZora
    OOTxMM_itemsextensionscrossGameitems_sharedScales: OOTxMM_itemsextensionscrossGameitems_sharedScales
    OOTxMM_itemsextensionscrossGameitems_sharedStrength: OOTxMM_itemsextensionscrossGameitems_sharedStrength
    OOTxMM_itemsextensionscrossGameitems_sharedHammer: OOTxMM_itemsextensionscrossGameitems_sharedHammer
    OOTxMM_itemsextensionscrossGameitems_sharedBoomerang: OOTxMM_itemsextensionscrossGameitems_sharedBoomerang
    OOTxMM_itemsextensionscrossGameitems_sharedGFS: OOTxMM_itemsextensionscrossGameitems_sharedGFS
    OOTxMM_itemsextensionscrossGameitems_sharedSlingshot: OOTxMM_itemsextensionscrossGameitems_sharedSlingshot
    OOTxMM_itemsextensionscrossGamemasks_sharedMaskGerudo: OOTxMM_itemsextensionscrossGamemasks_sharedMaskGerudo
    OOTxMM_itemsextensionscrossGamemasks_sharedMaskSkull: OOTxMM_itemsextensionscrossGamemasks_sharedMaskSkull
    OOTxMM_itemsextensionscrossGamemasks_sharedMaskSpooky: OOTxMM_itemsextensionscrossGamemasks_sharedMaskSpooky
    OOTxMM_itemsextensionscrossGameitems_sharedBottles: OOTxMM_itemsextensionscrossGameitems_sharedBottles
    OOTxMM_itemsageless_agelessSwords: OOTxMM_itemsageless_agelessSwords
    OOTxMM_itemsageless_agelessShields: OOTxMM_itemsageless_agelessShields
    OOTxMM_itemsageless_agelessTunics: OOTxMM_itemsageless_agelessTunics
    OOTxMM_itemsageless_agelessBoots: OOTxMM_itemsageless_agelessBoots
    OOTxMM_itemsageless_agelessSticks: OOTxMM_itemsageless_agelessSticks
    OOTxMM_itemsageless_agelessBoomerang: OOTxMM_itemsageless_agelessBoomerang
    OOTxMM_itemsageless_agelessHammer: OOTxMM_itemsageless_agelessHammer
    OOTxMM_itemsageless_agelessGFS: OOTxMM_itemsageless_agelessGFS
    OOTxMM_itemsageless_agelessHookshot: OOTxMM_itemsageless_agelessHookshot
    OOTxMM_itemsageless_agelessSlingshot: OOTxMM_itemsageless_agelessSlingshot
    OOTxMM_itemsageless_agelessBow: OOTxMM_itemsageless_agelessBow
    OOTxMM_itemsageless_agelessChildTrade: OOTxMM_itemsageless_agelessChildTrade
    OOTxMM_itemsageless_agelessStrength: OOTxMM_itemsageless_agelessStrength
    OOTxMM_itemsageless_agelessSoaring: OOTxMM_itemsageless_agelessSoaring
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildHookshot: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildHookshot
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultHookshot: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultHookshot
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildHookshotShort: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildHookshotShort
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultHookshotShort: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultHookshotShort
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBow: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBow
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBow: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBow
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildOcarinaOfTime: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildOcarinaOfTime
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultOcarinaOfTime: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultOcarinaOfTime
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildOcarinaFairy: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildOcarinaFairy
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultOcarinaFairy: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultOcarinaFairy
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBomb: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBomb
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBomb: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBomb
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBombchu: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBombchu
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBombchu: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBombchu
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildArrowFire: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildArrowFire
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultArrowFire: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultArrowFire
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildArrowIce: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildArrowIce
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultArrowIce: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultArrowIce
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildArrowLight: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildArrowLight
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultArrowLight: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultArrowLight
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildHammer: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildHammer
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultHammer: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultHammer
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSpellWind: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSpellWind
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSpellWind: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSpellWind
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSpellLove: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSpellLove
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSpellLove: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSpellLove
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSpellFire: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSpellFire
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSpellFire: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSpellFire
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBootsIron: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBootsIron
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBootsIron: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBootsIron
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBootsHover: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBootsHover
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBootsHover: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBootsHover
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildTunicGoron: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildTunicGoron
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultTunicGoron: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultTunicGoron
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildTunicZora: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildTunicZora
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultTunicZora: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultTunicZora
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildGreatFairySword: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildGreatFairySword
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultGreatFairySword: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultGreatFairySword
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBoomerang: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildBoomerang
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBoomerang: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultBoomerang
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSlingshot: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildSlingshot
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSlingshot: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultSlingshot
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildStick: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildStick
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultStick: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultStick
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskDeku: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskDeku
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskDeku: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskDeku
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDekuNuts: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDekuNuts
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDekuNuts: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDekuNuts
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMagicBean: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMagicBean
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMagicBean: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMagicBean
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildPowderKeg: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildPowderKeg
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultPowderKeg: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultPowderKeg
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildPictographBox: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildPictographBox
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultPictographBox: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultPictographBox
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildLensOfTruth: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildLensOfTruth
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultLensOfTruth: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultLensOfTruth
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGoron: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGoron
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGoron: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGoron
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskZora: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskZora
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskZora: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskZora
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskFierceDeity: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskFierceDeity
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskFierceDeity: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskFierceDeity
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskPostman: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskPostman
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskPostman: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskPostman
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskAllNight: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskAllNight
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskAllNight: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskAllNight
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskBlast: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskBlast
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskBlast: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskBlast
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskStone: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskStone
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskStone: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskStone
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGreatFairy: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGreatFairy
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGreatFairy: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGreatFairy
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskKeaton: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskKeaton
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskKeaton: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskKeaton
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskBremen: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskBremen
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskBremen: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskBremen
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskBunny: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskBunny
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskBunny: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskBunny
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskDonGero: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskDonGero
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskDonGero: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskDonGero
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskScents: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskScents
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskScents: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskScents
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskRomani: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskRomani
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskRomani: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskRomani
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskTroupeLeader: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskTroupeLeader
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskTroupeLeader: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskTroupeLeader
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskKafei: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskKafei
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskKafei: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskKafei
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskCouple: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskCouple
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskCouple: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskCouple
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskTruth: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskTruth
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskTruth: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskTruth
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskKamaro: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskKamaro
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskKamaro: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskKamaro
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGibdo: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGibdo
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGibdo: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGibdo
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGaro: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGaro
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGaro: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGaro
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskCaptain: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskCaptain
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskCaptain: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskCaptain
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGiant: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGiant
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGiant: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGiant
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGerudo: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskGerudo
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGerudo: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskGerudo
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskSkull: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskSkull
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskSkull: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskSkull
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskSpooky: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMaskSpooky
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskSpooky: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMaskSpooky
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMoonTear: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildMoonTear
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMoonTear: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultMoonTear
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedLand: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedLand
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedLand: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedLand
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedSwamp: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedSwamp
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedSwamp: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedSwamp
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedMountain: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedMountain
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedMountain: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedMountain
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedOcean: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildDeedOcean
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedOcean: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultDeedOcean
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildLetterToMama: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildLetterToMama
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultLetterToMama: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultLetterToMama
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildLetterToKafei: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildLetterToKafei
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultLetterToKafei: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultLetterToKafei
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildPendantOfMemories: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildPendantOfMemories
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultPendantOfMemories: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultPendantOfMemories
    OOTxMM_itemsmmAgeRequirements_mmAgeReqChildStrength: OOTxMM_itemsmmAgeRequirements_mmAgeReqChildStrength
    OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultStrength: OOTxMM_itemsmmAgeRequirements_mmAgeReqAdultStrength
    OOTxMM_itemsmmAgeRequirements_mmAgeReqRandom: OOTxMM_itemsmmAgeRequirements_mmAgeReqRandom
    OOTxMM_entrances_erSelfLoops: OOTxMM_entrances_erSelfLoops
    OOTxMM_entrances_erNoPolarity: OOTxMM_entrances_erNoPolarity
    OOTxMM_entrances_erDecoupled: OOTxMM_entrances_erDecoupled
    OOTxMM_entrances_erBoss: OOTxMM_entrances_erBoss
    OOTxMM_entrances_erDungeons: OOTxMM_entrances_erDungeons
    OOTxMM_entrances_erMajorDungeons: OOTxMM_entrances_erMajorDungeons
    OOTxMM_entrances_erMinorDungeons: OOTxMM_entrances_erMinorDungeons
    OOTxMM_entrances_erGanonCastle: OOTxMM_entrances_erGanonCastle
    OOTxMM_entrances_erGanonTower: OOTxMM_entrances_erGanonTower
    OOTxMM_entrances_erMoon: OOTxMM_entrances_erMoon
    OOTxMM_entrances_erSpiderHouses: OOTxMM_entrances_erSpiderHouses
    OOTxMM_entrances_erPirateFortress: OOTxMM_entrances_erPirateFortress
    OOTxMM_entrances_erBeneathWell: OOTxMM_entrances_erBeneathWell
    OOTxMM_entrances_erIkanaCastle: OOTxMM_entrances_erIkanaCastle
    OOTxMM_entrances_erSecretShrine: OOTxMM_entrances_erSecretShrine
    OOTxMM_entrances_erGrottos: OOTxMM_entrances_erGrottos
    OOTxMM_entrances_erIndoors: OOTxMM_entrances_erIndoors
    OOTxMM_entrances_erIndoorsMajor: OOTxMM_entrances_erIndoorsMajor
    OOTxMM_entrances_erIndoorsExtra: OOTxMM_entrances_erIndoorsExtra
    OOTxMM_entrances_erIndoorsTelescopes: OOTxMM_entrances_erIndoorsTelescopes
    OOTxMM_entrances_erIndoorsGameLinks: OOTxMM_entrances_erIndoorsGameLinks
    OOTxMM_entrances_erRegions: OOTxMM_entrances_erRegions
    OOTxMM_entrances_erRegionsExtra: OOTxMM_entrances_erRegionsExtra
    OOTxMM_entrances_erRegionsShortcuts: OOTxMM_entrances_erRegionsShortcuts
    OOTxMM_entrances_erOverworld: OOTxMM_entrances_erOverworld
    OOTxMM_entrances_erPiratesWorld: OOTxMM_entrances_erPiratesWorld
    OOTxMM_entrances_erMixed: OOTxMM_entrances_erMixed
    OOTxMM_entrances_erMixedDungeons: OOTxMM_entrances_erMixedDungeons
    OOTxMM_entrances_erMixedGrottos: OOTxMM_entrances_erMixedGrottos
    OOTxMM_entrances_erMixedIndoors: OOTxMM_entrances_erMixedIndoors
    OOTxMM_entrances_erMixedRegions: OOTxMM_entrances_erMixedRegions
    OOTxMM_entrances_erMixedOverworld: OOTxMM_entrances_erMixedOverworld
    OOTxMM_entrances_erSpawns: OOTxMM_entrances_erSpawns
    OOTxMM_entrances_erWallmasters: OOTxMM_entrances_erWallmasters
    OOTxMM_entrances_erWarps: OOTxMM_entrances_erWarps
    OOTxMM_entrances_erOneWays: OOTxMM_entrances_erOneWays
    OOTxMM_entrances_erOneWaysMajor: OOTxMM_entrances_erOneWaysMajor
    OOTxMM_entrances_erOneWaysIkana: OOTxMM_entrances_erOneWaysIkana
    OOTxMM_entrances_erOneWaysSongs: OOTxMM_entrances_erOneWaysSongs
    OOTxMM_entrances_erOneWaysStatues: OOTxMM_entrances_erOneWaysStatues
    OOTxMM_entrances_erOneWaysOwls: OOTxMM_entrances_erOneWaysOwls
    OOTxMM_entrances_erOneWaysWoods: OOTxMM_entrances_erOneWaysWoods
    OOTxMM_entrances_erOneWaysWaterVoids: OOTxMM_entrances_erOneWaysWaterVoids
    OOTxMM_entrances_erOneWaysAnywhere: OOTxMM_entrances_erOneWaysAnywhere
    OOTxMM_mainworld_mqDungeons: OOTxMM_mainworld_mqDungeons
    OOTxMM_mainworld_jpLayouts: OOTxMM_mainworld_jpLayouts
    OOTxMM_mainqol_mmEasierLightblock: OOTxMM_mainqol_mmEasierLightblock
    OOTxMM_mainqol_shadowFastBoat: OOTxMM_mainqol_shadowFastBoat
    OOTxMM_mainqol_openMaskShop: OOTxMM_mainqol_openMaskShop
    OOTxMM_mainqol_lenientSpikes: OOTxMM_mainqol_lenientSpikes
    OOTxMM_mainqol_fastBunnyHood: OOTxMM_mainqol_fastBunnyHood
    OOTxMM_mainqol_bowSlingshotBreakHives: OOTxMM_mainqol_bowSlingshotBreakHives
    OOTxMM_mainqol_critWiggleDisable: OOTxMM_mainqol_critWiggleDisable
    OOTxMM_mainqol_fastMasks: OOTxMM_mainqol_fastMasks
    OOTxMM_mainqol_keepItemsReset: OOTxMM_mainqol_keepItemsReset
    OOTxMM_mainqol_keepBottlesReset: OOTxMM_mainqol_keepBottlesReset
    OOTxMM_mainqol_mmSongOfDoubleTimeTimeSelector: OOTxMM_mainqol_mmSongOfDoubleTimeTimeSelector
    OOTxMM_mainqol_autoInvert: OOTxMM_mainqol_autoInvert
    OOTxMM_cutscenesmain_cutsceneSkipOoT: OOTxMM_cutscenesmain_cutsceneSkipOoT
    OOTxMM_cutscenesmain_cutsceneSkipMM: OOTxMM_cutscenesmain_cutsceneSkipMM
    OOTxMM_cutscenesglitches_cutsceneGlitchOoT: OOTxMM_cutscenesglitches_cutsceneGlitchOoT
    OOTxMM_cutscenesbossesoot_cutsceneIntroGohma: OOTxMM_cutscenesbossesoot_cutsceneIntroGohma
    OOTxMM_cutscenesbossesoot_cutsceneIntroKingDodongo: OOTxMM_cutscenesbossesoot_cutsceneIntroKingDodongo
    OOTxMM_cutscenesbossesoot_cutsceneIntroBarinade: OOTxMM_cutscenesbossesoot_cutsceneIntroBarinade
    OOTxMM_cutscenesbossesoot_cutsceneIntroPhantomGanon: OOTxMM_cutscenesbossesoot_cutsceneIntroPhantomGanon
    OOTxMM_cutscenesbossesoot_cutsceneIntroVolvagia: OOTxMM_cutscenesbossesoot_cutsceneIntroVolvagia
    OOTxMM_cutscenesbossesoot_cutsceneIntroMorpha: OOTxMM_cutscenesbossesoot_cutsceneIntroMorpha
    OOTxMM_cutscenesbossesoot_cutsceneIntroBongoBongo: OOTxMM_cutscenesbossesoot_cutsceneIntroBongoBongo
    OOTxMM_cutscenesbossesoot_cutsceneIntroTwinrova: OOTxMM_cutscenesbossesoot_cutsceneIntroTwinrova
    OOTxMM_cutscenesbossesoot_cutsceneIntroGanondorf: OOTxMM_cutscenesbossesoot_cutsceneIntroGanondorf
    OOTxMM_cutscenesbossesmm_cutsceneIntroOdolwa: OOTxMM_cutscenesbossesmm_cutsceneIntroOdolwa
    OOTxMM_cutscenesbossesmm_cutsceneIntroGoht: OOTxMM_cutscenesbossesmm_cutsceneIntroGoht
    OOTxMM_cutscenesminibossesmm_cutsceneIntroWart: OOTxMM_cutscenesminibossesmm_cutsceneIntroWart
    OOTxMM_cutscenesbossesmm_cutsceneIntroGyorg: OOTxMM_cutscenesbossesmm_cutsceneIntroGyorg
    OOTxMM_cutscenesminibossesmm_cutsceneIntroIgos: OOTxMM_cutscenesminibossesmm_cutsceneIntroIgos
    OOTxMM_cutscenesminibossesmm_cutsceneIntroGomess: OOTxMM_cutscenesminibossesmm_cutsceneIntroGomess
    OOTxMM_cutscenesbossesmm_cutsceneIntroTwinmold: OOTxMM_cutscenesbossesmm_cutsceneIntroTwinmold
    OOTxMM_cutscenesbossesmm_cutsceneIntroMajora: OOTxMM_cutscenesbossesmm_cutsceneIntroMajora

option_groups = []

option_presets = {}

