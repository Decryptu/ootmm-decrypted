# Roadmap

What is in progress and planned. Finished work is not listed: git history has it. Add a row when work starts, delete it when the item is done ([DEVELOPMENT.md](DEVELOPMENT.md#conventions)).

## Goal
A world a group can play a full multiworld with: generation in Archipelago, a patched OoTMM ROM per player, and a client that sends and receives items in game.

## In progress

| Item | Notes |
|---|---|
| Dolphin + Virtual Console evaluation (paused) | The experimental NARE build passed OoT mailbox item delivery and chest reporting. The Market door selected South Clock Town and stalled at the RSP status poll. A diagnostic build reached the final MM handoff and faulted before gameplay. The [evaluation guide](docs/dolphin_evaluation.md) records both results. Resolve the handoff, then verify MM mailbox reattachment, the return trip and save persistence before implementing the connector or publishing player setup. Project64 remains outside the roadmap. |

The hub lists every changed setting it cannot import. Newly ported settings can be imported once they are in `options.py`.

## Decisions
- Keep the game name `OOTxMM` and upstream's file layout, so Quasky's work can still be merged if AP-OOTMM resumes ([Syncing upstream](DEVELOPMENT.md#syncing-upstream)).
- Logic comes from OoTMM's data through `raw/GenerateMetadata.py`, not hand-written rules, so it follows OoTMM updates.
- Use OoTMM as released wherever possible: it is the data source for metadata (a checkout in `raw/ootmm`, ignored) and the ROM builder. Track one release at a time, currently v33.0. Change OoTMM only for what the patch or client needs, as patches in `ootmm-patches/` ([DEVELOPMENT.md](DEVELOPMENT.md#our-ootmm-changes)), and offer them upstream.
- Generate OoTMM's default world variant only: vanilla dungeons (no Master Quest) and the US Deku Palace. MQ and `jpLayouts` are not offered until the world can pick world files per option.
- Target Archipelago 0.6.8 (`archipelago.json`, CI and `tools/apworld-test.ps1` pin the same commit).
