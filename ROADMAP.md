# Roadmap

What is in progress and planned. Finished work is not listed: git history has it. Add a row when work starts, delete it when the item is done ([DEVELOPMENT.md](DEVELOPMENT.md#conventions)).

## Goal
A world a group can play a full multiworld with: generation in Archipelago, a patched OoTMM ROM per player, and a client that sends and receives items in game.

## Planned, in order
| Item | Notes |
|---|---|
| Options | The logic is exported for default settings only: export it per option value, or evaluate settings at generation. Only keep options that make sense in a multiworld (`raw/Meta_ForbiddenOptions.py` lists the excluded ones), and pass them to the patch. Options also decide which checks exist and what the pool holds: the world creates every check (pots, grass and the like, which OoTMM leaves out by default) and uses OoTMM's base pool only. Port `run()` in OoTMM's `packages/logic/src/world/transform.ts` (check filters, souls, keys, shared items, `itemPool` scarce/plentiful) alongside each option |
| Goal | The completion condition is OoTMM's `MM_MAJORA` event; follow the `main_goal` option (Ganon, Majora, both, Triforce) |
| ROM patch | Produce a per-player patch file that OoTMM's generator turns into the combo ROM, with this seed's item placements |
| Client | Item send/receive with the running game (emulator connector, likely BizHawk like the other N64 worlds) |
| Time of day | Time and flag conditions count as met ([DEVELOPMENT.md](DEVELOPMENT.md#logic)), so a seed can expect something at a time the route can't reach (mostly MM's clock). Model OoTMM's per-area time ranges in the state, or at least make the conditions that only one time slice meets false |
| Game and setup pages | `docs/en_OOTxMM.md` and `docs/setup_en.md` are stubs |

## Decisions
- Keep the game name `OOTxMM` and upstream's file layout, so Quasky's work can still be merged if AP-OOTMM resumes ([Syncing upstream](DEVELOPMENT.md#syncing-upstream)).
- Logic comes from OoTMM's data through `raw/GenerateMetadata.py`, not hand-written rules, so it follows OoTMM updates.
- Use OoTMM as released, not a fork: it is the data source for metadata (a checkout in `raw/ootmm`, ignored) and the ROM builder. Track one release at a time, currently v33.0. Fork OoTMM only if the patch or client needs a change OoTMM won't take upstream.
- Generate OoTMM's default world variant only: vanilla dungeons (no Master Quest) and the US Deku Palace. MQ and `jpLayouts` are not offered until the world can pick world files per option.
- Target Archipelago 0.6.8 (`archipelago.json`, CI and `tools/apworld-test.ps1` pin the same commit).
