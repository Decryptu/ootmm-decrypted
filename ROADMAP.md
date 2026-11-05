# Roadmap

What is in progress and planned. Finished work is not listed: git history has it. Add a row when work starts, delete it when the item is done ([DEVELOPMENT.md](DEVELOPMENT.md#conventions)).

## Goal
A world a group can play a full multiworld with: generation in Archipelago, a patched OoTMM ROM per player, and a client that sends and receives items in game.

## Planned, in order

Before the group playtest: verify actual pickups, game switches and boss victories using [the playtest checklist](docs/playtest_en.md). Keep one frozen build for both players.
The ordered developer tasks and validation gates are in [release readiness](docs/release_checklist.md), starting with isolated, repeatable gameplay setups and source-verified test shortcuts.
Release hardening still needs a full multiplayer playthrough and the remaining gameplay checks below. Additional options can follow the first prerelease.
| Item | Notes |
|---|---|
| Client | Implemented ([DEVELOPMENT.md](DEVELOPMENT.md#client)). Assisted candidate gameplay verifies real OoT chest exchange in both directions, an MM song pickup, the normal OoT-to-MM door, native key/fairy counters and actual Majora/Ganon boss packets. Reloading Majora's server progress before Ganon correctly completes a both-boss slot. Earlier-seed tests cover return travel, native-save cold boots, receipt replay protection and disconnected pickup recovery. [Disposable gameplay tests](docs/gameplay_testing.md) records setup assistance and assertion limits. Wider pickup/ability coverage, the opposite boss order, other goal settings, continuous native completion, interrupted sends and sustained ring load remain in [release readiness](docs/release_checklist.md) |
| More options | The world offers the settings that only change conditions or the ROM ([DEVELOPMENT.md](DEVELOPMENT.md#options)). The rest (the `port` class in `raw/SettingsClasses.json`) change which checks exist, the pool or the world's shape: port each with what `run()` in OoTMM's `packages/logic/src/world/transform.ts` does for it (check filters, souls, keys, shared items, `itemPool`), then add it to `Ported` ([DEVELOPMENT.md](DEVELOPMENT.md#options)). The check filters, Tingle map modes and map/compass, regular and Hideout/chest-game small-key, boss-key (including Ganon), stray-fairy, song and blue-warp, dungeon-only (with or without a one-reward limit) and anywhere reward placement are ported; other items follow OoTMM's defaults ([Placement](DEVELOPMENT.md#placement)); separate and shared skeleton keys, small-key rings, enemy, boss, NPC, animal and miscellaneous souls, including shared souls, separate or shared ocarina buttons, and shared bows, bomb bags, magic, elemental arrows, Hookshot, Lens of Truth, and Epona, Storms and Time songs are also ported; remaining pool changes (other shared items, `itemPool`, `pondFishShuffle`, the Triforce values of `goal`) come next |

Next options: the remaining shared equipment and songs, including pool counts and logic behavior.

## Decisions
- Keep the game name `OOTxMM` and upstream's file layout, so Quasky's work can still be merged if AP-OOTMM resumes ([Syncing upstream](DEVELOPMENT.md#syncing-upstream)).
- Logic comes from OoTMM's data through `raw/GenerateMetadata.py`, not hand-written rules, so it follows OoTMM updates.
- Use OoTMM as released wherever possible: it is the data source for metadata (a checkout in `raw/ootmm`, ignored) and the ROM builder. Track one release at a time, currently v33.0. Change OoTMM only for what the patch or client needs, as patches in `ootmm-patches/` ([DEVELOPMENT.md](DEVELOPMENT.md#our-ootmm-changes)), and offer them upstream.
- Generate OoTMM's default world variant only: vanilla dungeons (no Master Quest) and the US Deku Palace. MQ and `jpLayouts` are not offered until the world can pick world files per option.
- Target Archipelago 0.6.8 (`archipelago.json`, CI and `tools/apworld-test.ps1` pin the same commit).
