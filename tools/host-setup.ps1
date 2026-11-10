# Windows PowerShell 5.1; no PowerShell 7 installation required.
[CmdletBinding()]
param([string]$SeedFolder, [string]$OotRom, [string]$MmRom, [switch]$CheckOnly)
$ErrorActionPreference = 'Stop'
$env:WSL_UTF8 = '1'
$repo = Split-Path $PSScriptRoot -Parent

function WslPath([string]$Path) {
    $result = & wsl.exe -d Ubuntu-24.04 -u root --exec wslpath -a ($Path -replace '\\', '/')
    if ($LASTEXITCODE -ne 0) { throw "Cannot translate path: $Path" }
    return ($result -join "`n").Trim()
}
function PickFile([string]$Title) {
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Title = $Title
    $dialog.Filter = 'N64 ROM (*.z64;*.n64;*.v64)|*.z64;*.n64;*.v64|All files (*.*)|*.*'
    try {
        if ($dialog.ShowDialog() -ne 'OK') { throw 'Selection cancelled. No patches built.' }
        return $dialog.FileName
    } finally { $dialog.Dispose() }
}
try {
    if (-not (Get-Command wsl.exe -ErrorAction SilentlyContinue)) {
        throw 'WSL is missing. Follow the WSL installation steps in docs/setup_en.md, then run this helper again.'
    }
    & wsl.exe -d Ubuntu-24.04 -u root --exec true
    if ($LASTEXITCODE -ne 0) {
        throw 'Ubuntu-24.04 is not ready. In an administrator PowerShell run: wsl --install -d Ubuntu-24.04. Restart if requested, open Ubuntu 24.04 to finish setup, then run this helper again. See https://learn.microsoft.com/windows/wsl/install'
    }
    foreach ($relative in @('tools/ootmm-build.sh', 'ootmm-ap/ap-patch.ts', 'ootmm-patches')) {
        if (-not (Test-Path -LiteralPath (Join-Path $repo $relative))) { throw "Missing $relative. Extract the entire host ZIP first." }
    }
    if ($CheckOnly) { Write-Host 'WSL and host package are ready.'; exit 0 }
    Add-Type -AssemblyName System.Windows.Forms
    if (-not $SeedFolder) {
        $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
        $dialog.Description = 'Choose the extracted Archipelago seed folder containing .ootxmm.json files'
        try {
            if ($dialog.ShowDialog() -ne 'OK') { throw 'Selection cancelled. No patches built.' }
            $SeedFolder = $dialog.SelectedPath
        } finally { $dialog.Dispose() }
    }
    $SeedFolder = (Resolve-Path -LiteralPath $SeedFolder).Path
    if (-not (Get-ChildItem -LiteralPath $SeedFolder -Filter '*.ootxmm.json' -File)) {
        throw 'No .ootxmm.json files here. Extract the generated Archipelago ZIP and select that folder.'
    }
    if (-not $OotRom) { $OotRom = PickFile 'Choose your Ocarina of Time 1.0 NTSC-U ROM' }
    if (-not $MmRom) { $MmRom = PickFile "Choose your Majora's Mask NTSC-U ROM" }
    $OotRom = (Resolve-Path -LiteralPath $OotRom).Path
    $MmRom = (Resolve-Path -LiteralPath $MmRom).Path
    foreach ($path in @($repo, $SeedFolder, $OotRom, $MmRom)) {
        if ($path -notmatch '^[A-Za-z]:\\') { throw 'Use local Windows drive paths; network shares are not supported.' }
    }
    $output = Join-Path $SeedFolder ('patches-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
    New-Item -ItemType Directory -Path $output | Out-Null
    $linuxRepo = WslPath $repo
    $linuxSeed = WslPath $SeedFolder
    $linuxOot = WslPath $OotRom
    $linuxMm = WslPath $MmRom
    $linuxOutput = WslPath $output
    Write-Host 'Building patches. First use downloads the toolchain and can take several minutes. Keep this window open.'
    & wsl.exe -d Ubuntu-24.04 -u root --exec sh "$linuxRepo/tools/ootmm-build.sh" $linuxRepo --patch-seed $linuxSeed $linuxOot $linuxMm $linuxOutput
    if ($LASTEXITCODE -ne 0) { throw "Build failed. Do not distribute partial output. See the error above. Output: $output" }
    Write-Host "Build complete: $output"
    Write-Host 'Send each player their .ootmm patch. Keep ROMs and .build.json receipts private.'
    Start-Process explorer.exe -ArgumentList ('"' + $output + '"')
} catch {
    Write-Host ("ERROR: " + $_.Exception.Message) -ForegroundColor Red
    exit 1
}
