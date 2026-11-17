# Dolphin and Wii Virtual Console evaluation

This is a developer test procedure. An experimental OoTMM source build reached OoT gameplay and received an item through the RAM mailbox in Dolphin. Use the [player setup guide](setup_en.md) for playtests.

## Majora's Mask donor results

In Dolphin 2609b, the unmodified NTSC-U Majora's Mask channel (NARE) reached the Clock Town intro. gzinject 0.3.1 added the 64 MiB OOTxMM image as `content5/rom` and kept the donor's compressed `content5/romc` byte-for-byte intact. Wii RAM contained the vanilla Majora's Mask header during the injected run. The spinning mask and the earlier tests with a raw 32 or 64 MiB injection therefore provide no evidence that NARE booted a replacement ROM.

| NARE test image | Read-only RAM results |
| --- | --- |
| Combined image as raw `rom`, with the donor's `romc` removed | Neither ROM header found in MEM1 or MEM2. |
| Vanilla MM as type-0 `romc`, 32 MiB | Vanilla ROM header found in MEM1 and MEM2. |
| Same vanilla MM image padded to 64 MiB as type-0 `romc` | Vanilla ROM header found in MEM1 only. |
| Vanilla MM padded to 50 and 52 MiB as type-0 `romc` | Header and end-of-image markers found at the expected offsets in MEM2. |
| Vanilla MM padded to 53 MiB as type-0 `romc` | No header or markers found in either RAM bank at approximately 20 seconds. |
| First 32 MiB of the combined image as type-0 `romc` | Combined ROM header and matching ROM data past 16 MiB found in MEM2. The truncation omits data required by the combined game. |
| Full 64 MiB combined image as type-0 `romc` | Combined ROM header found in MEM1 only. No live mailbox observed on repeated scans. |
| Vanilla MM as type-1 `romc`, 32 MiB decoded | Header and final marker found at the expected offsets in MEM2. |
| Vanilla MM padded to 64 MiB as type-1 `romc` | No header or markers found in either RAM bank after roughly 35 seconds. The encoded file was only 35.6 MiB. |
| Full combined image as type-1 `romc`, 64 MiB decoded | No header, matching samples, or live mailbox found in MEM1 or MEM2. |

For the size controls, place distinct aligned markers near the end of the padded ROM and compare their Wii RAM addresses with the ROM header address. In stock Dolphin the ROM copy started at `0x901df620` and the Wii boot parameters reported the MEM2 arena ending at `0x935e0000`. The 52 MiB copy ends 2,528 bytes below that boundary. A 53 or 64 MiB copy at the same base would extend beyond the arena. This makes the arena a candidate for the load failure. The full 64 MiB type-0 combined image still showed its header only in MEM1 after roughly 35 seconds, with no live mailbox.

Wait at least 20 seconds before judging the copy on this setup. A scan at five seconds showed the 16 MiB marker for images that later reached the 52 MiB marker. Scan again in the same run if the latest marker is still moving.

The [type-1 ROMC tool](https://github.com/Plombo/romextract/blob/master/src/romc.c) decoded each generated file back to the original bytes. The 64 MiB padded vanilla control still failed with an encoded file smaller than a known-good type-0 input. This points to the decoded image size as the limiting factor in these tests.

A disposable Dolphin profile with the RAM override enabled and `MEM2Size = 134217728` in `Dolphin.ini` allocated a 128 MiB mapping. The title still reported 64 MiB of simulated MEM2, with the arena ending at `0x93fc0000`. The same 60 MiB control that showed its header only in MEM1 under stock settings copied through its final marker in MEM2 with the override. The 64 MiB combined image still had no header or matching image samples in MEM2 and no live mailbox after roughly 35 seconds. The standard Python memory engine could read MEM1 but could not read MEM2 with this override. The expanded test used read-only access to Dolphin's host mapping.

### Full ROM copy experiment

Dolphin initially reported 128 MiB of simulated MEM2 and an arena ending at `0x97fc0000`. The NARE NAND loader then used a 64 MiB value to reduce the simulated size, arena end, and IPC bounds. Bypassing that reduction preserved the 128 MiB guest layout. With the donor's existing allocator, the 63 and 64 MiB padded vanilla controls and the full combined image still failed to copy into MEM2.

The NARE allocator uses a 24-bit word count and reserves alignment space. The experiment capped the general MEM2 heap at 54 MiB and put the 64 MiB ROM in a separate buffer at `0x93800000`. A complete readback of that buffer matched the unchanged combined ROM byte for byte. The Direct3D 11 window remained black after the copy and the scan found no mailbox through 86 seconds. The padded vanilla control also matched byte for byte and rendered the spinning mask with the same buffer patch.

These are revision-specific changes to the locally extracted NARE donor. In `content7.app` the NAND loader branch at `0x813310c4` skips the simulated-memory reduction. In the type-0x10 LZ77-compressed DOL in `content1.app`, set the heap limit at `0x80089640` and `0x80089650` to 54 MiB. At `0x800528dc`, store `0x93800000` in the ROM buffer field at `4(r31)`, clear the allocation flag at `-0x70c0(r13)`, and rejoin at `0x80052938`. This procedure requires the 128 MiB Dolphin profile.

Changing bytes `0x3b–0x3e` of a disposable combined image to the vanilla Majora's Mask cartridge ID (`NZSE`) displayed the Nintendo 64 logo before the screen went black and exposed a valid big-endian mailbox at Wii address `0x8136a080`. Its `alive` counter stayed at zero at both 25 and 45 seconds. The Ocarina of Time ID (`CZLE`) exposed no valid mailbox on this donor.

### Startup exception after the logo

After the mailbox initialized, three snapshots of Wii MEM1 from 24 to 40 seconds were identical. The padded vanilla control kept changing. Dolphin's PowerPC log recorded an instruction-storage exception at `0x00000000`. Enabling the MMU or disabling panic dialogs in disposable profiles reproduced the exception.

In the combined run, Wii MEM1 backed N64 RDRAM starting at `0x80f1d0e0`. The captured N64 CPU state pointed to `0x801fec40`, the relocated update routine for OoT's River Sound actor (`0x003b`). The N64 return address `0x8041e504` is immediately after the call through the actor update pointer in `Actor_RunUpdate`. A temporary ROM variant skipped only that actor's update and another skipped the wrapper's dispatch entirely. Both continued changing MEM1 through 40 seconds without that exception. The mailbox counter remained zero in those unattended runs. The actor bypass is a diagnostic and omits the actor's behavior.

The targeted variant rendered the animated OoTMM title screen in Direct3D 11 and remained active through 140 seconds without input. The original actor update faulted at the same N64 address with both Dolphin JIT64 and the cached interpreter. A diagnostic trampoline that jumped directly to the captured update address also reproduced the PowerPC fault.

A later seed-specific test preserved the actor dispatch and rewrote the two tail jumps in its Yaz0-compressed update routine as ordinary calls followed by the shared return sequence. Those jumps were at offsets `0x160` and `0x194` from the callback entry. The modified overlay fit in its original ROM slot. With the soul lookup and heartbeat changes below, NARE passed the startup crash, opened an OoT file, and ran through at least 75 seconds with a moving mailbox counter.

Rebuilding the same seed with sibling-call optimization disabled in `EnRiverSound_Update` still faulted at the relocated callback entry (`0x801fec40`). The compiler emitted ordinary calls with a different branch and return sequence. Disabling delayed-branch scheduling as well, with `__attribute__((optimize("no-optimize-sibling-calls", "no-delayed-branch")))` on that function, reached OoT gameplay with no overlay editing. A separate rebuild using the original compiler settings also reached gameplay after applying the two guarded instruction substitutions at the rebuilt overlay's ROM offset. The affected River Sound scenes still need verification.

### File select and live OoT mailbox

Timed input through an emulated GameCube controller in port 1 (`SIDevice0 = 6` in the disposable Dolphin profile) passed the title screen, created a file and confirmed the file selection. With the River Sound update bypass still applied, opening that file reached a second PowerPC instruction-storage exception at zero. The captured N64 target, `0x8041843c`, was a case selected by the jump table in `comboHasSoulOot`. A seed-specific diagnostic replaced the jump table with a table of bitmap addresses and kept the same bit test. The file then opened inside Link's house. The standard read-only probe found the mailbox signature, but its counter stayed at zero through the run.

Changing the refresh routine's N64 RAM alias from uncached KSEG1 to cached KSEG0 let the counter advance after the file opened. The read-only MEM1 probe reported a live big-endian mailbox at Wii address `0x8136a080`, with `alive` advancing from 312 to 318 in one sample.

With the River Sound overlay change, a local test harness read the game's `HELLO` from the outgoing ring and put the reply in the incoming ring. The game consumed the reply, then sent item index queries and position packets. The harness sent one green rupee through the normal item packet in a fresh profile. The next item index advanced from 0 to 1 and the in-game rupee count rose from 0 to 1. The mailbox read and write routines still used KSEG1. Keep the shared mailbox's cache behavior for other emulators in mind when evaluating a transport fix.

The experimental source patch combines the River Sound compiler settings above with bitmap address tables in the OoT and MM soul lookups. It uses KSEG0 for both the heartbeat and connection flag in `IPC_Ram_Refresh`, with initialization and ring I/O on KSEG1. With only the heartbeat changed, the counter advanced and the game never sent `HELLO`. With both refresh fields changed, the source-built ROM completed the handshake. The harness retried the green rupee while the game still queried index 0. The game then queried index 1 and displayed one rupee. Both the original and source-built ROM tests used the same NARE donor and the `NZSE` cartridge ID.

In a separate fresh-profile run of the source build, the harness loaded Mido's house and placed Link beside the chest. An emulated GameCube A press opened it through the normal game handler. The outgoing packet reported `OOT Mido's House Top Left` (key `0x01280000`) and the seed's Fierce Deity's Mask placement for the other player. The game resent the same check token while the acknowledgment was withheld and stopped resending after receiving the acknowledgment. This test exercised the game's RAM mailbox directly.

### Market door handoff to Majora's Mask

In two disposable NARE profiles with Dolphin JIT64 and the Null video backend, the harness verified the OoT mailbox handshake, loaded the Market through a guarded scene transition, and placed Link in front of the Mask Shop door. An emulated GameCube A press opened the door through the game handler. The door requested entrance `0x0530` and OoTMM set the handoff context to MM South Clock Town (`0xd800`). South Clock Town did not start within 100 seconds of the first attempt or 55 seconds of the repeat.

During the repeat, the OoT mailbox heartbeat stopped and repeated hashes of the full 8 MiB of N64 RDRAM stayed identical. The expected MM bootstrap bytes had not appeared at N64 address `0x80080000`, and the handoff context had not been exported to `0x80098280`. The stall occurred before MM gameplay and is observable without relying on screenshot timing. MM mailbox reattachment, the return trip, save persistence and a live Archipelago connection remain unverified.

A separate source build with stage markers reached the RSP status polling loop in `waitSubsystems()` after the save call and interrupt disable. It never reached the following RDP status poll. The RSP loop requires both HALT and BROKE and waits for both DMA status flags to clear.

A diagnostic variant recorded RSP status `0x241`, which has HALT set, BROKE clear and both DMA flags clear. Requiring HALT and idle DMA let the switch pass the RSP poll, load the MM bootstrap prefix and export the handoff context. Dolphin then logged invalid PowerPC writes in the range `0xa171d0d4–0xa171d0dc` and an instruction-storage exception at zero. Those writes are immediately below the Wii address corresponding to the temporary N64 stack at `0xa0800000`. South Clock Town still did not start.

With the relaxed RSP poll and the temporary stack at the cached N64 alias `0x80800000`, the invalid-write warnings disappeared. The bootstrap prefix and exported context appeared again, but the instruction-storage exception at zero still occurred. The next diagnostic is to capture the N64 execution address around the final jump in `comboGameSwitch4()` and check where bootstrap execution stops. These diagnostic changes are outside the experimental patch.

## Rebuild the experimental ROM

Apply [the experimental source patch](../ootmm-patches/experimental/dolphin-vc.patch) after the regular patches. From a prepared WSL toolchain with dependencies installed, replace the two `/mnt/c/path/` arguments with the player placement file and a scratch output folder.

```powershell
pwsh tools/ootmm-build.ps1 'git apply "$OOTMM_AP_SOURCE_ROOT/ootmm-patches/experimental/dolphin-vc.patch" && pnpm nx run @ootmm/generator:build --prod && cd packages/generator && NODE_ENV=production pnpm exec tsx lib/ap/ap-patch.ts /mnt/c/path/player.ootxmm.json ../../roms/oot.z64 ../../roms/mm.z64 /mnt/c/path/out'
```

Use the NARE `romc` injection and memory changes described above, including `NZSE` on the disposable ROM copy. The source build already includes the actor, soul lookup and mailbox changes. The experimental patch is outside the default build's patch glob.

## Ocarina of Time donor results

The NTSC-U Ocarina of Time channel (NACE) stores a raw 32 MiB `content5/rom`. Repacking it with the full combined ROM in that slot yielded neither the combined header nor a live mailbox in the Wii RAM scans. The stock NACE run exposed ROM data in MEM2, but the scanner did not find the stock header there either, so a missing header is inconclusive for this donor. Gameplay with the repacked WAD remains unverified.

## Try building a test WAD

1. Apply an OOTxMM slot's `.ootmm` patch to your own base ROMs using the usual [patch steps](setup_en.md). Keep the entire resulting `.z64` so the test covers both games.
2. Use your own dump of a Wii Virtual Console donor. Have a local Wii common key file and a build of [gzinject](https://github.com/PracticeROM/gzinject) available. Confirm the unmodified donor WAD boots in Dolphin first.
3. Extract the donor with gzinject. In the extracted `content5` directory, replace the existing ROM entry using the format expected by that donor. For a raw `rom` entry, copy the patched ROM over it. For the NARE test, replace `romc` with an uncompressed type-0 ROMC file. Its four-byte big-endian header is the ROM's byte length shifted left by two bits, followed by the ROM bytes.

   ```powershell
   gzinject -a extract -w "C:\path\to\donor.wad" -k "C:\path\to\common-key.bin" -d wadextract
   # Replace wadextract\content5\rom or romc as described above.
   gzinject -a pack -w ootxmm-test.wad -k "C:\path\to\common-key.bin" -d wadextract
   ```

   For the type-0 ROMC test, use this command before packing:

   ```powershell
   python -c 'import pathlib, struct, sys; rom = pathlib.Path(sys.argv[1]).read_bytes(); pathlib.Path(sys.argv[2]).write_bytes(struct.pack(">I", len(rom) << 2) + rom)' "C:\path\to\slot.z64" wadextract\content5\romc
   ```

4. Use a separate Dolphin user directory for test saves. Open the output WAD through Dolphin's **File → Open**, enter gameplay, and check that saving and reopening the file works. Test switching from OoT to MM and back. If it fails, record the donor revision, Dolphin version and first failing step. Keep the ROMs, key and WAD local and remove scratch output after the test.

## Find the mailbox

For repeatable Windows tests, launch one Dolphin instance with the WAD and a disposable profile:

```powershell
& $dolphin --batch --user $scratchProfile --exec $testWad
```

Add `--video_backend Null` for unattended memory scans without video output. The memory engine could read both Wii RAM banks in this mode on Dolphin 2609b for Windows. Use the regular video backend to verify gameplay. [Dolphin command-line options](https://github.com/dolphin-emu/dolphin/blob/master/Readme.md)

Install [dolphin-memory-engine](https://pypi.org/project/dolphin-memory-engine/) in the Python environment used for the probe. With one Dolphin instance running and the game unpaused in gameplay, run from the repository root:

```powershell
python tools/dolphin_probe.py
```

The probe scans MEM1 and MEM2 for aligned copies of the mailbox signature in native and word-swapped byte order. It checks the header and requires the `alive` counter to change. It only reads memory. If a Wii memory bank is unavailable and you need to inspect the other one, pass `--region MEM1` or `--region MEM2`. Record the reported address and byte layout in each game, then repeat after restarting Dolphin to see whether they change.

On Windows, dolphin-memory-engine 1.3.1 attached to Dolphin 2609b and read both Wii memory banks. A startup scan can distinguish the vanilla and combined ROM headers, but header presence alone cannot establish that the game is running. Verify gameplay and a changing mailbox counter.

Once gameplay and a live mailbox are confirmed, the Dolphin connector needs to reuse the existing protocol. Verify guarded mailbox writes, the handshake, bidirectional checks and items, and reattachment after switching games before adding Dolphin to player setup.
