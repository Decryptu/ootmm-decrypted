# Roadmap

What is in progress and planned. Finished work is not listed: git history has it. Add a row when work starts, delete it when the item is done ([DEVELOPMENT.md](DEVELOPMENT.md#conventions)).

## Goal
A world a group can play a full multiworld with: generation in Archipelago, a patched OoTMM ROM per player, and a client that sends and receives items in game.

## Planned, in order

Remaining gameplay checks use [the playtest checklist](docs/playtest_en.md) and [disposable gameplay tests](docs/gameplay_testing.md). No group playtest is planned.
The ordered developer tasks and validation gates are in [release readiness](docs/release_checklist.md), starting with isolated, repeatable gameplay setups and source-verified test shortcuts. The standalone gameplay observer records mailbox recovery and client-poll timings for game-switch validation ([measurement limits](docs/gameplay_testing.md)).
Release hardening still needs a full playthrough and the remaining gameplay checks below. Additional options can follow the current alpha releases.
| Item | Notes |
|---|---|
| Client | Implemented ([DEVELOPMENT.md](DEVELOPMENT.md#client)); remaining gameplay gates include fairy rewards, shared equipment abilities, continuous native completion/credits and other goal settings. Current source, exchange, native inventory, OoT and MM remote small-key, dungeon boss-key and Ganon-key doors, boss blue-warp and recovery/load coverage is recorded in [release readiness](docs/release_checklist.md). [Disposable gameplay tests](docs/gameplay_testing.md) defines the isolated setup, assistance and assertion limits |
| More options | The world offers condition/ROM settings and the check, placement and pool changes listed in [Options](DEVELOPMENT.md#options). Unported settings retain OoTMM defaults. Port each remaining setting with the relevant behavior in OoTMM's `world/transform.ts` and `misc/fixer.ts`, then add it to `Ported` in `raw/Meta_Options.py` and regenerate metadata. Remaining pool changes include other shared items, `itemPool`, `pondFishShuffle` and the Triforce values of `goal` |
| Gossip stone hints | Gossip stones only show OoTMM's junk (joke) hints, because OoTMM's hint pass needs a playthrough of the whole seed ([ROM patch](DEVELOPMENT.md#rom-patch)); a tester read them as broken. Archipelago knows the whole multiworld at generation: compute way-of-the-hero, foolish and item hints there (from the spheres and required locations, across worlds) and pass them to `ap-patch.ts` as gossip texts |
| Dolphin + Virtual Console (to evaluate, after the alpha) | Players asked for Dolphin with a `.wad`, which gives better picture, latency and audio sync than BizHawk's N64 core. Needs a client on `dolphin-memory-engine` (as Archipelago's existing Dolphin worlds use) instead of the BizHawk connector, finding the IPC mailbox in the VC emulator's RAM by its magic, checking OoTMM runs correctly under the VC emulator, and a player guide for building the WAD from the patched ROM. Project64 would need a new connector too and is not planned |

Next options: the remaining shared equipment and songs (including Zelda's Lullaby, Saria's Song and warp songs), including pool counts and logic behavior; shared ocarinas, wallets and health need their own pool rules, while cross-game equipment needs its enabling settings ported together. The hub lists every changed setting it cannot import, so a newly ported setting is imported once it is in `options.py`.

## Decisions
- Keep the game name `OOTxMM` and upstream's file layout, so Quasky's work can still be merged if AP-OOTMM resumes ([Syncing upstream](DEVELOPMENT.md#syncing-upstream)).
- Logic comes from OoTMM's data through `raw/GenerateMetadata.py`, not hand-written rules, so it follows OoTMM updates.
- Use OoTMM as released wherever possible: it is the data source for metadata (a checkout in `raw/ootmm`, ignored) and the ROM builder. Track one release at a time, currently v33.0. Change OoTMM only for what the patch or client needs, as patches in `ootmm-patches/` ([DEVELOPMENT.md](DEVELOPMENT.md#our-ootmm-changes)), and offer them upstream.
- Generate OoTMM's default world variant only: vanilla dungeons (no Master Quest) and the US Deku Palace. MQ and `jpLayouts` are not offered until the world can pick world files per option.
- Target Archipelago 0.6.8 (`archipelago.json`, CI and `tools/apworld-test.ps1` pin the same commit).
