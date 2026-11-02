# Roadmap

What is in progress and planned. Finished work is not listed: git history has it. Add a row when work starts, delete it when the item is done ([DEVELOPMENT.md](DEVELOPMENT.md#conventions)).

## Goal
A world a group can play a full multiworld with: generation in Archipelago, a patched OoTMM ROM per player, and a client that sends and receives items in game.

## Planned, in order
| Item | Notes |
|---|---|
| Item pool | The items come from OoTMM, but the pool is a placeholder: one of every non-junk item, then random junk. Port OoTMM's pool rules per option (`packages/logic`), and mark which items are progression once the logic exists |
| Logic | `rules.py` still holds the Archipelago example world's rules, unused: every entrance and location is open. Translate OoTMM's world-file conditions and macros (`raw/GreatMacroJSONdump.json`) into access rules, including the per-parent entrances of multi-region checks ([DEVELOPMENT.md](DEVELOPMENT.md#metadata)) |
| Options | Only keep options that make sense in a multiworld (`raw/Meta_ForbiddenOptions.py` lists the excluded ones), and pass them to the patch |
| Goal | The completion condition is a placeholder `BEAT MAJORA` event on `MM Moon`; follow the `main_goal` option (Ganon, Majora, both, Triforce) |
| ROM patch | Produce a per-player patch file that OoTMM's generator turns into the combo ROM, with this seed's item placements |
| Client | Item send/receive with the running game (emulator connector, likely BizHawk like the other N64 worlds) |
| Game and setup pages | `docs/en_OOTxMM.md` and `docs/setup_en.md` are stubs |

## Decisions
- Keep the game name `OOTxMM` and upstream's file layout, so Quasky's work can still be merged if AP-OOTMM resumes ([Syncing upstream](DEVELOPMENT.md#syncing-upstream)).
- Logic comes from OoTMM's data through `raw/GenerateMetadata.py`, not hand-written rules, so it follows OoTMM updates.
- Use OoTMM as released, not a fork: it is the data source for metadata (a checkout in `raw/ootmm`, ignored) and the ROM builder. Track one release at a time, currently v33.0. Fork OoTMM only if the patch or client needs a change OoTMM won't take upstream.
- Generate OoTMM's default world variant only: vanilla dungeons (no Master Quest) and the US Deku Palace. MQ and `jpLayouts` are not offered until the world can pick world files per option.
- Target Archipelago 0.6.8 (`archipelago.json`, CI and `tools/apworld-test.ps1` pin the same commit).
