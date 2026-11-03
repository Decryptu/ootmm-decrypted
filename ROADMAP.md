# Roadmap

What is in progress and planned. Finished work is not listed: git history has it. Add a row when work starts, delete it when the item is done ([DEVELOPMENT.md](DEVELOPMENT.md#conventions)).

## Goal
A world a group can play a full multiworld with: generation in Archipelago, a patched OoTMM ROM per player, and a client that sends and receives items in game.

## Planned, in order
The first playable release needs everything up to the game and setup pages. The rest can follow it.
| Item | Notes |
|---|---|
| Player setup | Players need their ROM without the OoTMM toolchain. The ROM patch works ([DEVELOPMENT.md](DEVELOPMENT.md#rom-patch)) but runs in the toolchain under WSL. Either the host builds each player's `.ootmm` patch file and players build the ROM with an OoTMM patch mode of the same release, or the patch script is packaged to run with plain Node; decide with the client, then write it up in the setup page |
| Client | Written ([DEVELOPMENT.md](DEVELOPMENT.md#client)). In BizHawk 2.11.1 it attaches, connects and the game takes a received item; a check reported from the game is only tested against a simulated mailbox. Then: keep the goal across client restarts (`goal: both`), and check that the 2 KB rings are enough while playing |
| Game and setup pages | `docs/en_OOTxMM.md` and `docs/setup_en.md` are stubs |
| More options | The world offers the settings that only change conditions or the ROM ([DEVELOPMENT.md](DEVELOPMENT.md#options)). The rest (the `port` class in `raw/SettingsClasses.json`) change which checks exist, the pool or the world's shape: port each with what `run()` in OoTMM's `packages/logic/src/world/transform.ts` does for it (check filters, souls, keys, shared items, `itemPool`), then add it to `Ported` ([DEVELOPMENT.md](DEVELOPMENT.md#options)). The check filters are ported, and items are placed as OoTMM's defaults place them ([Placement](DEVELOPMENT.md#placement)); the pool is otherwise OoTMM's base pool, so pool changes (souls, keys, shared items, `itemPool`, `pondFishShuffle`, the Triforce values of `goal`) and the placement settings (keysanity and the like) come next |
| Time of day | Time and flag conditions count as met ([DEVELOPMENT.md](DEVELOPMENT.md#logic)), so a seed can expect something at a time the route can't reach (mostly MM's clock). Model OoTMM's per-area time ranges in the state, or at least make the conditions that only one time slice meets false |

## Decisions
- Keep the game name `OOTxMM` and upstream's file layout, so Quasky's work can still be merged if AP-OOTMM resumes ([Syncing upstream](DEVELOPMENT.md#syncing-upstream)).
- Logic comes from OoTMM's data through `raw/GenerateMetadata.py`, not hand-written rules, so it follows OoTMM updates.
- Use OoTMM as released wherever possible: it is the data source for metadata (a checkout in `raw/ootmm`, ignored) and the ROM builder. Track one release at a time, currently v33.0. Change OoTMM only for what the patch or client needs, as patches in `ootmm-patches/` ([DEVELOPMENT.md](DEVELOPMENT.md#our-ootmm-changes)), and offer them upstream.
- Generate OoTMM's default world variant only: vanilla dungeons (no Master Quest) and the US Deku Palace. MQ and `jpLayouts` are not offered until the world can pick world files per option.
- Target Archipelago 0.6.8 (`archipelago.json`, CI and `tools/apworld-test.ps1` pin the same commit).
