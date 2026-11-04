# Player hub assets

The PNG icons and interface textures are extracted from the owner's supported NTSC-U game copies. `game-assets.json` records each source bank, DMA index, texture symbol, offset, format and size. Re-export with `python tools/extract_site_assets.py` (requires Pillow; reads ignored `roms/oot.z64` and `roms/mm.z64`). The website needs only these PNGs, never the ROMs.

| Site asset | Original artwork |
|---|---|
| `menu-guide.png` | OoT Dungeon Map inventory icon |
| `menu-notebook.png` | MM Bombers' Notebook inventory icon |
| `menu-ocarina.png` | OoT Ocarina of Time inventory icon |
| `menu-package.png` | OoT Boss Key inventory icon |
| `menu-mask.png` | MM Mask of Truth inventory icon |
| `menu-tools.png` | OoT Megaton Hammer inventory icon |
| `pause-frame.png` | OoT save-screen panel pieces; the caption tile is replaced with blank game-over stone for HTML titles |
| `pause-stone.png`, `pause-dark.png` | OoT blank game-over panel texture |
| `button-a.png`, `button-b.png`, `button-c.png`, `heart.png` | OoT HUD button background, pause-button symbols, ocarina C-down prompt and heart texture |
| `cursor.png` | OoT's four pause-menu selection-cursor corners |
| `name-panel.png` | OoT's two item-name panel pieces |
| `message-box.png` | OoT's default dialogue-box texture |

Intensity/alpha textures are colored when rendered in the game. The exporter applies fixed HUD and olive/blue panel colors to those original pixels; CSS scales the PNGs with nearest-neighbor sampling. Backgrounds use the original stone material, not a drawn landscape.

Texture names and layouts follow [zeldaret/oot](https://github.com/zeldaret/oot/tree/main/assets/xml/textures), [zeldaret/mm](https://github.com/zeldaret/mm/blob/main/assets/xml/archives/icon_item_static.xml) and the [OoTMM v33.0 metadata](https://github.com/OoTMM/OoTMM/tree/v33.0/packages/generator/data/setup). The game artwork belongs to Nintendo and its respective rights holders and is not covered by the repository's MIT license.

`pixelify-sans.ttf` is Pixelify Sans by the Pixelify Sans Project Authors, distributed under the SIL Open Font License. See `pixelify-sans-OFL.txt` and [the source](https://github.com/google/fonts/tree/main/ofl/pixelifysans).

The combined emblem is copied from the repository's `assets/ootmm-decrypted.png` during staging. Its artwork credits are in the repository's `assets/README.md`.
