# Roadmap

What is in progress and planned. Finished work is not listed: git history has it. Add a row when work starts, delete it when the item is done ([DEVELOPMENT.md](DEVELOPMENT.md#conventions)).

## Goal
A world a group can play a full multiworld with: generation in Archipelago, a patched OoTMM ROM per player, and a client that sends and receives items in game.

## Planned, in order
The first playable release needs everything up to the setup pages. The rest can follow it.
| Item | Notes |
|---|---|
| Build toolchain | `tools/` script that builds OoTMM (its C payload needs a MIPS toolchain; on Windows, through WSL), so the fork below and the patch can be built and tested here |
| OoTMM fork: RAM IPC | OoTMM's multiworld code talks only to its own Project64 build, through cartridge I/O registers (`packages/generator/src/common/ipc/project64.c`). With multiplayer on and no connection, the second item sent waits forever for an ack (`Multi_EnsureSendBufferEmpty` in `src/common/multi/multi.c`), so the game locks. Add an IPC backend next to `project64.c` that exchanges the same packets through a mailbox in RDRAM, which a BizHawk client can read and write. Small and self-contained: offer it upstream |
| ROM patch | Per player: a Node script run on OoTMM's generator that runs its pipeline with the player's `settings` (`fill_slot_data`), then replaces the placements with the seed's: our items with `player` = our world, other players' items as a placeholder item for world 2, so the game hands them to the multiworld code. Output is OoTMM's `.ootmm` patch file, built into a ROM by the player with OoTMM's patch mode |
| Client | Python client on Archipelago's BizHawk connector (`worlds/_bizhawk`). It speaks OoTMM's multiworld protocol (`src/common/multi/multi.h`: HELLO, WAL items, ACK) through the RAM mailbox: outgoing WAL items become checked locations (by check key), received items become incoming WAL items, reaching the goal (`OOT_GANON`, `MM_MAJORA`) is reported as the goal |
| Game and setup pages | `docs/en_OOTxMM.md` and `docs/setup_en.md` are stubs |
| More options | The world offers the settings that only change conditions or the ROM ([DEVELOPMENT.md](DEVELOPMENT.md#options)). The rest (the `port` class in `raw/SettingsClasses.json`) change which checks exist, the pool or the world's shape: port each with what `run()` in OoTMM's `packages/logic/src/world/transform.ts` does for it (check filters, souls, keys, shared items, `itemPool`), then add it to `Ported` ([DEVELOPMENT.md](DEVELOPMENT.md#options)). The check filters are ported; the pool is still OoTMM's base pool, so pool changes (souls, keys, shared items, `itemPool`, `pondFishShuffle`, the Triforce values of `goal`) come next |
| Time of day | Time and flag conditions count as met ([DEVELOPMENT.md](DEVELOPMENT.md#logic)), so a seed can expect something at a time the route can't reach (mostly MM's clock). Model OoTMM's per-area time ranges in the state, or at least make the conditions that only one time slice meets false |

## Decisions
- Keep the game name `OOTxMM` and upstream's file layout, so Quasky's work can still be merged if AP-OOTMM resumes ([Syncing upstream](DEVELOPMENT.md#syncing-upstream)).
- Logic comes from OoTMM's data through `raw/GenerateMetadata.py`, not hand-written rules, so it follows OoTMM updates.
- Use OoTMM as released wherever possible: it is the data source for metadata (a checkout in `raw/ootmm`, ignored) and the ROM builder. Track one release at a time, currently v33.0. Fork OoTMM only for what the patch or client needs: the RAM IPC backend (planned above) is the one change so far, and it should go upstream.
- Generate OoTMM's default world variant only: vanilla dungeons (no Master Quest) and the US Deku Palace. MQ and `jpLayouts` are not offered until the world can pick world files per option.
- Target Archipelago 0.6.8 (`archipelago.json`, CI and `tools/apworld-test.ps1` pin the same commit).
