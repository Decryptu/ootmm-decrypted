# OOTxMM setup

This world is in development. A full multiworld play session has not been validated. Logic tracks per-area clock ranges and conditional waiting; clock-sensitive routes still need gameplay verification.

The [interactive setup guide](https://decryptu.github.io/ootmm-decrypted/setup.html) shows a checklist for joining, organizing a group or playing solo, with progress saved in your browser. The full instructions are below.

## How a game is made

Each step depends on the one before it. Doing them out of order is the most common source of problems.

1. Each player sends a YAML to the host.
2. The host runs **Generate** in Archipelago. This makes the seed, but no ROM.
3. The host builds one `.ootmm` patch per player from that seed ([Host preparation](#host-preparation)).
4. Each player applies their patch on the OoTMM website in **Patch** mode and gets a `.z64` ROM.
5. The host starts the server with the same seed.
6. Each player opens their ROM in BizHawk, starts the Lua connector and the BizHawk Client, then connects.

> **Do not generate a seed on ootmm.com.** A ROM from the website's normal generator is an ordinary OoTMM randomizer. It cannot talk to Archipelago and has a different item layout. The BizHawk Client still says it is running the OOTxMM handler for such a ROM, but no item is ever sent or received. Only use the website's **Patch** mode with a `.ootmm` file built from your Archipelago seed.

**Playing solo?** You are both host and player: follow every step yourself, including [Host preparation](#host-preparation).

## What each player needs

- Archipelago 0.6.8, the version this world is tested against.
- The group's matching `ootxmm.apworld`, installed in Archipelago's `custom_worlds` folder. Restart the launcher afterward.
- BizHawk 2.11.1.
- Your own Ocarina of Time 1.0 NTSC-U and Majora's Mask NTSC-U ROMs.
- Your slot's `.ootmm` patch from the host, plus the server address, port, slot name and password if set.

Download the matching world package from the [player hub](https://decryptu.github.io/ootmm-decrypted/). No GitHub account is needed.

## Choose settings

The player hub downloads a starter YAML with your name and goal; all other options keep their defaults. Send one YAML per player to the host, using a unique name. The `name` is your slot name: you type it exactly when connecting, and it is case-sensitive.

For all supported options, select **Generate Template Options** in the Archipelago launcher after installing the world. Edit `Players/Templates/OOTxMM.yaml`, set your name, and send it to the host. Options absent from the template are unsupported.

Already have settings on ootmm.com? Export them from the website, then choose the file in the player hub's YAML form. The hub copies every setting this world supports into your YAML and lists the changed settings it could not import. Archipelago does not read the website's export directly. Generate OOTxMM seeds locally with this custom world installed.

## Build your ROM

1. Open the [OoTMM v33.0 generator](https://ootmm.com/gen/v33.0), matching the host's release.
2. Select your two original ROMs.
3. Under **Generator Mode**, select **Patch**, then your slot's `.ootmm` file. Do not use the normal generator mode.
4. Select **Generate**, then **Download**. Extract the `.z64` if the download is a ZIP.

Cosmetics, such as tunic colors and music, are not part of the patch: the website applies its own cosmetic settings when it builds your ROM. Change them there and patch again whenever you like. Gameplay settings come only from the YAML.

The patch contains the seed's placements and communication code. Players need no WSL or compiler. Keep the patch to rebuild your ROM. The `.ootxmm.json` file is the host's input, not a Patch-mode file. A patch only works with the seed it was built from: if the host generates again, every player needs a new patch.

## Connect and play

1. Open your patched `.z64` in BizHawk.
2. In BizHawk, open **Tools → Lua Console**, then **Script → Open Script**. The connector ships with Archipelago, not BizHawk: select `data/lua/connector_bizhawk_generic.lua` in your Archipelago installation (on Windows, by default `C:\ProgramData\Archipelago\data\lua\connector_bizhawk_generic.lua`).
3. Open the Archipelago launcher and start **BizHawk Client**. Its log shows `Connected to BizHawk`, then `Running handler for OOTxMM`.
4. In the client's **Server** field, enter only the host's address and port, such as `localhost:38281` or `archipelago.gg:12345`, then select **Connect**. Do not add a name or password to the address. When the client asks for the slot name, enter your YAML's `name` exactly, then the password if the host set one.
5. Start a new save file and enter gameplay. The client then finds the game's mailbox; the mailbox is only active in gameplay, not on the title screen or file select. Keep the Lua script, the client and the server running.
6. Open your first check. The client log shows the item found, as in any Archipelago game.

Type `/bh` in the client to see whether it is connected to BizHawk. If the client was started before the Lua script, or BizHawk was restarted, load the script again.

Boss completion is saved on the Archipelago server, so the client can restart between bosses for the `both` goal. The host must keep the server save. Use native in-game saves when resuming; loading an older savestate can rewind received-item progress.

Use Archipelago's BizHawk Client for item exchange. The standalone OoTMM multiplayer client is not used.

Keep the client connected during play. If the server connection drops during a pickup, a following pickup may wait for acknowledgement; reconnect before restarting the emulator. Unrestricted offline play has not been verified.

To resume later, start in the same order: the server with the same seed (it keeps its save), BizHawk with the same ROM and the Lua script, then the client.

### BizHawk settings

The default N64 settings can add input lag and audio delay. In BizHawk:

- **Picture:** under **N64 → Plugins**, select the GLideN64 video plugin and raise its resolution.
- **Audio delay:** under **Config → Sound**, lower the buffer size.
- **Input lag:** under **Config → Display**, try turning off VSync. Keep the Lua Console minimized while playing.
- Keep the Mupen64Plus core, shown in the status bar. The Ares64 core is more accurate but much slower.

## Troubleshooting

| Message or symptom | Cause and fix |
|---|---|
| `connector_bizhawk_generic.lua` is not in BizHawk's `Lua` folder | It ships with Archipelago. Open it from Archipelago's `data/lua` folder ([Connect and play](#connect-and-play), step 2). |
| `Invalid Slot; please verify that you have connected to the correct world` | The server has no slot with that name. Check the name against the YAML (case-sensitive) and check the address and port. If the log lists data packages for games nobody in your group plays, you are connected to someone else's room: get the current address from the host. |
| Connected to the server, but no item is sent or received | The ROM was not built from this seed's `.ootmm` patch, for example a seed generated directly on ootmm.com, or a patch from an older seed. Rebuild the ROM in Patch mode with the current patch. The client log warns when no mailbox exists in the game's memory. |
| The client waits for the mailbox | Enter gameplay: the mailbox is inactive on the title screen and file select. |
| `Waiting to connect to BizHawk` | Load the Lua script again in BizHawk's Lua Console. |
| A room on archipelago.gg stops answering | Rooms sleep when idle and may get a new port when they wake. Open the room's page to wake it, then use the port it shows. |

## Host preparation

Windows hosts can use the host helper below. It needs WSL with Ubuntu 24.04, but no Git, Python or PowerShell 7 on Windows. Players joining your game do not need WSL. macOS/Linux hosts use the Docker commands below.

### Windows host helper

1. Download `ootxmm-host.zip` alongside the matching world package from the group's release, if offered. Extract the entire ZIP to a short local path, such as `C:\ootxmm-host`. Older releases without this ZIP use the manual build instructions below; do not mix their world package with a newer helper. From a repository checkout, the same helper is `Host Setup.cmd` in the root.
2. Double-click **Host Setup.cmd**. It checks WSL before asking for files. If Ubuntu 24.04 is missing, open **Start**, type **PowerShell**, right-click **Windows PowerShell** and select **Run as administrator**. Paste:

   ```powershell
   wsl --install -d Ubuntu-24.04
   ```

   Restart if requested, then open **Ubuntu 24.04** from Start and finish its username/password setup. Run **Host Setup.cmd** again as your normal user. See [Microsoft's WSL installation guide](https://learn.microsoft.com/windows/wsl/install) if Windows reports an installation error.
3. After generating your Archipelago game as described below, select its extracted seed folder in the helper, then your original OoT and MM ROMs. Use files on local Windows drives. The helper converts paths automatically and downloads/builds the toolchain on first use; keep its window open.
4. On success it opens a new `patches-...` folder inside the seed folder. Send each player their `.ootmm` file. Keep the generated `.z64` ROMs and `.build.json` receipts private. If the build fails, the window stays open with the error; rerun the helper after fixing it. Each attempt uses a new output folder, so partial output is never mixed with a later run.

If double-clicking is unavailable, open Windows PowerShell in the extracted helper folder and paste:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -STA -File .\tools\host-setup.ps1
```

This runs the local helper for that process only. The helper uses the dedicated `/root/ootmm` build checkout inside Ubuntu; do not keep your own edits there. It installs Podman and Git inside Ubuntu as needed. Internet access and space for the toolchain and build are required. The helper does not install WSL or restart Windows itself.

### Generate and build

Windows helper users follow steps 1-2, then use the helper instead of steps 3-4. The manual commands remain available for existing toolchain setups.

1. Install the matching world in Archipelago 0.6.8.
2. Put the group's YAMLs in Archipelago's `Players` folder and run **Generate**. The window closes on its own when done. Extract the output ZIP from Archipelago's `output` folder into a dedicated seed folder. It holds the seed's `.archipelago` file, one `.ootxmm.json` file per player and the spoiler.
3. Copy your ROMs to `roms/oot.z64` and `roms/mm.z64` in the repository, then build OoTMM once: `pwsh tools/ootmm-build.ps1` on Windows, or `sh tools/ootmm-build-docker.sh` on macOS or Linux.
4. Build all players with the command below. Unrelated seed files in the input folder are ignored.

On Windows, substitute your paths using their `/mnt/c/...` WSL equivalents:

```powershell
pwsh tools/ootmm-build.ps1 "cd packages/generator && NODE_ENV=production pnpm exec tsx lib/ap/ap-patch.ts /mnt/c/seeds/my-seed ../../roms/oot.z64 ../../roms/mm.z64 /mnt/c/seeds/my-seed/patches"
```

On macOS or Linux, the seed folder is mounted in the container as `/seed`:

```bash
sh tools/ootmm-build-docker.sh --seed ~/seeds/my-seed "cd packages/generator && NODE_ENV=production pnpm exec tsx lib/ap/ap-patch.ts /seed ../../roms/oot.z64 ../../roms/mm.z64 /seed/patches"
```

The input can also be one player JSON. The command stops on the first failure; check it succeeds before distributing patches. It writes a `.ootmm`, `.z64` and private `.build.json` receipt per player. Send each player their patch, the matching world package and connection details. ROMs stay on the machine that built them.

### Start the server

The server passes items between players and saves the group's progress. Both hosting methods use the same locally generated seed and patches: archipelago.gg cannot generate this custom world for you.

#### On archipelago.gg

1. Open [Host Game](https://archipelago.gg/uploads) and upload the generated seed ZIP, not ROMs or the repository.
2. On the seed page, select **Create Room**. Give players the room link, server address and port, slot name and any password.
3. Keep the room link to resume later. Open it to wake an idle room and check its current port. Distribute each player's locally built `.ootmm` patch separately.

See [Archipelago's hosting instructions](https://archipelago.gg/tutorial/Archipelago/setup_en#hosting-on-the-website) for room management.

#### On your computer

Host the seed with the launcher:

1. In the Archipelago launcher, select **Host**, then the seed's output ZIP or the `.archipelago` file extracted from it.
2. Keep the server window open while anyone plays. It shows `Hosting game at <address>:38281`.
3. Players on the same computer connect to `localhost:38281`. Players elsewhere need your public address and port 38281 forwarded; see the [Archipelago setup guide](https://archipelago.gg/tutorial/Archipelago/setup_en) for network setup.

The server saves progress next to the seed file. Start it from the same file to resume.
