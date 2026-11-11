# Imports an upstream branch into refs/clean/<name>, with prohibited attribution stripped
# from commit messages. The rewrite is deterministic, so running it again later produces the same
# hashes for commits already imported and a normal `git merge clean/<name>` keeps working. The ref
# sits outside refs/remotes/, so Git clients do not list it as a branch.
#
#   pwsh tools/sync-upstream.ps1                  # quasky main (the default)
#   git merge clean/quasky-main
#
# -Path keeps only one folder of the upstream repo and -Prefix moves it; -Name picks the clean/
# ref when one branch is imported twice. Neither is needed for AP-OOTMM, whose layout we keep.
#
# Needs git-filter-repo: python -m pip install git-filter-repo
param(
    [string]$Remote = "quasky",
    [string]$Branch = "main",
    [string]$Path = "",
    [string]$Prefix = "",
    [string]$Name = ""
)
$ErrorActionPreference = "Stop"
$repo = (git rev-parse --show-toplevel).Trim()
$url = (git -C $repo remote get-url $Remote).Trim()
if (-not $Name) { $Name = "$Remote-$Branch" }
$work = Join-Path ([IO.Path]::GetTempPath()) "ootmmd-sync-$($Name -replace '/', '-')"

if (Test-Path $work) { Remove-Item -Recurse -Force $work }
git clone --bare --single-branch --branch $Branch --no-tags $url $work
if ($LASTEXITCODE) { throw "clone failed" }

$env:OOTXMM_PUBLIC_METADATA_CHECK = Join-Path $repo 'tools/check_public_metadata.py'
$callback = @'
import os
import runpy
prohibited = runpy.run_path(os.environ["OOTXMM_PUBLIC_METADATA_CHECK"])["prohibited"]
lines = message.splitlines(keepends=True)
kept = [line for line in lines if not (
    line.lstrip().lower().startswith(b"co-authored-by:")
    and prohibited(line.decode("utf-8", "replace"))
)]
if len(kept) != len(lines):
    message = b"".join(kept).rstrip() + b"\n"
return message
'@
$pathArgs = @()
if ($Path) { $pathArgs += @("--path", $Path) }
if ($Path -and $Prefix) { $pathArgs += @("--path-rename", "${Path}:$Prefix") }
try {
    python -m git_filter_repo --source $work --target $work --force --quiet --message-callback $callback @pathArgs
    if ($LASTEXITCODE) { throw "filter-repo failed" }
    Push-Location $work
    try {
        python $env:OOTXMM_PUBLIC_METADATA_CHECK --history "refs/heads/$Branch"
        if ($LASTEXITCODE) { throw "upstream publication metadata check failed" }
    } finally {
        Pop-Location
    }
} finally {
    Remove-Item Env:OOTXMM_PUBLIC_METADATA_CHECK
}

git -C $repo fetch --no-tags $work "+refs/heads/${Branch}:refs/clean/$Name"
if ($LASTEXITCODE) { throw "fetch failed" }
Remove-Item -Recurse -Force $work
Write-Host "Updated clean/$Name -> $((git -C $repo rev-parse --short "clean/$Name").Trim())"
