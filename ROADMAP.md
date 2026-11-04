# Roadmap

What is in progress and planned. Finished work is not listed: git history has it. Add a row when work starts, delete it when the item is done ([DEVELOPMENT.md](DEVELOPMENT.md#conventions)).

## Goal
A world a group can play a full multiworld with: generation in Archipelago, a patched OoTMM ROM per player, and a client that sends and receives items in game.

## Planned, in order
The first playable release needs the client work and player hub validation. The remaining options can follow it.
| Item | Notes |
|---|---|
| Client | Written ([DEVELOPMENT.md](DEVELOPMENT.md#client)). In BizHawk 2.11.1 it attaches, connects and the game takes a received item. Check reporting and boss packets still need gameplay verification; boss persistence passes against a real server with a simulated mailbox. Check that the 2 KB rings are enough while playing |
| Player hub deployment | Guides and a starter YAML download are in `site/`, built from the shared `docs/` pages. GitHub Pages uses GitHub Actions; put the Player hub workflow on `main` to deploy and verify the first deployment |
| Next options: Hideout and chest-game keys | Port `smallKeyShuffleHideout` and `smallKeyShuffleChestGame`: vanilla, own-dungeon/minigame and anywhere placement. Match OoTMM's fixed checks and pool restrictions, regenerate symbolic logic, then test mixed settings and build a seed and ROM. Both currently retain their defaults. |
| More options | The world offers the settings that only change conditions or the ROM ([DEVELOPMENT.md](DEVELOPMENT.md#options)). The rest (the `port` class in `raw/SettingsClasses.json`) change which checks exist, the pool or the world's shape: port each with what `run()` in OoTMM's `packages/logic/src/world/transform.ts` does for it (check filters, souls, keys, shared items, `itemPool`), then add it to `Ported` ([DEVELOPMENT.md](DEVELOPMENT.md#options)). The check filters, Tingle map modes and map/compass, regular small-key, boss-key (including Ganon), stray-fairy, song and blue-warp, dungeon-only (with or without a one-reward limit) and anywhere reward placement are ported; other items follow OoTMM's defaults ([Placement](DEVELOPMENT.md#placement)); the pool is otherwise OoTMM's base pool, so pool changes (souls, keys, shared items, `itemPool`, `pondFishShuffle`, the Triforce values of `goal`) come next |

## Decisions
- Keep the game name `OOTxMM` and upstream's file layout, so Quasky's work can still be merged if AP-OOTMM resumes ([Syncing upstream](DEVELOPMENT.md#syncing-upstream)).
- Logic comes from OoTMM's data through `raw/GenerateMetadata.py`, not hand-written rules, so it follows OoTMM updates.
- Use OoTMM as released wherever possible: it is the data source for metadata (a checkout in `raw/ootmm`, ignored) and the ROM builder. Track one release at a time, currently v33.0. Change OoTMM only for what the patch or client needs, as patches in `ootmm-patches/` ([DEVELOPMENT.md](DEVELOPMENT.md#our-ootmm-changes)), and offer them upstream.
- Generate OoTMM's default world variant only: vanilla dungeons (no Master Quest) and the US Deku Palace. MQ and `jpLayouts` are not offered until the world can pick world files per option.
- Target Archipelago 0.6.8 (`archipelago.json`, CI and `tools/apworld-test.ps1` pin the same commit).
