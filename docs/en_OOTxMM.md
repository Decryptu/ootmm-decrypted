# OOTxMM

Play Ocarina of Time and Majora's Mask in one ROM, sharing items through an Archipelago multiworld. This world uses OoTMM v33.0's regions, checks, items and logic.

Your checks can contain items for other players, and their checks can send items into your game. Choose Ganon, Majora, either boss, or both as your goal. Boss completion is kept on the Archipelago server across client restarts.

## Supported settings

The world offers settings it reproduces in both logic and the ROM: logic and cosmetic settings, tricks, and check shuffles such as pots, grass and rocks. Other settings retain OoTMM's defaults. Maps, compasses, regular dungeon small keys and boss keys can stay in their own dungeon, shuffle anywhere across the multiworld, or be removed. Maps and compasses can also start in your inventory. Tingle maps support vanilla purchases, anywhere in the multiworld, starting inventory, or removal. All four modes retain Tingle's checks. Chest and freestanding dungeon stray fairies independently support vanilla, own dungeon, anywhere or starting inventory. Freestanding fairy checks can also be removed, granting those fairies at the start. Songs can stay on song checks or shuffle anywhere across the multiworld. Individual song notes are not offered. Dungeon rewards can stay on blue warps, shuffle into eligible dungeons across OoTMM players, or shuffle anywhere across the multiworld. Dungeon placement also offers a one-reward-per-dungeon limit. A dungeon containing a limited reward cannot contain another reward, even from another player; Stone Tower and its inverted layout count as one dungeon. Ganon’s boss key can be removed, kept in its vanilla chest, shuffled within Ganon’s Castle and Tower, or shuffled anywhere in the multiworld. Its default is removed; custom requirements are unavailable. Other dungeon items keep default restrictions; some checks keep their vanilla items.

Only vanilla dungeons and the US Deku Palace layout are supported. Master Quest and Japanese layouts are not offered. Logic tracks reachable times per area, including MM's three-day clock and conditional waiting, along with regional flag constraints. Renewable resources and item licenses are approximated by owning the item.

Gossip stones do not give useful hints yet: they show OoTMM's joke messages. OoTMM builds its hints from a playthrough of the whole seed, which a single world in a multiworld cannot run. Fixed hints still work, such as where dungeon rewards, the Light Arrows, the Oath to Order and Ganon's boss key are. Use Archipelago's `!hint` command instead.

## Current status

This is a development build pending a full multiworld play session. Assisted candidate tests verify actual OoT/MM checks, bidirectional item exchange, a cross-game entrance, native key/fairy counters and real Majora/Ganon victory reporting. Server progress survives a restart between the two boss victories and the both-boss slot completes. Earlier-seed tests cover native-save recovery and return travel. A complete unmodified route, wider item/ability coverage, the opposite boss order and other goal settings still need gameplay verification.

Follow the setup guide to install the world, choose settings, obtain your player's patch and connect through Archipelago's BizHawk Client.
