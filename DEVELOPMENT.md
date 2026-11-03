# Working on OoTMM Decrypted

Everything a new contributor needs, with no other context. Keep it current. [ROADMAP.md](ROADMAP.md) lists what is in progress and planned.

## What this is
- A continuation of [Quasky/AP-OOTMM](https://github.com/Quasky/AP-OOTMM): an Archipelago world (`OOTxMM`) for the [OoTMM](https://github.com/OoTMM/OoTMM) combo randomizer.
- OoTMM's own data (world graph, conditions, items, settings) is converted into the world's metadata by `raw/GenerateMetadata.py`, so logic follows OoTMM instead of being written by hand.
- The repository root is the world package. `tools/build_apworld.py` picks the files that go into `ootxmm.apworld`; everything else (tools, these docs, the generator and its intermediates) stays out.

## Repository layout
| Path | Contents |
|---|---|
| `world.py` | The `World` class: game name, origin region (`OOT SPAWN`), the generation steps |
| `items.py` | Items built at import from `raw/GreatItemJSONdump.json` and `raw/ItemIDs.json` (below) |
| `logic.py` | The world graph per age with OoTMM's conditions, built per player's settings from `raw/GreatLogicJSONdump.json` ([Logic](#logic)) |
| `regions.py`, `locations.py` | Create the regions, checks and events `logic.py` keeps |
| `rules.py` | Turns conditions into access rules; the completion condition |
| `options.py` | Options, generated from OoTMM's settings by `raw/GenerateMetadata.py` ([Options](#options)). Don't edit it by hand |
| `ootxmm_staticdata.py` | Loads the metadata JSON the world reads at runtime |
| `web_world.py`, `docs/` | Archipelago website pages: game page (`en_OOTxMM.md`) and setup guide (`setup_en.md`) |
| `raw/` | `GenerateMetadata.py` and its outputs. Only the `GreatWorld`, `GreatLogic`, `GreatCheckItem`, `GreatCheckInfo`, `GreatSettings` and `GreatItem` JSON dumps, `LocationIDs.json` and `ItemIDs.json` ship in the apworld (`tools/build_apworld.py`); the YAML, `Isolated*` and `SettingsClasses.json` files are intermediates kept for reading and diffing. The generator also writes `test/check_samples.json` ([Options](#options)) |
| `test/` | The world's own tests, run with Archipelago's ([Build and test](#build-and-test)) |
| `assets/` | Logo |
| `tools/` | Our scripts: pack the world, prune other games from the test checkout, test it, build OoTMM, import upstream |
| `roms/` | The developer's own ROMs (`oot.z64`, `mm.z64`), ignored by git |

## Metadata
`raw/GenerateMetadata.py` is the single place OoTMM data is converted. To regenerate:
1. Put an OoTMM checkout of the release we track ([ROADMAP.md](ROADMAP.md#decisions)) in `raw/ootmm` (ignored by git): `git clone --depth 1 --branch v33.0 https://github.com/OoTMM/OoTMM.git raw/ootmm`. Name the release in the commit message.
2. From `raw/` (the script uses relative paths), run `python GenerateMetadata.py`. It needs PyYAML, and Node with pnpm and `npx tsx`: the logic, item and settings steps import OoTMM's TypeScript directly. The logic step installs OoTMM's dependencies and builds its data package in the checkout itself.
3. It merges `data/world` and `data/macros` into the `Great*` dumps, exports the settings and sorts them ([Options](#options)), exports the logic, updates the location ID registry (below), exports each check's vanilla item, exports the items and updates their registry, splits out the `Isolated*` files, converts the offered settings into `GeneratedOptions.py` and copies that over `../options.py`. Any error stops it.

What the world data looks like, and why:
- **Default variant only.** `WorldSources` lists the files OoTMM's `packages/data/build/world.ts` loads for default settings: no `dungeons_mq` (Master Quest) and no `mm/jp` (the `jpLayouts` Deku Palace). Those files reuse the vanilla region names, so they can't share one dump.
- **Game prefix.** OoT and MM reuse names (shops, `GLOBAL`, `VOID`), so every region and location is named `OOT <name>` or `MM <name>`, like OoTMM's internal IDs. An exit that already starts with a prefix points into the other game. The spawn is `OOT SPAWN`.
- **Reachable regions only.** Regions no exit chain reaches from `OOT SPAWN` are dropped and printed: stubs for the other Deku Palace layout, entrance-randomizer-only sources, and data OoTMM never connects (in v33.0, `Pirate Fortress Telescope` has `exit:` instead of `exits:`).
- **Macros** stay split as `common`, `OOT` and `MM`, since the same macro name differs per game. They are kept for reading: the world uses the logic dump, where OoTMM has already inlined them.

## Logic
OoTMM's own code turns its conditions into rules, so nothing is parsed or rewritten by hand. The generator runs OoTMM's pipeline with default settings up to the entrance pass (which links the games: the Mask Shop door leads to Clock Town) and writes every exit, check and event condition into `raw/GreatLogicJSONdump.json` as a node table. Macros, the vanilla shop prices and the song events are already decided there, and so are the settings the world doesn't offer. The world transform pass is skipped, because it drops the checks default settings leave out and this world keeps them.

The offered settings conditions read (the `logic` and `ported` classes in [Options](#options)) and every trick stay symbolic: OoTMM's parser decides `setting(...)` and `trick(...)` on the spot, so the export wraps its `parseExprSetting` and `parseExprTrick` to return marker events instead, and parses `!` and `cond(...)` itself, since OoTMM only allows them on settings it has decided. The dump has `setting`, `trick` and `not` nodes for them, which `logic.py` decides from the player's settings.

`logic.py` builds the graph from it for each player's settings (`logic.build`, shared by players whose logic settings and tricks match):
- **Ages.** OoTMM explores every area as child and as adult, so each region has a `(Child)` and an `(Adult)` copy, and conditions are specialized to the copy's age. Both ages start at `OOT SPAWN`, the origin, as in OoTMM's pathfinder; the adult spawn needs the `OOT_TIME_TRAVEL` event. Age change at will (`ageChange`) is off by default and not modeled.
- **Events** become event items placed on locations named after them (`MM_MAJORA`). The completion condition follows `goal` (below).
- **Impossible conditions are false**, as they are for OoTMM: an item the pool never holds (MM Ruto's Letter) or an event no area triggers (the pre-completed dungeon events). The pool is the vanilla items of the checks that exist, and which checks exist depends on the pool, so `logic.py` starts from every item and drops those whose check is unreachable until it settles.
- **Left out:** region copies no exit reaches with every pool item, and checks and events false at every copy. In v33.0 with default settings that is 34 checks (MM underwater rocks without MM iron boots, child silver boulders, the guarded Hyrule Castle tree), all unreachable in OoTMM too with default settings.
- **Several parents.** OoTMM lists some checks and events under several regions, meaning reachable from any of them, and every age copy is a parent. Archipelago gives a location one region, so `locations.py` gives a check with more than one parent its own `<check> (check)` region (`<event> (event)` for events), with an entrance from every parent that carries that parent's condition.
- **Approximations.** OoTMM tracks the time of day per area (OoT day and night, MM's three-day clock) and some per-area flags; Archipelago's state can't, so time and flag conditions count as met. `renewable(x)` and `license(x)` count as having `x`.
- **Progression** items are the ones some condition of the player's graph asks for (`Logic.items`). An item link group's world has no graph of its own: its progression items are its members'.

## Options
OoTMM has over 500 settings, and most change more than conditions: the pool, which checks exist, the shape of the world. The world offers only the ones it handles, and `ClassifySettings` in `raw/GenerateMetadata.py` decides which by scanning OoTMM's source, so a new OoTMM release is classified again without a hand-kept list. Its result is `raw/SettingsClasses.json`:
- **ported**: OoTMM's code reads it outside conditions, and the world does what that code does. Listed by hand in `Ported` in `raw/Meta_Options.py`. Offered, and symbolic in the logic dump.
- **port**: OoTMM's code reads it outside conditions (`packages/logic/src`, `packages/data/build`, `packages/core/src`, except the files that only define, parse or roll settings). Not offered until the world ports what it does there ([ROADMAP.md](ROADMAP.md)).
- **logic**: only conditions read it (`setting(...)` in `data/`). Offered, and symbolic in the logic dump ([Logic](#logic)).
- **patch**: neither reads it, so only the ROM patcher does. Offered and passed through.
- **not_offered**: listed in `raw/Meta_Options.py`: meaningless in a multiworld (players, hints, spoiler), read through computed keys the scan can't see (`items.mmAgeRequirements`), or a `custom` value that needs `specialConds`, which is not ported (`lacs`, `rainbowBridge`, `majoraChild`).

The tricks are one option set, `tricks`, defaulting to OoTMM's default tricks. Options are named by their OoTMM key (`doorOfTime: open` in a player YAML), grouped by OoTMM's categories. Archipelago lowercases Choice names and reserves `random` (it rolls it itself, so OoTMM's own `random` value is skipped and a `random` default becomes `default = "random"`); each Choice keeps OoTMM's values in `ootmm_values`. `ootmm_settings` in `world.py` turns a player's options back into OoTMM settings, which `logic.build` reads and `fill_slot_data` hands on as `settings`, for the patch.

Settings the world doesn't offer keep OoTMM's default (`defaults` in `raw/GreatSettingsJSONdump.json`).

**Ported so far: the check filters and the goal.** OoTMM leaves out the checks a setting doesn't shuffle (pots, grass, rocks, free rupees and the like, `filterChecks*` and the removals before `makePools` in `run()` of its `world/transform.ts`); the world's checks are its world files' checks minus `removed_checks` in `logic.py`. That reads each check's type, scene and whether the scene is a dungeon from `raw/GreatCheckInfoJSONdump.json`, which the generator exports from OoTMM's check data along with the name lists `transform.ts` removes by. A removed check's vanilla item leaves the pool with it, as in OoTMM. `pondFishShuffle` is not ported: it also puts fish of random weights in the pool.

`goal` sets the completion condition in `rules.py` as OoTMM's `isGoalReached` does, from its `OOT_GANON` and `MM_MAJORA` events. An enum can be offered with only some of its values (`OfferedValues` in `raw/Meta_Options.py`): `goal` leaves out the Triforce values, which add pieces to the pool.

To port a setting: do in the world what OoTMM's code does with it, add it to `PortedChecks` or `PortedGoal` in `raw/Meta_Options.py` (or a new list for a new kind), and rerun the generator. `test/test_checks.py` checks that every ported setting is one `removed_checks` or the completion condition follows (`PORTED_SETTINGS` in `options.py`) and that `removed_checks` leaves exactly OoTMM's own checks for the settings in `test/check_samples.json`. The generator writes that file by running OoTMM's pipeline with defaults, then every ported check setting at `all` (or on), `overworld` and `dungeons` (or off), as hashes of the check names; on a mismatch, compare `removed_checks` with OoTMM's `state.worlds[0].locations` for that sample. `test/test_options.py` generates with non-default settings and all tricks, and `test/test_checks.py` also generates with every ported setting on.

## Items
`raw/GenerateMetadata.py` exports OoTMM's item list (`packages/logic/src/items/defs.ts`) with each item's display name (`packages/generator/lib/combo/names.ts`) and whether it is in the `TRAPS` or `JUNK` group (`groups.ts`) into `raw/GreatItemJSONdump.json`. `items.py` makes traps `trap`, items the logic asks for `progression`, junk `filler` (including `Nothing`, OoTMM's empty check) and everything else `useful`.

- **Names.** Archipelago needs unique item names, and OoTMM reuses some (`Blue Fire` is an OoT, an MM and a shared item). A reused name gets ` (OoT)` or ` (MM)` on the game's own items, so the shared item keeps the plain name; one still reused gets its OoTMM ID added (`5 Deku Nuts (OoT) (OOT_NUTS_5_ALT)`). The generator fails if any name is still reused.
- **Pool.** OoTMM's base pool: the vanilla item of every check, plus the items whose vanilla source is not a check (`EXTRA_ITEMS` in `logic.py`, from OoTMM's `world/transform.ts`), which replace random filler so the pool matches the location count. The generator exports each check's vanilla item from OoTMM's `data/checks` XML into `raw/GreatCheckItemJSONdump.json`, swapping the placeholders OoTMM swaps itself (`OOT_RANDOM` and the like become green rupees, `CheckItemAliases`), and fails if a location has none. Option-dependent pool changes other than the checks a setting leaves out are not ported yet ([ROADMAP.md](ROADMAP.md)).
- **IDs** live in `raw/ItemIDs.json`, a registry keyed by OoTMM's item ID that follows the same rules as the location registry below: OoT `1001-1999`, MM `2001-2999`, shared `3001-3999`. Item and location IDs are part of the multiworld protocol: once a release is out, never renumber them. `items.py` fails at import if an item has no ID.

## Locations
Location IDs live in `raw/LocationIDs.json`, a registry `raw/GenerateMetadata.py` only adds to. IDs are keyed by name: a check keeps its ID across OoTMM releases (one OoTMM renames counts as new); a new check gets the next free ID in its game's range (OoT `100001-199999`, MM `200001-299999`) and is printed; a check OoTMM removes keeps its entry, so its ID is never reused. Don't edit or reorder the file by hand. `locations.py` fails at import if a location has no ID, which means the generator was not rerun.

## ROMs
OoTMM accepts only Ocarina of Time 1.0 NTSC-U and Majora's Mask NTSC-U, checked by CRC32 in `packages/generator/lib/combo/config.ts` of OoTMM:

| Game | CRC32 | SHA-256 |
|---|---|---|
| OoT 1.0 NTSC-U | `cd16c529` | `c916ab315fbe82a22169bff13d6b866e9fddc907461eb6b0a227b82acdf5b506` |
| MM NTSC-U | `b428d8a7` | `efb1365b3ae362604514c0f9a1a2d11f5dc8688ba5be660a37debf5e3be43f2b` |

OoTMM also lists a second OoT CRC (`d423e8b0`, SHA-256 `d38fd6ff…`). Keep ROMs in `roms/`; nothing copyrighted is committed.

## Build and test
- `python tools/build_apworld.py dist/ootxmm.apworld` packs the world. A new file the world needs must be added to `WORLD_FILES` there (or live under a listed folder such as `test/`).
- `pwsh tools/apworld-test.ps1` runs Archipelago's generic world tests (`test/general`, `test/benchmark`) and the world's own `test/` inside an Archipelago 0.6.8 source checkout. `tools/prune_worlds.py` first removes every other game from that checkout (keeping `generic` and `apquest`, which the tests need), so another game's random failure can't fail our checks. To restore them: `git -C <checkout> checkout HEAD -- worlds`. The first run clones Archipelago and builds a Python 3.12 virtualenv under `%LOCALAPPDATA%\ootmm-decrypted\archipelago`; extra arguments go to pytest.
- `.github/workflows/apworld.yml` (World) runs the same on pushes to `dev` and on pull requests, and uploads the packed `ootxmm.apworld`. `gh workflow run apworld.yml --ref <branch>` runs it on any branch.

## OoTMM build
The ROM patch and the in-game multiworld code come from OoTMM itself, built from source with our changes. `pwsh tools/ootmm-build.ps1` builds it inside WSL (distribution `Ubuntu-24.04`, as root):
- `tools/ootmm-build.sh` keeps a checkout of the tracked release ([ROADMAP.md](ROADMAP.md#decisions)) in `/root/ootmm`, resets it to the tag on every run and applies `ootmm-patches/*.patch` (our changes, as `git diff` output against the tag), so the patches are the only changes. It copies the ROMs from `roms/`, which OoTMM's build reads.
- The build runs in OoTMM's own toolchain image (`ghcr.io/ootmm/toolchain:1.4`, the one its CI uses) under Podman. Ubuntu's own MIPS compiler is too old for OoTMM's C code. The checkout is mounted at the same path inside the container, so CMake caches stay valid.
- Extra arguments run a command in the checkout inside the image instead of the build. A test seed: `pwsh tools/ootmm-build.ps1 "cd packages/generator && NODE_ENV=production pnpm start --seed test"` writes the ROM, the `.ootmm` patch and the spoiler to `/root/ootmm/packages/generator/out` (`\wsl$\Ubuntu-24.04\root\ootmm\...` from Windows).
- WSL itself is set up once with `wsl --install -d Ubuntu-24.04` (needs admin and a reboot); the script installs Podman and pulls the image on first use.

## Branches
- `main`: stable. Only moves to a commit `dev` already tested.
- `dev`: integration branch. Feature branches merge here first.
- `feature/<name>`: one feature or fix per branch. Delete it once merged; only `main` and `dev` stay.

## Syncing upstream
Upstream is `quasky` (Quasky/AP-OOTMM). Its branches are fetched into `refs/quasky/`, outside `refs/remotes/`, so Git clients don't list them as branches. Never merge it directly: import it with the sync script, which strips AI co-author trailers from commit messages deterministically, so repeated imports give the same hashes and later merges stay clean.

```
git remote add quasky https://github.com/Quasky/AP-OOTMM.git        # once
git config remote.quasky.fetch "+refs/heads/*:refs/quasky/*"        # once
pwsh tools/sync-upstream.ps1                                        # -> clean/quasky-main
git merge clean/quasky-main
```

The script needs `python -m pip install git-filter-repo`.

## Conventions
- Commit messages are plain and descriptive. No co-author trailers for tools, and no mention of AI assistants anywhere in commits, code or docs. Local assistant files (`CLAUDE.md`, `AGENTS.md`, `.claude/`) are listed in `.git/info/exclude` and never committed.
- The game name `OOTxMM` is what seeds and clients match on. Changing it is a breaking change.
- Update `ROADMAP.md` in the same commit that starts or finishes an item: add its row when work starts, delete it when the item is done. The roadmap and docs describe the current state, never history. At the end of a change, grep `ROADMAP.md` and the docs for its topic and remove anything it made stale.
- Credit ported work (`cherry-pick -x` or a source note) and keep the README's Credits current.
