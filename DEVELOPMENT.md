# Working on OoTMM Decrypted

Everything a new contributor needs, with no other context. Keep it current. [ROADMAP.md](ROADMAP.md) lists what is in progress and planned.

## What this is
- A continuation of [Quasky/AP-OOTMM](https://github.com/Quasky/AP-OOTMM): an Archipelago world (`OOTxMM`) for the [OoTMM](https://github.com/OoTMM/OoTMM) combo randomizer.
- OoTMM's own data (world graph, macros, settings) is converted into the world's metadata by `raw/GenerateMetadata.py`, so logic follows OoTMM instead of being written by hand.
- The repository root is the world package. `tools/build_apworld.py` picks the files that go into `ootxmm.apworld`; everything else (tools, these docs, the generator and its intermediates) stays out.

## Repository layout
| Path | Contents |
|---|---|
| `world.py` | The `World` class: game name, origin region, the generation steps |
| `items.py` | Static item lists and the item ID scheme (below) |
| `locations.py`, `regions.py` | Locations and regions built at import from `raw/GreatWorldJSONdump.json` |
| `rules.py` | Access rules and the completion condition |
| `options.py` | Options, generated from OoTMM's settings by `raw/GenerateMetadata.py`. Don't edit it by hand |
| `ootxmm_staticdata.py` | Loads the metadata JSON the world reads at runtime |
| `web_world.py`, `docs/` | Archipelago website pages: game page (`en_OOTxMM.md`) and setup guide (`setup_en.md`) |
| `raw/` | `GenerateMetadata.py` and its outputs. Only `GreatWorldJSONdump.json` and `GreatMacroJSONdump.json` ship in the apworld; the YAML and `Isolated*` files are intermediates kept for reading and diffing |
| `assets/` | Logo |
| `tools/` | Our scripts: pack the world, test it, import upstream |
| `roms/` | The developer's own ROMs (`oot.z64`, `mm.z64`), ignored by git |

## Metadata
`raw/GenerateMetadata.py` is the single place OoTMM data is converted. To regenerate:
1. Put an OoTMM checkout in `raw/ootmm` (ignored by git). Note its commit in the commit message.
2. From `raw/` (the script uses relative paths), run `python GenerateMetadata.py`. It needs PyYAML, and Node with `npx tsx` for the settings step, which reads `ootmm/packages/core/src/settings/data.ts`.
3. It merges `data/world` and `data/macros` into the `Great*` dumps, splits out the `Isolated*` files, converts the settings into `GeneratedOptions.py` (skipping the names in `Meta_ForbiddenOptions.py`) and copies that over `../options.py`.

## Items
Items are static lists in `items.py`. Each ID is a one-digit game (`GID`), a one-digit category (`CID`) and a three-digit item number (`IID`): `OOT_FISH` is `11069` (OoT, item, 069), `MM_SOUL_NPC_DAMPE` is `22520` (MM, soul, 520).

| Game | GID |
|---|---|
| OoT | 1 |
| MM | 2 |
| Shared | 3 |

| Category | CID |
|---|---|
| Item | 1 |
| Soul | 2 |

| List | ID range |
|---|---|
| OoT items | 11001-11999 |
| MM items | 21001-21999 |
| Shared items | 31001-31999 |
| OoT enemy souls / NPC souls | 12001-12499 / 12501-12999 |
| MM enemy souls / NPC souls | 22001-22499 / 22501-22999 |
| Shared enemy souls / NPC souls | 32001-32499 / 32501-32999 |

Split ranges keep similar items apart without a new category. Item and location IDs are part of the multiworld protocol: once a release is out, never renumber them.

## ROMs
OoTMM accepts only Ocarina of Time 1.0 NTSC-U and Majora's Mask NTSC-U, checked by CRC32 in `packages/generator/lib/combo/config.ts` of OoTMM:

| Game | CRC32 | SHA-256 |
|---|---|---|
| OoT 1.0 NTSC-U | `cd16c529` | `c916ab315fbe82a22169bff13d6b866e9fddc907461eb6b0a227b82acdf5b506` |
| MM NTSC-U | `b428d8a7` | `efb1365b3ae362604514c0f9a1a2d11f5dc8688ba5be660a37debf5e3be43f2b` |

OoTMM also lists a second OoT CRC (`d423e8b0`, SHA-256 `d38fd6ff…`). Keep ROMs in `roms/`; nothing copyrighted is committed.

## Build and test
- `python tools/build_apworld.py dist/ootxmm.apworld` packs the world. A new file the world needs must be added to `WORLD_FILES` there (or live under a listed folder such as `test/`).
- `pwsh tools/apworld-test.ps1` runs Archipelago's generic world tests (`test/general`, `test/benchmark`) and the world's own `test/` inside an Archipelago 0.6.8 source checkout. The first run clones Archipelago and builds a Python 3.12 virtualenv under `%LOCALAPPDATA%\ootmm-decrypted\archipelago`; extra arguments go to pytest.
- `.github/workflows/apworld.yml` (World) runs the same on pushes to `dev` and on pull requests, and uploads the packed `ootxmm.apworld`. `gh workflow run apworld.yml --ref <branch>` runs it on any branch.

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
