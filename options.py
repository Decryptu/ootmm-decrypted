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
    - **cross**: Any unshuffled Token can be found on any other unshuffled Skulltula
    - **all**: Swamp and Ocean Tokens can be found anywhere
    """
    display_name = "House Skulltula Tokens Shuffle"
    option_none = 0
    option_cross = 1
    option_all = 2
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
    - **random**: All prices are randomized.
    """
    display_name = "OoT Shop Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    option_random = 3
    default = option_vanilla

class OOTxMM_mainprices_priceOotScrubs(Choice):
    """
    Sets the price of items sold by OoT scrubs
    - **affordable**: All prices are set to 10 rupees.
    - **vanilla**: All prices are set to their vanilla values.
    - **weighted**: All prices are randomized, but lower prices are favored.
    - **random**: All prices are randomized.
    """
    display_name = "OoT Scrub Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    option_random = 3
    default = option_vanilla

class OOTxMM_mainprices_priceOotMerchants(Choice):
    """
    Sets the price of items sold by OoT merchants
    - **affordable**: All prices are set to 10 rupees.
    - **vanilla**: All prices are set to their vanilla values.
    - **weighted**: All prices are randomized, but lower prices are favored.
    - **random**: All prices are randomized.
    """
    display_name = "OoT Merchants Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    option_random = 3
    default = option_vanilla

class OOTxMM_mainprices_priceMmShops(Choice):
    """
    Sets the price of items sold inside MM shops
    - **affordable**: All prices are set to 10 rupees.
    - **vanilla**: All prices are set to their vanilla values.
    - **weighted**: All prices are randomized, but lower prices are favored.
    - **random**: All prices are randomized.
    """
    display_name = "MM Shop Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    option_random = 3
    default = option_vanilla

class OOTxMM_mainprices_priceMmTingle(Choice):
    """
    Sets the price of items sold by Tingle
    - **affordable**: All prices are set to 10 rupees.
    - **vanilla**: All prices are set to their vanilla values.
    - **weighted**: All prices are randomized, but lower prices are favored.
    - **random**: All prices are randomized.
    """
    display_name = "MM Tingle Prices"
    option_affordable = 0
    option_vanilla = 1
    option_weighted = 2
    option_random = 3
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

class OOTxMM_mainevents_startingAge(Choice):
    """
    Choose the starting age
    - **child**: Link will start off as Child
    - **adult**: Link will start off as Adult
    - **random**: Link will start off as either Adult or Child, with a 50/50 probability
    """
    display_name = "Starting Age"
    option_child = 0
    option_adult = 1
    option_random = 2
    default = option_child

class OOTxMM_mainevents_swordlessAdult(Toggle):
    """
    Choose whether or not Adult Link can be swordless
    """
    display_name = "Allow Adult Link to be swordless"
    default = False

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
    Allows you to switch ages by playing Song of Time after you've switched ages once in Temple of Time.<br>Preserves your current position on the scene, which logic can expect you to take advantage of.
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

class OOTxMM_itemsextensions_fillWallets(Toggle):
    """
    Fills the wallet upon finding a new one
    """
    display_name = "Fill Wallets"
    default = False

class OOTxMM_itemsextensions_bottleContentShuffle(Toggle):
    """
    Randomize what bottles from both games contain upon finding them in the world
    """
    display_name = "Random Bottle Contents"
    default = False

class OOTxMM_itemsextensions_stoneAgonyMm(Toggle):
    """
    Enables Stone of Agony in MM
    """
    display_name = "Stone of Agony in MM"
    default = False

class OOTxMM_itemsextensions_sticksNutsUpgradesMm(Toggle):
    """
    Enables Deku Stick and Nut upgrades in MM
    """
    display_name = "Deku Stick & Nut Upgrades in MM"
    default = False

class OOTxMM_itemsextensions_fairyOcarinaMm(Toggle):
    """
    Functionally identical as the Ocarina of Time, but now there's 2 Ocarinas for Majora's Mask!
    """
    display_name = "Fairy Ocarina in MM"
    default = False

class OOTxMM_itemsextensions_blueFireArrows(Toggle):
    """
    Gives the OoT Ice Arrows the properties of Blue Fire
    """
    display_name = "Blue Fire Arrows"
    default = False

class OOTxMM_itemsextensions_iceArrowPlatformsOot(Toggle):
    """
    Allow ice arrows in OoT to create walkable ice platforms on water
    """
    display_name = "Ice Arrow Platforms (OoT)"
    default = False

class OOTxMM_itemsextensions_sunlightArrows(Toggle):
    """
    Gives the OoT Light Arrows the ability to activate most sun switches
    """
    display_name = "Sunlight Arrows"
    default = False

class OOTxMM_itemsextensions_shortHookshotMm(Toggle):
    """
    Adds a short Hookshot in MM, which logic accounts for. A trick is also there for some of the harder spots
    """
    display_name = "Short Hookshot in MM"
    default = False

class OOTxMM_itemsextensions_bronzeScale(Toggle):
    """
    Add an extra scale item, that is required to enter deep water.
    """
    display_name = "Bronze Scale"
    default = False

class OOTxMM_itemsextensions_childWallets(Toggle):
    """
    Shuffles the starting wallet in each game... making it so you have to find it to hold anything!
    """
    display_name = "Child Wallets"
    default = False

class OOTxMM_itemsextensions_colossalWallets(Toggle):
    """
    Adds a Wallet that can hold up to 999 rupees in each game
    """
    display_name = "Colossal Wallets"
    default = False

class OOTxMM_itemsextensions_bottomlessWallets(Toggle):
    """
    Adds a Wallet that can hold up to 9999 rupees in each game
    """
    display_name = "Bottomless Wallets"
    default = False

class OOTxMM_itemsextensions_rupeeScaling(Toggle):
    """
    Makes rupees worth twice as much with the Colossal Wallet, and twenty times as much with the Bottomless Wallet.
    """
    display_name = "Rupee Scaling"
    default = False

class OOTxMM_itemsextensions_skeletonKeyOot(Toggle):
    """
    Adds a Skeleton Key that can open every small-key-locked door in OoT.
    """
    display_name = "Skeleton Key (OoT)"
    default = False

class OOTxMM_itemsextensions_skeletonKeyMm(Toggle):
    """
    Adds a Skeleton Key that can open every small-key-locked door in MM.
    """
    display_name = "Skeleton Key (MM)"
    default = False

class OOTxMM_itemsextensions_magicalRupee(Toggle):
    """
    Adds a Magical Rupee that can trigger every silver-rupee event in OoT dungeons.
    """
    display_name = "Magical Rupee"
    default = False

class OOTxMM_itemsextensions_transcendentFairy(Toggle):
    """
    Adds a Transcendent Fairy that counts as every Stray Fairy in MM.
    """
    display_name = "Transcendent Fairy"
    default = False

class OOTxMM_itemsextensions_platinumTokenOot(Toggle):
    """
    Adds a Platinum Token that counts as every Gold Skulltula Token.
    """
    display_name = "Platinum Token (OoT)"
    default = False

class OOTxMM_itemsextensions_platinumTokenMm(Toggle):
    """
    Adds a Platinum Token that counts as every House Token.
    """
    display_name = "Platinum Token (MM)"
    default = False

class OOTxMM_itemsextensions_bombchuBehaviorOot(Choice):
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

class OOTxMM_itemsextensions_bombchuBehaviorMm(Choice):
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

class OOTxMM_itemsextensions_spellFireMm(Toggle):
    """
    Adds Din's Fire in Majora's Mask.
    """
    display_name = "Din's Fire (MM)"
    default = False

class OOTxMM_itemsextensions_spellWindMm(Toggle):
    """
    Adds Farore's Wind in Majora's Mask.
    """
    display_name = "Farore's Wind (MM)"
    default = False

class OOTxMM_itemsextensions_spellLoveMm(Toggle):
    """
    Adds Nayru's Love in Majora's Mask.
    """
    display_name = "Nayru's Love (MM)"
    default = False

class OOTxMM_itemsextensions_bootsIronMm(Toggle):
    """
    Adds Iron Boots in Majora's Mask.
    """
    display_name = "Iron Boots (MM)"
    default = False

class OOTxMM_itemsextensions_bootsHoverMm(Toggle):
    """
    Adds Hover Boots in Majora's Mask.
    """
    display_name = "Hover Boots (MM)"
    default = False

class OOTxMM_itemsextensions_tunicGoronMm(Toggle):
    """
    Adds the Goron Tunic in Majora's Mask.
    """
    display_name = "Goron Tunic (MM)"
    default = False

class OOTxMM_itemsextensions_tunicZoraMm(Toggle):
    """
    Adds the Zora Tunic in Majora's Mask.
    """
    display_name = "Zora Tunic (MM)"
    default = False

class OOTxMM_itemsextensions_scalesMm(Toggle):
    """
    Adds the Silver Scale and Golden Scale in Majora's Mask.
    """
    display_name = "Scales (MM)"
    default = False

class OOTxMM_itemsextensions_strengthMm(Toggle):
    """
    Adds the Goron's Bracelet, Silver Gauntlets and Golden Gauntlets in Majora's Mask.
    """
    display_name = "Strength (MM)"
    default = False

class OOTxMM_itemsextensions_kegStrength3(Toggle):
    """
    If you have the Golden Gauntlets in Majora's Mask, this allows you to purchase and use Powder Kegs, and attempt the Keg Trial.
    """
    display_name = "Use Keg With Golden Gauntlets"
    default = False

class OOTxMM_itemsextensions_hammerMm(Toggle):
    """
    Adds the Megaton Hammer in Majora's Mask.
    """
    display_name = "Megaton Hammer (MM)"
    default = False

class OOTxMM_itemsextensions_boomerangMm(Toggle):
    """
    Adds the Boomerang in Majora's Mask.
    """
    display_name = "Boomerang (MM)"
    default = False

class OOTxMM_itemsextensions_gfsOot(Toggle):
    """
    Adds the Great Fairy's Sword in Ocarina of Time.
    """
    display_name = "Great Fairy's Sword (OoT)"
    default = False

class OOTxMM_itemsextensions_slingshotMm(Toggle):
    """
    Adds the Slingshot in Majora's Mask.
    """
    display_name = "Slingshot (MM)"
    default = False

class OOTxMM_itemsextensions_spinUpgradeOot(Toggle):
    """
    Add the Spin Attack upgrade as an item in OoT.
    """
    display_name = "Spin Attack Upgrade (OoT)"
    default = False

class OOTxMM_itemsextensions_extraChildSwordsOot(Toggle):
    """
    Add the Razor and Gilded Swords in OoT, as upgrades to the Kokiri Sword.
    """
    display_name = "Extra Child Swords (OoT)"
    default = False

class OOTxMM_itemsextensions_dekuShieldMm(Toggle):
    """
    Add the Deku Shield in Majora's Mask.
    """
    display_name = "Deku Shield (MM)"
    default = False

class OOTxMM_itemsextensions_blastMaskOot(Toggle):
    """
    Add the Blast Mask in Ocarina of Time.
    """
    display_name = "Blast Mask (OoT)"
    default = False

class OOTxMM_itemsextensions_stoneMaskOot(Toggle):
    """
    Add the Stone Mask in Ocarina of Time.
    """
    display_name = "Stone Mask (OoT)"
    default = False

class OOTxMM_itemsextensions_kamaroMaskOot(Toggle):
    """
    Add the Kamaro Mask in Ocarina of Time.
    """
    display_name = "Kamaro Mask (OoT)"
    default = False

class OOTxMM_itemsextensions_elegyOot(Toggle):
    """
    Add the Elegy of Emptiness in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Elegy of Emptiness (OoT)"
    default = False

class OOTxMM_itemsextensions_songSoaringOot(Toggle):
    """
    Add the Song of Soaring in Ocarina of Time. Usable only as child. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Song of Soaring (OoT)"
    default = False

class OOTxMM_itemsextensions_songHealingOot(Toggle):
    """
    Add the Song of Healing in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Song of Healing (OoT)"
    default = False

class OOTxMM_itemsextensions_songAwakeningOot(Toggle):
    """
    Add the Sonata of Awakening in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Sonata of Awakening (OoT)"
    default = False

class OOTxMM_itemsextensions_songGoronOot(Toggle):
    """
    Add the Goron Lullaby in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Goron Lullaby (OoT)"
    default = False

class OOTxMM_itemsextensions_songZoraOot(Toggle):
    """
    Add the New Wave Bossa Nova in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "New Wave Bossa Nova (OoT)"
    default = False

class OOTxMM_itemsextensions_songOrderOot(Toggle):
    """
    Add the Oath to Order in Ocarina of Time. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Oath to Order (OoT)"
    default = False

class OOTxMM_itemsextensions_songSunMm(Toggle):
    """
    Add Sun's Song in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Sun's Song (MM)"
    default = False

class OOTxMM_itemsextensions_songZeldaLullabyMm(Toggle):
    """
    Add Zelda's Lullaby in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Zelda's Lullaby (MM)"
    default = False

class OOTxMM_itemsextensions_songSariasMm(Toggle):
    """
    Add Saria's Song in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Saria's Song (MM)"
    default = False

class OOTxMM_itemsextensions_songMinuetMm(Toggle):
    """
    Add the Minuet of Forest in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Minuet of Forest (MM)"
    default = False

class OOTxMM_itemsextensions_songBoleroMm(Toggle):
    """
    Add the Bolero of Fire in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Bolero of Fire (MM)"
    default = False

class OOTxMM_itemsextensions_songSerenadeMm(Toggle):
    """
    Add the Serenade of Water in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Serenade of Water (MM)"
    default = False

class OOTxMM_itemsextensions_songRequiemMm(Toggle):
    """
    Add the Requiem of Spirit in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Requiem of Spirit (MM)"
    default = False

class OOTxMM_itemsextensions_songNocturneMm(Toggle):
    """
    Add the Nocturne of Shadow in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Nocturne of Shadow (MM)"
    default = False

class OOTxMM_itemsextensions_songPreludeMm(Toggle):
    """
    Add the Prelude of Light in Majora's Mask. If Songs are on Song Locations, you must share or start with at least one song
    """
    display_name = "Prelude of Light (MM)"
    default = False

class OOTxMM_itemsextensions_powderKegOot(Toggle):
    """
    Add the Powder Keg in Ocarina of Time. Once found, Medigoron in Goron City will sell Powder Kegs after you buy his item.
    """
    display_name = "Powder Keg (OoT)"
    default = False

class OOTxMM_itemsextensions_ocarinaButtonsShuffleOot(Toggle):
    """
    Add the Ocarina Buttons for OoT into the item pool. Ocarina notes cannot be played until the corresponding button is obtained.
    """
    display_name = "Ocarina Buttons (OoT)"
    default = False

class OOTxMM_itemsextensions_ocarinaButtonsShuffleMm(Toggle):
    """
    Add the Ocarina Buttons for MM into the item pool. Ocarina notes cannot be played until the corresponding button is obtained.
    """
    display_name = "Ocarina Buttons (MM)"
    default = False

class OOTxMM_itemsextensions_soulsEnemyOot(Toggle):
    """
    Add Souls for OoT enemies into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Enemy Souls (OoT)"
    default = False

class OOTxMM_itemsextensions_soulsEnemyMm(Toggle):
    """
    Add Souls for MM enemies into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Enemy Souls (MM)"
    default = False

class OOTxMM_itemsextensions_soulsBossOot(Toggle):
    """
    Add Souls for OoT bosses into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Boss Souls (OoT)"
    default = False

class OOTxMM_itemsextensions_soulsBossMm(Toggle):
    """
    Add Souls for MM bosses into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Boss Souls (MM)"
    default = False

class OOTxMM_itemsextensions_soulsNpcOot(Toggle):
    """
    Add Souls for OoT NPCs into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "NPC Souls (OoT)"
    default = False

class OOTxMM_itemsextensions_soulsNpcMm(Toggle):
    """
    Add Souls for MM NPCs into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "NPC Souls (MM)"
    default = False

class OOTxMM_itemsextensions_soulsAnimalOot(Toggle):
    """
    Add Souls for OoT animals into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Animal Souls (OoT)"
    default = False

class OOTxMM_itemsextensions_soulsAnimalMm(Toggle):
    """
    Add Souls for MM animals into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Animal Souls (MM)"
    default = False

class OOTxMM_itemsextensions_soulsMiscOot(Toggle):
    """
    Add Souls for OoT Business Scrubs and Gold Skulltulas into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Misc. Souls (OoT)"
    default = False

class OOTxMM_itemsextensions_soulsMiscMm(Toggle):
    """
    Add Souls for MM Business Scrubs and Gold Skulltulas into the item pool. They won't spawn unless their Soul is obtained.
    """
    display_name = "Misc. Souls (MM)"
    default = False

class OOTxMM_itemsextensions_rustyKeysOot(Toggle):
    """
    Add rusty keys to the item pool. Every rusty key locks a single overworld door.
    """
    display_name = "Rusty Keys (OoT)"
    default = False

class OOTxMM_itemsextensions_rustyKeysMm(Toggle):
    """
    Add rusty keys to the item pool. Every rusty key locks a single overworld door.
    """
    display_name = "Rusty Keys (MM)"
    default = False

class OOTxMM_itemsextensions_clocks(Toggle):
    """
    Add items representing every Majora's Mask day and night into the pool. The moon will crash early unless you collect these items.
    """
    display_name = "Clocks as Items"
    default = False

class OOTxMM_itemsextensions_menuNotebook(Toggle):
    """
    Locks the in-game tracker behind the Bombers' Notebook
    """
    display_name = "Bombers' Tracker"
    default = False

class OOTxMM_itemsextensions_coins(Toggle):
    """
    Enable the leftover Coin items. These can be used for special conditions
    """
    display_name = "Coins"
    default = False

class OOTxMM_itemsextensions_coinsRed(Range):
    """
    How many Red Coins to add to the item pool
    """
    display_name = "Red Coins"
    range_start = 0
    range_end = 999
    default = 0

class OOTxMM_itemsextensions_coinsGreen(Range):
    """
    How many Green Coins to add to the item pool
    """
    display_name = "Green Coins"
    range_start = 0
    range_end = 999
    default = 0

class OOTxMM_itemsextensions_coinsBlue(Range):
    """
    How many Blue Coins to add to the item pool
    """
    display_name = "Blue Coins"
    range_start = 0
    range_end = 999
    default = 0

class OOTxMM_itemsextensions_coinsYellow(Range):
    """
    How many Yellow Coins to add to the item pool
    """
    display_name = "Yellow Coins"
    range_start = 0
    range_end = 999
    default = 0

class OOTxMM_itemsextensions_trapIce(Toggle):
    """
    Add Ice Traps to the item pool. They freeze you when collected.
    """
    display_name = "Ice Traps"
    default = True

class OOTxMM_itemsextensions_trapFire(Toggle):
    """
    Add Fire Traps to the item pool. They burn you when collected.
    """
    display_name = "Fire Traps"
    default = False

class OOTxMM_itemsextensions_trapShock(Toggle):
    """
    Add Shock Traps to the item pool. They shock you when collected.
    """
    display_name = "Shock Traps"
    default = False

class OOTxMM_itemsextensions_trapDrain(Toggle):
    """
    Add Drain Traps to the item pool. They drain your life when collected.
    """
    display_name = "Drain Traps"
    default = False

class OOTxMM_itemsextensions_trapAntiMagic(Toggle):
    """
    Add Anti-Magic Traps to the item pool. They drain magic from you when collected.
    """
    display_name = "Anti-Magic Traps"
    default = False

class OOTxMM_itemsextensions_trapKnockback(Toggle):
    """
    Add Knockback Traps to the item pool. They throw you in a random direction.
    """
    display_name = "Knockback Traps"
    default = False

class OOTxMM_itemsextensions_trapRupoor(Toggle):
    """
    Add Rupoors to the item pool. They remove 10 rupees when collected.
    """
    display_name = "Rupoors"
    default = False

class OOTxMM_itemsextensions_cloakTraps(Toggle):
    """
    Makes traps look like different items.
    """
    display_name = "Cloak Traps"
    default = True

class OOTxMM_itemsextensions_trapsQuantity(Choice):
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

class OOTxMM_itemsextensions_songOfDoubleTimeOot(Toggle):
    """
    Enables using Song of Double Time in OoT when you have the Song of Time in OoT
    """
    display_name = "Song of Double Time (OoT)"
    default = False

class OOTxMM_itemsshared_sharedStoneAgony(Toggle):
    """
    Combines the Stones of Agony from OoT and MM into one item for both games
    """
    display_name = "Shared Stone of Agony"
    default = False

class OOTxMM_itemsshared_sharedSpinUpgrade(Toggle):
    """
    Combines the Spin Attack Upgrades from OoT and MM into one item for both games
    """
    display_name = "Shared Spin Attack Upgrade"
    default = False

class OOTxMM_itemsshared_sharedNutsSticks(Toggle):
    """
    Combines the Deku Stick and Nut Upgrades from OoT and MM into two items each for both games
    """
    display_name = "Shared Deku Sticks & Nuts"
    default = False

class OOTxMM_itemsshared_sharedBows(Toggle):
    """
    Combines the Bows from OoT and MM into three progressive items for both games
    """
    display_name = "Shared Bows"
    default = False

class OOTxMM_itemsshared_sharedBombBags(Toggle):
    """
    Combines the Bomb Bags from OoT and MM into three progressive items for both games
    """
    display_name = "Shared Bomb Bags"
    default = False

class OOTxMM_itemsshared_sharedMagic(Toggle):
    """
    Combines the Magic Upgrades from OoT and MM into two progressive items for both games
    """
    display_name = "Shared Magic"
    default = False

class OOTxMM_itemsshared_sharedMagicArrowFire(Toggle):
    """
    Combines the Fire Arrows from OoT and MM into one item for both games
    """
    display_name = "Shared Fire Arrows"
    default = False

class OOTxMM_itemsshared_sharedMagicArrowIce(Toggle):
    """
    Combines the Ice Arrows from OoT and MM into one item for both games
    """
    display_name = "Shared Ice Arrows"
    default = False

class OOTxMM_itemsshared_sharedMagicArrowLight(Toggle):
    """
    Combines the Light Arrows from OoT and MM into one item for both games
    """
    display_name = "Shared Light Arrows"
    default = False

class OOTxMM_itemsshared_sharedSongEpona(Toggle):
    """
    Combines Epona's Song from OoT and MM into one item for both games
    """
    display_name = "Shared Epona's Song"
    default = False

class OOTxMM_itemsshared_sharedSongStorms(Toggle):
    """
    Combines Song of Storms from OoT and MM into one item for both games
    """
    display_name = "Shared Song of Storms"
    default = False

class OOTxMM_itemsshared_sharedSongTime(Toggle):
    """
    Combines Song of Time from OoT and MM into one item for both games
    """
    display_name = "Shared Song of Time"
    default = False

class OOTxMM_itemsshared_sharedSongSun(Toggle):
    """
    Combines Sun's Song from OoT and MM into one item for both games
    """
    display_name = "Shared Sun's Song"
    default = False

class OOTxMM_itemsshared_sharedHookshot(Toggle):
    """
    Combines the Hookshots from OoT and MM into two progressive items for both games.<br>If "Short Hookshot in MM" is disabled, the MM Hookshot will be given along with the first progressive item.
    """
    display_name = "Shared Hookshots"
    default = False

class OOTxMM_itemsshared_sharedLens(Toggle):
    """
    Combines the Lenses of Truth from OoT and MM into one item for both games
    """
    display_name = "Shared Lens of Truth"
    default = False

class OOTxMM_itemsshared_sharedOcarina(Toggle):
    """
    Combines the Ocarinas from OoT and MM into two progressive items for both games.<br>If "Fairy Ocarina in MM" is disabled, the MM Ocarina will be given along with the second progressive item.
    """
    display_name = "Shared Ocarinas"
    default = False

class OOTxMM_itemsshared_sharedMaskGoron(Toggle):
    """
    Combines the Goron Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Goron Mask"
    default = False

class OOTxMM_itemsshared_sharedMaskZora(Toggle):
    """
    Combines the Zora Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Zora Mask"
    default = False

class OOTxMM_itemsshared_sharedMaskBunny(Toggle):
    """
    Combines the Bunny Hoods from OoT and MM into one item for both games
    """
    display_name = "Shared Bunny Hood"
    default = False

class OOTxMM_itemsshared_sharedMaskKeaton(Toggle):
    """
    Combines the Keaton Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Keaton Mask"
    default = False

class OOTxMM_itemsshared_sharedMaskTruth(Toggle):
    """
    Combines the Masks of Truth from OoT and MM into one item for both games
    """
    display_name = "Shared Mask of Truth"
    default = False

class OOTxMM_itemsshared_sharedMaskBlast(Toggle):
    """
    Combines the Blast Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Blast Mask"
    default = False

class OOTxMM_itemsshared_sharedMaskStone(Toggle):
    """
    Combines the Stone Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Stone Mask"
    default = False

class OOTxMM_itemsshared_sharedMaskKamaro(Toggle):
    """
    Combines the Kamaro Masks from OoT and MM into one item for both games
    """
    display_name = "Shared Kamaro Mask"
    default = False

class OOTxMM_itemsshared_sharedSongElegy(Toggle):
    """
    Combines the Elegies of Emptiness from OoT and MM into one item for both games
    """
    display_name = "Shared Elegy of Emptiness"
    default = False

class OOTxMM_itemsshared_sharedSongHealing(Toggle):
    """
    Combines the Songs of Healing from OoT and MM into one item for both games
    """
    display_name = "Shared Song of Healing"
    default = False

class OOTxMM_itemsshared_sharedSongSoaring(Toggle):
    """
    Combines the Songs of Song from OoT and MM into one item for both games
    """
    display_name = "Shared Song of Soaring"
    default = False

class OOTxMM_itemsshared_sharedSongAwakening(Toggle):
    """
    Combines the Sonata of Awakening from OoT and MM into one item for both games
    """
    display_name = "Shared Sonata of Awakening"
    default = False

class OOTxMM_itemsshared_sharedSongGoron(Toggle):
    """
    Combines the Goron Lullaby from OoT and MM into one item for both games
    """
    display_name = "Shared Goron Lullaby"
    default = False

class OOTxMM_itemsshared_sharedSongZora(Toggle):
    """
    Combines the New Wave Bossa Nova from OoT and MM into one item for both games
    """
    display_name = "Shared New Wave Bossa Nova"
    default = False

class OOTxMM_itemsshared_sharedSongOrder(Toggle):
    """
    Combines the Oath to Order from OoT and MM into one item for both games
    """
    display_name = "Shared Oath to Order"
    default = False

class OOTxMM_itemsshared_sharedSongZeldaLullaby(Toggle):
    """
    Combines Zelda's Lullaby from OoT and MM into one item for both games
    """
    display_name = "Shared Zelda's Lullaby"
    default = False

class OOTxMM_itemsshared_sharedSongSarias(Toggle):
    """
    Combines Saria's Song from OoT and MM into one item for both games
    """
    display_name = "Shared Saria's Song"
    default = False

class OOTxMM_itemsshared_sharedSongMinuet(Toggle):
    """
    Combines the Minuet of Forest from OoT and MM into one item for both games
    """
    display_name = "Shared Minuet of Forest"
    default = False

class OOTxMM_itemsshared_sharedSongBolero(Toggle):
    """
    Combines the Bolero of Fire from OoT and MM into one item for both games
    """
    display_name = "Shared Bolero of Fire"
    default = False

class OOTxMM_itemsshared_sharedSongSerenade(Toggle):
    """
    Combines the Serenade of Water from OoT and MM into one item for both games
    """
    display_name = "Shared Serenade of Water"
    default = False

class OOTxMM_itemsshared_sharedSongRequiem(Toggle):
    """
    Combines the Requiem of Spirit from OoT and MM into one item for both games
    """
    display_name = "Shared Requiem of Spirit"
    default = False

class OOTxMM_itemsshared_sharedSongNocturne(Toggle):
    """
    Combines the Nocturne of Shadow from OoT and MM into one item for both games
    """
    display_name = "Shared Nocturne of Shadow"
    default = False

class OOTxMM_itemsshared_sharedSongPrelude(Toggle):
    """
    Combines the Prelude of Light from OoT and MM into one item for both games
    """
    display_name = "Shared Prelude of Light"
    default = False

class OOTxMM_itemsshared_sharedPowderKeg(Toggle):
    """
    Combines the Powder Kegs from OoT and MM into one item for both games.
    """
    display_name = "Shared Powder Keg"
    default = False

class OOTxMM_itemsshared_sharedWallets(Toggle):
    """
    Combines the Wallets from OoT and MM into multiple progressive items for both games, depending on settings
    """
    display_name = "Shared Wallets"
    default = False

class OOTxMM_itemsshared_sharedHealth(Toggle):
    """
    Combines the Heart Pieces, Heart Containers and Double Defenses from OoT and MM into 44 Heart Pieces, 6 Heart Containers and one Double Defense for both games
    """
    display_name = "Shared Health"
    default = False

class OOTxMM_itemsshared_sharedSwords(Toggle):
    """
    Combines the Kokiri, Razor and Gilded Swords from OoT and MM into three progressive items for both games
    """
    display_name = "Shared Child Swords"
    default = False

class OOTxMM_itemsshared_sharedShields(Toggle):
    """
    When you obtain a shield, the opposite game's equivalent is given to you as well. With this, the Hylian and Hero's Shields are considered equivalent.<br>If Shields are Progressive, all Shields are combined into three progressive items: Deku Shield -> Hylian/Hero's Shield -> Mirror Shield
    """
    display_name = "Shared Shields"
    default = False

class OOTxMM_itemsshared_sharedSoulsEnemy(Toggle):
    """
    Combines the OoT and MM Souls for a specific enemy into one item, for all enemies present in both games
    """
    display_name = "Shared Enemy Souls"
    default = False

class OOTxMM_itemsshared_sharedSoulsNpc(Toggle):
    """
    Combines the OoT and MM Souls for a specific NPC into one item, for all NPCs present in both games
    """
    display_name = "Shared NPC Souls"
    default = False

class OOTxMM_itemsshared_sharedSoulsAnimal(Toggle):
    """
    Combines the OoT and MM Souls for a specific animal into one item, for all animals present in both games
    """
    display_name = "Shared Animal Souls"
    default = False

class OOTxMM_itemsshared_sharedSoulsMisc(Toggle):
    """
    Combines the OoT and MM Souls for Business Scrubs and Gold Skulltulas into two items for both games
    """
    display_name = "Shared Misc. Souls"
    default = False

class OOTxMM_itemsshared_sharedOcarinaButtons(Toggle):
    """
    Combines the Ocarina Buttons from OoT and MM into five items for both games
    """
    display_name = "Shared Ocarina Buttons"
    default = False

class OOTxMM_itemsshared_sharedSkeletonKey(Toggle):
    """
    Combines the Skeleton Key from OoT and MM into one item for both games
    """
    display_name = "Shared Skeleton Key"
    default = False

class OOTxMM_itemsshared_sharedPlatinumToken(Toggle):
    """
    Combines the Platinum Token from OoT and MM into one item for both games
    """
    display_name = "Shared Platinum Token"
    default = False

class OOTxMM_itemsshared_sharedBombchu(Toggle):
    """
    Combines either Bombchu or the Bombchu Bags from OoT and MM into items for both games, depending on settings
    """
    display_name = "Shared Bombchu"
    default = False

class OOTxMM_itemsshared_sharedSpellFire(Toggle):
    """
    Combines Din's Fire from OoT and MM into one item for both games
    """
    display_name = "Shared Din's Fire"
    default = False

class OOTxMM_itemsshared_sharedSpellWind(Toggle):
    """
    Combines Farore's Wind from OoT and MM into one item for both games
    """
    display_name = "Shared Farore's Wind"
    default = False

class OOTxMM_itemsshared_sharedSpellLove(Toggle):
    """
    Combines Nayru's Love from OoT and MM into one item for both games
    """
    display_name = "Shared Nayru's Love"
    default = False

class OOTxMM_itemsshared_sharedBootsIron(Toggle):
    """
    Combines the Iron Boots from OoT and MM into one item for both games
    """
    display_name = "Shared Iron Boots"
    default = False

class OOTxMM_itemsshared_sharedBootsHover(Toggle):
    """
    Combines the Hover Boots from OoT and MM into one item for both games
    """
    display_name = "Shared Hover Boots"
    default = False

class OOTxMM_itemsshared_sharedTunicGoron(Toggle):
    """
    Combines the Goron Tunics from OoT and MM into two items for both games
    """
    display_name = "Shared Goron Tunic"
    default = False

class OOTxMM_itemsshared_sharedTunicZora(Toggle):
    """
    Combines the Zora Tunics from OoT and MM into two items for both games
    """
    display_name = "Shared Zora Tunic"
    default = False

class OOTxMM_itemsshared_sharedScales(Toggle):
    """
    Combines the Scales from OoT and MM into multiple progressive items for both games, depending on settings
    """
    display_name = "Shared Scales"
    default = False

class OOTxMM_itemsshared_sharedStrength(Toggle):
    """
    Combines the Strength Upgrades from OoT and MM into three progressive items for both games
    """
    display_name = "Shared Strength"
    default = False

class OOTxMM_itemsshared_sharedHammer(Toggle):
    """
    Combines the Megaton Hammers from OoT and MM into one item for both games
    """
    display_name = "Shared Megaton Hammer"
    default = False

class OOTxMM_itemsshared_sharedBoomerang(Toggle):
    """
    Combines the Boomerangs from OoT and MM into one item for both games
    """
    display_name = "Shared Boomerang"
    default = False

class OOTxMM_itemsshared_sharedGFS(Toggle):
    """
    Combines the Great Fairy's Sword from OoT and MM into one item for both games
    """
    display_name = "Shared Great Fairy's Sword"
    default = False

class OOTxMM_itemsshared_sharedSlingshot(Toggle):
    """
    Combines the Slingshots from OoT and MM into one item for both games
    """
    display_name = "Shared Slingshot"
    default = False

class OOTxMM_itemsshared_sharedBottles(Toggle):
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
    OOTxMM_mainshuffle_shuffleWonderItemsOot: OOTxMM_mainshuffle_shuffleWonderItemsOot
    OOTxMM_mainshuffle_shuffleWonderItemsMm: OOTxMM_mainshuffle_shuffleWonderItemsMm
    OOTxMM_mainshuffle_shuffleSnowballsMm: OOTxMM_mainshuffle_shuffleSnowballsMm
    OOTxMM_mainshuffle_shuffleButterfliesOot: OOTxMM_mainshuffle_shuffleButterfliesOot
    OOTxMM_mainshuffle_shuffleButterfliesMm: OOTxMM_mainshuffle_shuffleButterfliesMm
    OOTxMM_mainshuffle_shuffleRedBouldersOot: OOTxMM_mainshuffle_shuffleRedBouldersOot
    OOTxMM_mainshuffle_shuffleRedBouldersMm: OOTxMM_mainshuffle_shuffleRedBouldersMm
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
    OOTxMM_mainevents_startingAge: OOTxMM_mainevents_startingAge
    OOTxMM_mainevents_swordlessAdult: OOTxMM_mainevents_swordlessAdult
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
    OOTxMM_itemsextensions_fillWallets: OOTxMM_itemsextensions_fillWallets
    OOTxMM_itemsextensions_bottleContentShuffle: OOTxMM_itemsextensions_bottleContentShuffle
    OOTxMM_itemsextensions_stoneAgonyMm: OOTxMM_itemsextensions_stoneAgonyMm
    OOTxMM_itemsextensions_sticksNutsUpgradesMm: OOTxMM_itemsextensions_sticksNutsUpgradesMm
    OOTxMM_itemsextensions_fairyOcarinaMm: OOTxMM_itemsextensions_fairyOcarinaMm
    OOTxMM_itemsextensions_blueFireArrows: OOTxMM_itemsextensions_blueFireArrows
    OOTxMM_itemsextensions_iceArrowPlatformsOot: OOTxMM_itemsextensions_iceArrowPlatformsOot
    OOTxMM_itemsextensions_sunlightArrows: OOTxMM_itemsextensions_sunlightArrows
    OOTxMM_itemsextensions_shortHookshotMm: OOTxMM_itemsextensions_shortHookshotMm
    OOTxMM_itemsextensions_bronzeScale: OOTxMM_itemsextensions_bronzeScale
    OOTxMM_itemsextensions_childWallets: OOTxMM_itemsextensions_childWallets
    OOTxMM_itemsextensions_colossalWallets: OOTxMM_itemsextensions_colossalWallets
    OOTxMM_itemsextensions_bottomlessWallets: OOTxMM_itemsextensions_bottomlessWallets
    OOTxMM_itemsextensions_rupeeScaling: OOTxMM_itemsextensions_rupeeScaling
    OOTxMM_itemsextensions_skeletonKeyOot: OOTxMM_itemsextensions_skeletonKeyOot
    OOTxMM_itemsextensions_skeletonKeyMm: OOTxMM_itemsextensions_skeletonKeyMm
    OOTxMM_itemsextensions_magicalRupee: OOTxMM_itemsextensions_magicalRupee
    OOTxMM_itemsextensions_transcendentFairy: OOTxMM_itemsextensions_transcendentFairy
    OOTxMM_itemsextensions_platinumTokenOot: OOTxMM_itemsextensions_platinumTokenOot
    OOTxMM_itemsextensions_platinumTokenMm: OOTxMM_itemsextensions_platinumTokenMm
    OOTxMM_itemsextensions_bombchuBehaviorOot: OOTxMM_itemsextensions_bombchuBehaviorOot
    OOTxMM_itemsextensions_bombchuBehaviorMm: OOTxMM_itemsextensions_bombchuBehaviorMm
    OOTxMM_itemsextensions_spellFireMm: OOTxMM_itemsextensions_spellFireMm
    OOTxMM_itemsextensions_spellWindMm: OOTxMM_itemsextensions_spellWindMm
    OOTxMM_itemsextensions_spellLoveMm: OOTxMM_itemsextensions_spellLoveMm
    OOTxMM_itemsextensions_bootsIronMm: OOTxMM_itemsextensions_bootsIronMm
    OOTxMM_itemsextensions_bootsHoverMm: OOTxMM_itemsextensions_bootsHoverMm
    OOTxMM_itemsextensions_tunicGoronMm: OOTxMM_itemsextensions_tunicGoronMm
    OOTxMM_itemsextensions_tunicZoraMm: OOTxMM_itemsextensions_tunicZoraMm
    OOTxMM_itemsextensions_scalesMm: OOTxMM_itemsextensions_scalesMm
    OOTxMM_itemsextensions_strengthMm: OOTxMM_itemsextensions_strengthMm
    OOTxMM_itemsextensions_kegStrength3: OOTxMM_itemsextensions_kegStrength3
    OOTxMM_itemsextensions_hammerMm: OOTxMM_itemsextensions_hammerMm
    OOTxMM_itemsextensions_boomerangMm: OOTxMM_itemsextensions_boomerangMm
    OOTxMM_itemsextensions_gfsOot: OOTxMM_itemsextensions_gfsOot
    OOTxMM_itemsextensions_slingshotMm: OOTxMM_itemsextensions_slingshotMm
    OOTxMM_itemsextensions_spinUpgradeOot: OOTxMM_itemsextensions_spinUpgradeOot
    OOTxMM_itemsextensions_extraChildSwordsOot: OOTxMM_itemsextensions_extraChildSwordsOot
    OOTxMM_itemsextensions_dekuShieldMm: OOTxMM_itemsextensions_dekuShieldMm
    OOTxMM_itemsextensions_blastMaskOot: OOTxMM_itemsextensions_blastMaskOot
    OOTxMM_itemsextensions_stoneMaskOot: OOTxMM_itemsextensions_stoneMaskOot
    OOTxMM_itemsextensions_kamaroMaskOot: OOTxMM_itemsextensions_kamaroMaskOot
    OOTxMM_itemsextensions_elegyOot: OOTxMM_itemsextensions_elegyOot
    OOTxMM_itemsextensions_songSoaringOot: OOTxMM_itemsextensions_songSoaringOot
    OOTxMM_itemsextensions_songHealingOot: OOTxMM_itemsextensions_songHealingOot
    OOTxMM_itemsextensions_songAwakeningOot: OOTxMM_itemsextensions_songAwakeningOot
    OOTxMM_itemsextensions_songGoronOot: OOTxMM_itemsextensions_songGoronOot
    OOTxMM_itemsextensions_songZoraOot: OOTxMM_itemsextensions_songZoraOot
    OOTxMM_itemsextensions_songOrderOot: OOTxMM_itemsextensions_songOrderOot
    OOTxMM_itemsextensions_songSunMm: OOTxMM_itemsextensions_songSunMm
    OOTxMM_itemsextensions_songZeldaLullabyMm: OOTxMM_itemsextensions_songZeldaLullabyMm
    OOTxMM_itemsextensions_songSariasMm: OOTxMM_itemsextensions_songSariasMm
    OOTxMM_itemsextensions_songMinuetMm: OOTxMM_itemsextensions_songMinuetMm
    OOTxMM_itemsextensions_songBoleroMm: OOTxMM_itemsextensions_songBoleroMm
    OOTxMM_itemsextensions_songSerenadeMm: OOTxMM_itemsextensions_songSerenadeMm
    OOTxMM_itemsextensions_songRequiemMm: OOTxMM_itemsextensions_songRequiemMm
    OOTxMM_itemsextensions_songNocturneMm: OOTxMM_itemsextensions_songNocturneMm
    OOTxMM_itemsextensions_songPreludeMm: OOTxMM_itemsextensions_songPreludeMm
    OOTxMM_itemsextensions_powderKegOot: OOTxMM_itemsextensions_powderKegOot
    OOTxMM_itemsextensions_ocarinaButtonsShuffleOot: OOTxMM_itemsextensions_ocarinaButtonsShuffleOot
    OOTxMM_itemsextensions_ocarinaButtonsShuffleMm: OOTxMM_itemsextensions_ocarinaButtonsShuffleMm
    OOTxMM_itemsextensions_soulsEnemyOot: OOTxMM_itemsextensions_soulsEnemyOot
    OOTxMM_itemsextensions_soulsEnemyMm: OOTxMM_itemsextensions_soulsEnemyMm
    OOTxMM_itemsextensions_soulsBossOot: OOTxMM_itemsextensions_soulsBossOot
    OOTxMM_itemsextensions_soulsBossMm: OOTxMM_itemsextensions_soulsBossMm
    OOTxMM_itemsextensions_soulsNpcOot: OOTxMM_itemsextensions_soulsNpcOot
    OOTxMM_itemsextensions_soulsNpcMm: OOTxMM_itemsextensions_soulsNpcMm
    OOTxMM_itemsextensions_soulsAnimalOot: OOTxMM_itemsextensions_soulsAnimalOot
    OOTxMM_itemsextensions_soulsAnimalMm: OOTxMM_itemsextensions_soulsAnimalMm
    OOTxMM_itemsextensions_soulsMiscOot: OOTxMM_itemsextensions_soulsMiscOot
    OOTxMM_itemsextensions_soulsMiscMm: OOTxMM_itemsextensions_soulsMiscMm
    OOTxMM_itemsextensions_rustyKeysOot: OOTxMM_itemsextensions_rustyKeysOot
    OOTxMM_itemsextensions_rustyKeysMm: OOTxMM_itemsextensions_rustyKeysMm
    OOTxMM_itemsextensions_clocks: OOTxMM_itemsextensions_clocks
    OOTxMM_itemsextensions_menuNotebook: OOTxMM_itemsextensions_menuNotebook
    OOTxMM_itemsextensions_coins: OOTxMM_itemsextensions_coins
    OOTxMM_itemsextensions_coinsRed: OOTxMM_itemsextensions_coinsRed
    OOTxMM_itemsextensions_coinsGreen: OOTxMM_itemsextensions_coinsGreen
    OOTxMM_itemsextensions_coinsBlue: OOTxMM_itemsextensions_coinsBlue
    OOTxMM_itemsextensions_coinsYellow: OOTxMM_itemsextensions_coinsYellow
    OOTxMM_itemsextensions_trapIce: OOTxMM_itemsextensions_trapIce
    OOTxMM_itemsextensions_trapFire: OOTxMM_itemsextensions_trapFire
    OOTxMM_itemsextensions_trapShock: OOTxMM_itemsextensions_trapShock
    OOTxMM_itemsextensions_trapDrain: OOTxMM_itemsextensions_trapDrain
    OOTxMM_itemsextensions_trapAntiMagic: OOTxMM_itemsextensions_trapAntiMagic
    OOTxMM_itemsextensions_trapKnockback: OOTxMM_itemsextensions_trapKnockback
    OOTxMM_itemsextensions_trapRupoor: OOTxMM_itemsextensions_trapRupoor
    OOTxMM_itemsextensions_cloakTraps: OOTxMM_itemsextensions_cloakTraps
    OOTxMM_itemsextensions_trapsQuantity: OOTxMM_itemsextensions_trapsQuantity
    OOTxMM_main_trapsLink: OOTxMM_main_trapsLink
    OOTxMM_itemsextensions_songOfDoubleTimeOot: OOTxMM_itemsextensions_songOfDoubleTimeOot
    OOTxMM_itemsshared_sharedStoneAgony: OOTxMM_itemsshared_sharedStoneAgony
    OOTxMM_itemsshared_sharedSpinUpgrade: OOTxMM_itemsshared_sharedSpinUpgrade
    OOTxMM_itemsshared_sharedNutsSticks: OOTxMM_itemsshared_sharedNutsSticks
    OOTxMM_itemsshared_sharedBows: OOTxMM_itemsshared_sharedBows
    OOTxMM_itemsshared_sharedBombBags: OOTxMM_itemsshared_sharedBombBags
    OOTxMM_itemsshared_sharedMagic: OOTxMM_itemsshared_sharedMagic
    OOTxMM_itemsshared_sharedMagicArrowFire: OOTxMM_itemsshared_sharedMagicArrowFire
    OOTxMM_itemsshared_sharedMagicArrowIce: OOTxMM_itemsshared_sharedMagicArrowIce
    OOTxMM_itemsshared_sharedMagicArrowLight: OOTxMM_itemsshared_sharedMagicArrowLight
    OOTxMM_itemsshared_sharedSongEpona: OOTxMM_itemsshared_sharedSongEpona
    OOTxMM_itemsshared_sharedSongStorms: OOTxMM_itemsshared_sharedSongStorms
    OOTxMM_itemsshared_sharedSongTime: OOTxMM_itemsshared_sharedSongTime
    OOTxMM_itemsshared_sharedSongSun: OOTxMM_itemsshared_sharedSongSun
    OOTxMM_itemsshared_sharedHookshot: OOTxMM_itemsshared_sharedHookshot
    OOTxMM_itemsshared_sharedLens: OOTxMM_itemsshared_sharedLens
    OOTxMM_itemsshared_sharedOcarina: OOTxMM_itemsshared_sharedOcarina
    OOTxMM_itemsshared_sharedMaskGoron: OOTxMM_itemsshared_sharedMaskGoron
    OOTxMM_itemsshared_sharedMaskZora: OOTxMM_itemsshared_sharedMaskZora
    OOTxMM_itemsshared_sharedMaskBunny: OOTxMM_itemsshared_sharedMaskBunny
    OOTxMM_itemsshared_sharedMaskKeaton: OOTxMM_itemsshared_sharedMaskKeaton
    OOTxMM_itemsshared_sharedMaskTruth: OOTxMM_itemsshared_sharedMaskTruth
    OOTxMM_itemsshared_sharedMaskBlast: OOTxMM_itemsshared_sharedMaskBlast
    OOTxMM_itemsshared_sharedMaskStone: OOTxMM_itemsshared_sharedMaskStone
    OOTxMM_itemsshared_sharedMaskKamaro: OOTxMM_itemsshared_sharedMaskKamaro
    OOTxMM_itemsshared_sharedSongElegy: OOTxMM_itemsshared_sharedSongElegy
    OOTxMM_itemsshared_sharedSongHealing: OOTxMM_itemsshared_sharedSongHealing
    OOTxMM_itemsshared_sharedSongSoaring: OOTxMM_itemsshared_sharedSongSoaring
    OOTxMM_itemsshared_sharedSongAwakening: OOTxMM_itemsshared_sharedSongAwakening
    OOTxMM_itemsshared_sharedSongGoron: OOTxMM_itemsshared_sharedSongGoron
    OOTxMM_itemsshared_sharedSongZora: OOTxMM_itemsshared_sharedSongZora
    OOTxMM_itemsshared_sharedSongOrder: OOTxMM_itemsshared_sharedSongOrder
    OOTxMM_itemsshared_sharedSongZeldaLullaby: OOTxMM_itemsshared_sharedSongZeldaLullaby
    OOTxMM_itemsshared_sharedSongSarias: OOTxMM_itemsshared_sharedSongSarias
    OOTxMM_itemsshared_sharedSongMinuet: OOTxMM_itemsshared_sharedSongMinuet
    OOTxMM_itemsshared_sharedSongBolero: OOTxMM_itemsshared_sharedSongBolero
    OOTxMM_itemsshared_sharedSongSerenade: OOTxMM_itemsshared_sharedSongSerenade
    OOTxMM_itemsshared_sharedSongRequiem: OOTxMM_itemsshared_sharedSongRequiem
    OOTxMM_itemsshared_sharedSongNocturne: OOTxMM_itemsshared_sharedSongNocturne
    OOTxMM_itemsshared_sharedSongPrelude: OOTxMM_itemsshared_sharedSongPrelude
    OOTxMM_itemsshared_sharedPowderKeg: OOTxMM_itemsshared_sharedPowderKeg
    OOTxMM_itemsshared_sharedWallets: OOTxMM_itemsshared_sharedWallets
    OOTxMM_itemsshared_sharedHealth: OOTxMM_itemsshared_sharedHealth
    OOTxMM_itemsshared_sharedSwords: OOTxMM_itemsshared_sharedSwords
    OOTxMM_itemsshared_sharedShields: OOTxMM_itemsshared_sharedShields
    OOTxMM_itemsshared_sharedSoulsEnemy: OOTxMM_itemsshared_sharedSoulsEnemy
    OOTxMM_itemsshared_sharedSoulsNpc: OOTxMM_itemsshared_sharedSoulsNpc
    OOTxMM_itemsshared_sharedSoulsAnimal: OOTxMM_itemsshared_sharedSoulsAnimal
    OOTxMM_itemsshared_sharedSoulsMisc: OOTxMM_itemsshared_sharedSoulsMisc
    OOTxMM_itemsshared_sharedOcarinaButtons: OOTxMM_itemsshared_sharedOcarinaButtons
    OOTxMM_itemsshared_sharedSkeletonKey: OOTxMM_itemsshared_sharedSkeletonKey
    OOTxMM_itemsshared_sharedPlatinumToken: OOTxMM_itemsshared_sharedPlatinumToken
    OOTxMM_itemsshared_sharedBombchu: OOTxMM_itemsshared_sharedBombchu
    OOTxMM_itemsshared_sharedSpellFire: OOTxMM_itemsshared_sharedSpellFire
    OOTxMM_itemsshared_sharedSpellWind: OOTxMM_itemsshared_sharedSpellWind
    OOTxMM_itemsshared_sharedSpellLove: OOTxMM_itemsshared_sharedSpellLove
    OOTxMM_itemsshared_sharedBootsIron: OOTxMM_itemsshared_sharedBootsIron
    OOTxMM_itemsshared_sharedBootsHover: OOTxMM_itemsshared_sharedBootsHover
    OOTxMM_itemsshared_sharedTunicGoron: OOTxMM_itemsshared_sharedTunicGoron
    OOTxMM_itemsshared_sharedTunicZora: OOTxMM_itemsshared_sharedTunicZora
    OOTxMM_itemsshared_sharedScales: OOTxMM_itemsshared_sharedScales
    OOTxMM_itemsshared_sharedStrength: OOTxMM_itemsshared_sharedStrength
    OOTxMM_itemsshared_sharedHammer: OOTxMM_itemsshared_sharedHammer
    OOTxMM_itemsshared_sharedBoomerang: OOTxMM_itemsshared_sharedBoomerang
    OOTxMM_itemsshared_sharedGFS: OOTxMM_itemsshared_sharedGFS
    OOTxMM_itemsshared_sharedSlingshot: OOTxMM_itemsshared_sharedSlingshot
    OOTxMM_itemsshared_sharedBottles: OOTxMM_itemsshared_sharedBottles
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
    OOTxMM_mainqol_critWiggleDisable: OOTxMM_mainqol_critWiggleDisable
    OOTxMM_mainqol_fastMasks: OOTxMM_mainqol_fastMasks
    OOTxMM_mainqol_keepItemsReset: OOTxMM_mainqol_keepItemsReset
    OOTxMM_mainqol_keepBottlesReset: OOTxMM_mainqol_keepBottlesReset
    OOTxMM_mainqol_autoInvert: OOTxMM_mainqol_autoInvert

option_groups = []

option_presets = {}

