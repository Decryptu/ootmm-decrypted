# Builds OoTMM with our patches inside WSL (tools/ootmm-build.sh); see "OoTMM build" in DEVELOPMENT.md.
# Extra arguments are run in the checkout, in OoTMM's toolchain image, instead of the build.
$ErrorActionPreference = 'Stop'
$env:WSL_UTF8 = 1
$repo = Split-Path $PSScriptRoot -Parent
$wslRepo = (wsl -d Ubuntu-24.04 -u root -- wslpath -a ($repo -replace '\\', '/')).Trim()
wsl -d Ubuntu-24.04 -u root -- sh "$wslRepo/tools/ootmm-build.sh" $wslRepo @args
exit $LASTEXITCODE
