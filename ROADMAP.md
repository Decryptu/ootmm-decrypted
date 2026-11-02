# Roadmap

What is in progress and planned. Finished work is not listed: git history has it. Add a row when work starts, delete it when the item is done ([DEVELOPMENT.md](DEVELOPMENT.md#conventions)).

## Goal
A world a group can play a full multiworld with: generation in Archipelago, a patched OoTMM ROM per player, and a client that sends and receives items in game.

## Planned, in order
| Item | Notes |
|---|---|
| World loads in Archipelago | It fails at import: `options.py` has Choice options with a `random` value (first: `OOTxMM_mainprices_priceOotShops`), which Archipelago forbids. Fix it in `raw/GenerateMetadata.py`'s option conversion (map OoTMM's `random` to Archipelago's own random handling), then regenerate. The World workflow is red until then |
| Clean up generation output | `regions.py` and `locations.py` print every region and location on import and swallow errors with bare `except`. Remove the prints; let a bad name fail |
| Location IDs | IDs are a counter over the JSON's iteration order, so they shift whenever OoTMM data changes. Give each location a stable ID derived from its OoTMM check, like the item scheme |
| Items from OoTMM data | `items.py` is hand-written. Check it against OoTMM's item list and pool rules per option |
| Logic | `rules.py` still holds the Archipelago example world's rules, unused. Translate OoTMM's world-file conditions and macros (`raw/GreatMacroJSONdump.json`) into access rules |
| Options | Only keep options that make sense in a multiworld (`raw/Meta_ForbiddenOptions.py` lists the excluded ones), and pass them to the patch |
| Goal | The completion condition is a placeholder `BEAT MAJORA` event on `Moon`; follow the `main_goal` option (Ganon, Majora, both, Triforce) |
| ROM patch | Produce a per-player patch file that OoTMM's generator turns into the combo ROM, with this seed's item placements |
| Client | Item send/receive with the running game (emulator connector, likely BizHawk like the other N64 worlds) |
| Game and setup pages | `docs/en_OOTxMM.md` and `docs/setup_en.md` are stubs |

## Decisions
- Keep the game name `OOTxMM` and upstream's file layout, so Quasky's work can still be merged if AP-OOTMM resumes ([Syncing upstream](DEVELOPMENT.md#syncing-upstream)).
- Logic comes from OoTMM's data through `raw/GenerateMetadata.py`, not hand-written rules, so it follows OoTMM updates.
- Target Archipelago 0.6.8 (`archipelago.json`, CI and `tools/apworld-test.ps1` pin the same commit).
