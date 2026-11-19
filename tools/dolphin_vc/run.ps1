param([string]$name, [int]$secs = 90)
$ErrorActionPreference = 'Stop'
$R = '/mnt/c/path/to/ootmm-decrypted'
Set-Location C:\path\to\ootmm-decrypted
Get-Process Dolphin -ErrorAction SilentlyContinue | Stop-Process -Force
Remove-Item C:\t\vc\out\* -Force -ErrorAction SilentlyContinue
wsl -d Ubuntu-24.04 -u root -- sh /mnt/c/t/vc/gendiag.sh | Out-Null
pwsh -NoProfile -File tools/ootmm-build.ps1 "git apply $R/ootmm-patches/experimental/dolphin-vc.patch && git apply /mnt/c/t/vc/diag.patch && pnpm nx run @ootmm/generator:build --prod && cd packages/generator && NODE_ENV=production pnpm exec tsx lib/ap/ap-patch.ts $R/dist/age-change/placements/AP_56218420061762034023_P1_AgeOot.ootxmm.json ../../roms/oot.z64 ../../roms/mm.z64 /mnt/c/t/vc/out" 2>&1 | Select-Object -Last 1
Set-Location C:\t\vc
Remove-Item "C:\t\vc\$name", "C:\t\vc\$name.wad" -Recurse -Force -ErrorAction SilentlyContinue
C:\t\venv\Scripts\python.exe mkwad.py nare (Get-ChildItem C:\t\vc\out\*.z64).FullName $name
wsl -d Ubuntu-24.04 -u root -- sh /mnt/c/t/vc/pack.sh $name "$name.wad" | Out-Null
Remove-Item "C:\t\vc\$name" -Recurse -Force
Remove-Item C:\t\vc\prof\Logs -Recurse -Force -ErrorAction SilentlyContinue
Start-Process "C:\Program Files\Dolphin-x64\Dolphin.exe" -ArgumentList '--batch', '--user', 'C:\t\vc\prof', '--exec', "C:\t\vc\$name.wad" | Out-Null
$w = if ($env:WATCH) { $env:WATCH } else { 'watch.py' }
C:\t\venv\Scripts\python.exe "C:\t\vc\$w" $secs | Select-Object -Last 30
Select-String -Path C:\t\vc\prof\Logs\dolphin.log -Pattern 'exception|Invalid' | Select-Object -Last 5 | ForEach-Object Line
