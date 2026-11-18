# Dolphin Virtual Console test scripts

Scratch tooling for the Dolphin + Wii VC (NARE) evaluation in [docs/dolphin_evaluation.md](../../docs/dolphin_evaluation.md). The scripts expect a scratch folder `C:\t\vc` holding them, a Python venv at `C:\t\venv` (capstone, dolphin-memory-engine), gzinject built in WSL at `/root/gzinject`, and the NARE donor extracted to `C:\t\vc\nare`. Replace `C:\path\to\ootmm-decrypted` and `/mnt/c/path/to/ootmm-decrypted` with the repository path.

- `mkwad.py`: patches the extracted donor for the 128 MiB layout and injects a ROM as type-0 `romc` with the `NZSE` ID. `pack.sh` packs it.
- `genpatch.py`: generates `vc_libultra.S` (scheduler variable relocation) for both games from the vanilla ROMs.
- `mkfix.py`: applies the fix to the WSL OoTMM checkout; `mkdiag.py` adds diagnostics (stage markers at N64 `0x800003f0`, auto switch from the OoT title demo after 400 frames and back from MM after 300). `gendiag.sh` turns them into `fix.patch` and `diag.patch`.
- `run.ps1 <name> <seconds>`: builds, makes the WAD, runs Dolphin with the `C:\t\vc\prof` profile and follows the markers (`$env:WATCH = 'watch3.py'` for the switch log).
- `ctx.py`: Wii OS exception context and PowerPC stack after an ISI. The NARE `Cpu` struct was at `0x809a3098`, N64 PC at `+0x38`, GPRs (u64) at `+0x58`.
