# Dolphin and Wii Virtual Console evaluation

This is a developer test procedure. OoTMM gameplay and Archipelago item delivery in Dolphin are unverified. Use the [player setup guide](setup_en.md) for playtests.

In Dolphin 2609b, the unmodified NTSC-U Majora's Mask channel (NARE) reached the Clock Town intro. With the same donor and command, the original Majora's Mask ROM reached the spinning-mask intro at both its original 32 MiB size and after padding it with zeros to 64 MiB. The padded test checks whether the channel can boot with a 64 MiB ROM file. It does not exercise reads beyond the original 32 MiB.

With the full 64 MiB OOTxMM ROM injected by gzinject 0.3.1, the channel also reached the spinning-mask intro. The black frame in the first test was insufficient to determine a boot failure. Extracting the generated WAD confirmed that its content contains the exact combined ROM. Which ROM the channel runs remains unverified. Check for OOTxMM-specific gameplay or a live mailbox before counting this as a successful OOTxMM boot.

## Try building a test WAD

1. Apply an OOTxMM slot's `.ootmm` patch to your own base ROMs using the usual [patch steps](setup_en.md). Keep the entire resulting `.z64` so the test covers both games.
2. Use your own dump of the NTSC-U Majora's Mask Wii Virtual Console channel as the first candidate. Have a local Wii common key file and a build of [gzinject](https://github.com/PracticeROM/gzinject) available. Confirm the unmodified donor WAD boots in Dolphin first.
3. From a disposable directory, try the following command with absolute input paths. The command is an injection attempt. Compatibility depends on whether the donor can load and run the full combined ROM.

   ```powershell
   gzinject -a inject -w "C:\path\to\donor.wad" -m "C:\path\to\slot.z64" -k "C:\path\to\common-key.bin" -d wadextract -o ootxmm-test.wad
   ```

4. Use a separate Dolphin user directory for test saves. Open the output WAD through Dolphin's **File → Open**, enter gameplay, and check that saving and reopening the file works. Test switching from OoT to MM and back. If it fails, record the donor revision, Dolphin version and first failing step. Keep the ROMs, key and WAD local and remove scratch output after the test.

## Find the mailbox

For repeatable Windows tests, launch one Dolphin instance with the WAD and a disposable profile:

```powershell
& $dolphin --batch --user $scratchProfile --exec $testWad
```

Install [dolphin-memory-engine](https://pypi.org/project/dolphin-memory-engine/) in the Python environment used for the probe. With one Dolphin instance running and the game unpaused in gameplay, run from the repository root:

```powershell
python tools/dolphin_probe.py
```

The probe scans MEM1 and MEM2 for aligned copies of the mailbox signature in native and word-swapped byte order. It checks the header and requires the `alive` counter to change. It only reads memory. If a Wii memory bank is unavailable and you need to inspect the other one, pass `--region MEM1` or `--region MEM2`. Record the reported address and byte layout in each game, then repeat after restarting Dolphin to see whether they change.

On Windows, dolphin-memory-engine 1.3.1 attached to Dolphin 2609b and read both Wii memory banks for the original and injected WADs. Scans during startup found no mailbox in either run. Repeat the scan after entering gameplay.

Once gameplay and a live mailbox are confirmed, the Dolphin connector needs to reuse the existing protocol. Verify guarded mailbox writes, the handshake, bidirectional checks and items, and reattachment after switching games before adding Dolphin to player setup.
