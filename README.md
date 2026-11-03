<p align="center">
<img src="assets/ap-ootmm.png" alt="logo" width="25%"/>
</p>

# OoTMM Decrypted

An [Archipelago](https://archipelago.gg) world for the [OoTMM](https://github.com/OoTMM/OoTMM) combo randomizer (The Legend of Zelda: Ocarina of Time and Majora's Mask in one ROM).

It continues Quasky's [AP-OOTMM](https://github.com/Quasky/AP-OOTMM), with its full history. In Archipelago the game is called `OOTxMM`.

## Status

Not playable yet. Archipelago can generate with it: OoTMM v33.0's regions, locations and items are in, the pool is OoTMM's base pool placed as OoTMM's defaults place it, the logic is OoTMM's, and the settings that only change conditions or the ROM, or which checks exist (pots, grass and the like), are offered as options (time of day is not tracked yet). A player's ROM can be built from the seed, but only with the OoTMM toolchain, and the BizHawk client connects to the game in BizHawk but has not been through a real play session yet. [ROADMAP.md](ROADMAP.md) lists what is left.

## What you need

- Archipelago 0.6.8 or newer.
- Your own ROMs: Ocarina of Time 1.0 NTSC-U and Majora's Mask NTSC-U (`.z64`, the versions OoTMM accepts). They are never part of this repository.

## Working on it

[DEVELOPMENT.md](DEVELOPMENT.md) has the layout, tools, ID registries and conventions.

## Credits

- Quasky, for AP-OOTMM, which this repository is built on.
- [Fletch64](https://github.com/Fletch64) and [alphaONE2](https://github.com/alphaONE2), for the first pass at an OoTMM Archipelago world and generator.
- The [OoTMM team](https://github.com/OoTMM/OoTMM), for OoTMM, whose world and settings data this world is generated from.
- The Archipelago contributors.

MIT License, see [LICENSE](LICENSE).
