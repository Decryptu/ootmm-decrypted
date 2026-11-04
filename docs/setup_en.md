# OOTxMM setup

This world is in development. A full multiworld play session has not been validated. Logic tracks per-area clock ranges and conditional waiting; clock-sensitive routes still need gameplay verification.

## What each player needs

- Archipelago 0.6.8, the version this world is tested against.
- The group's matching `ootxmm.apworld`, installed in Archipelago's `custom_worlds` folder. Restart the launcher afterward.
- BizHawk 2.11.1.
- Your own Ocarina of Time 1.0 NTSC-U and Majora's Mask NTSC-U ROMs.
- Your slot's `.ootmm` patch from the host, plus the server address, port, slot name and password if set.

Ask the host for the world package. Development builds are the `ootxmm.apworld` artifact of successful [World workflow runs](https://github.com/Decryptu/ootmm-decrypted/actions/workflows/apworld.yml). Sign in to GitHub and extract the downloaded artifact ZIP. Everyone should use the same build.

## Choose settings

The player hub downloads a starter YAML with your name and goal; all other options keep their defaults. Send one YAML per player to the host, using a unique name.

For all supported options, select **Generate Template Options** in the Archipelago launcher after installing the world. Edit `Players/Templates/OOTxMM.yaml`, set your name, and send it to the host. Options absent from the template are unsupported. Generate OOTxMM seeds locally with this custom world installed.

## Build your ROM

1. Open the [OoTMM v33.0 generator](https://ootmm.com/gen/v33.0), matching the host's release.
2. Select your two original ROMs.
3. Under **Generator Mode**, select **Patch**, then your slot's `.ootmm` file.
4. Select **Generate**, then **Download**. Extract the `.z64` if the download is a ZIP.

The patch contains the seed's placements and communication code. Players need no WSL or compiler. Keep the patch to rebuild your ROM. The `.ootxmm.json` file is the host's input, not a Patch-mode file.

## Connect and play

1. Open your patched `.z64` in BizHawk and enter gameplay.
2. Open **Tools → Lua Console**, then load `data/lua/connector_bizhawk_generic.lua` from your Archipelago installation.
3. Launch **BizHawk Client** from the Archipelago launcher.
4. Connect to the host's server address and port. Enter your YAML's player name when asked for the slot, and the password if required.
5. Wait for the client to report finding the mailbox and connecting to the game. Keep both the Lua script and client running.

Boss completion is saved on the Archipelago server, so the client can restart between bosses for the `both` goal. The host must keep the server save.

Use Archipelago's BizHawk Client for item exchange. The standalone OoTMM multiplayer client is not used. If the mailbox is not found, enter gameplay: its counter does not move on the title screen or file select. If server login fails, check the slot name and that your patch matches the seed and player.

## Host preparation

The host needs this repository, the two ROMs, and the WSL toolchain described in the repository's `DEVELOPMENT.md`.

1. Install the matching world in Archipelago 0.6.8.
2. Put the group's YAMLs in Archipelago's `Players` folder, run **Generate**, and extract the output ZIP into a dedicated seed folder.
3. Build OoTMM once: `pwsh tools/ootmm-build.ps1`.
4. Build all players with the command below. Substitute your paths using their `/mnt/c/...` WSL equivalents. Unrelated seed files in the input folder are ignored.

```powershell
pwsh tools/ootmm-build.ps1 "cd packages/generator && NODE_ENV=production pnpm exec tsx lib/ap/ap-patch.ts /mnt/c/seeds/my-seed ../../roms/oot.z64 ../../roms/mm.z64 /mnt/c/seeds/my-seed/patches"
```

The input can also be one player JSON. The command stops on the first failure; check it succeeds before distributing patches. It writes a `.ootmm` and `.z64` per player. Send each player their patch, the matching world package and connection details. ROMs stay on the machine that built them.

Host the generated `.archipelago` file with Archipelago's server. See the [Archipelago setup guide](https://archipelago.gg/tutorial/Archipelago/setup_en) for hosting and network setup.
