# Runs the world's tests inside an Archipelago 0.6.8
# source checkout, with the world copied to worlds/ootxmm (tools/build_apworld.py picks the files)
# and every other game removed (tools/prune_worlds.py).
#
#   pwsh tools/apworld-test.ps1                  # default seed and client smoke checks
#   pwsh tools/apworld-test.ps1 -k TestBase      # select tests from the world suite
#   pwsh tools/apworld-test.ps1 -Full            # include upstream tests and benchmarks
#
# The first run clones Archipelago and installs its Python packages into a virtualenv
# (Python 3.12, from the py launcher) under %LOCALAPPDATA%\ootmm-decrypted\archipelago.
# -Reinstall starts that over.
param(
    [switch]$Reinstall,
    [switch]$Full,
    [Parameter(ValueFromRemainingArguments = $true)][string[]]$PytestArgs
)
$ErrorActionPreference = "Stop"
$env:PIP_DISABLE_PIP_VERSION_CHECK = "1"   # also covers the pip runs ModuleUpdate starts
$apRef = "54803be064fc7e80c4628777ed0b46a9390f255f"   # Archipelago 0.6.8, as in apworld.yml
$repo = (git rev-parse --show-toplevel).Trim()
$ap = Join-Path $env:LOCALAPPDATA "ootmm-decrypted\archipelago"
$python = Join-Path $ap ".venv\Scripts\python.exe"
$marker = Join-Path $ap ".ootmmd-ready"

function Run([string]$exe, [string[]]$argv) {
    & $exe @argv
    if ($LASTEXITCODE) { throw "$exe $($argv -join ' ') failed ($LASTEXITCODE)" }
}

if ($Reinstall -and (Test-Path $ap)) { Remove-Item -Recurse -Force $ap }
if (-not (Test-Path $marker) -or (Get-Content $marker) -ne $apRef) {
    if (Test-Path $ap) { Remove-Item -Recurse -Force $ap }
    New-Item -ItemType Directory -Force $ap | Out-Null
    Run git @("-C", $ap, "init", "-q")
    Run git @("-C", $ap, "fetch", "-q", "--depth", "1", "https://github.com/ArchipelagoMW/Archipelago.git", $apRef)
    Run git @("-C", $ap, "-c", "advice.detachedHead=false", "checkout", "-q", "FETCH_HEAD")
    Run py @("-3.12", "-m", "venv", (Join-Path $ap ".venv"))
    Push-Location $ap
    try {
        Run $python @("-m", "pip", "install", "--upgrade", "pip")
        Run $python @("-m", "pip", "install", "-r", "ci-requirements.txt")
        Run $python @("ModuleUpdate.py", "--yes", "--force", "--append", "WebHostLib/requirements.txt")
        $env:SKIP_REQUIREMENTS_UPDATE = "1"
        Run $python @("Launcher.py", "--update_settings")
    } finally { Pop-Location }
    Set-Content -LiteralPath $marker -Value $apRef -NoNewline
}

$world = Join-Path $ap "worlds\ootxmm"
if (Test-Path $world) { Remove-Item -Recurse -Force $world }
Run $python @((Join-Path $repo "tools\build_apworld.py"), "--dir", $world)
Run $python @((Join-Path $repo "tools\prune_worlds.py"), $ap)

Push-Location $ap
try {
    $env:SKIP_REQUIREMENTS_UPDATE = "1"
    if ($Full) {
        & $python -m pytest test/general test/benchmark worlds/ootxmm -n auto -q @PytestArgs
    } elseif ($PytestArgs) {
        & $python -m pytest worlds/ootxmm -q @PytestArgs
    } else {
        & $python -m pytest worlds/ootxmm/test/test_options.py::TestDefaults worlds/ootxmm/test/test_client.py -q
    }
    exit $LASTEXITCODE
} finally { Pop-Location }
