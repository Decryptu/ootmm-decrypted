#!/bin/sh
# Builds OoTMM with our patches (ootmm-patches/) in OoTMM's own toolchain image, inside WSL.
# Run through tools/ootmm-build.ps1, which passes the repository path; see "OoTMM build" in DEVELOPMENT.md.
# Usage: ootmm-build.sh <repository path> [command run in the checkout instead of the build]
set -eu

REPO="$1"
shift
OOTMM_TAG=v33.0
TOOLCHAIN=ghcr.io/ootmm/toolchain:1.4
SRC=/root/ootmm

if ! command -v podman >/dev/null; then
  DEBIAN_FRONTEND=noninteractive apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq podman git >/dev/null
fi

# A clean checkout of the tracked release with our patches on top. Reset on every run, so the patches
# are the only changes; build outputs and installed packages are ignored by git and survive.
if [ ! -d "$SRC/.git" ]; then
  git clone -q --depth 1 --branch "$OOTMM_TAG" https://github.com/OoTMM/OoTMM.git "$SRC"
fi
cd "$SRC"
git -c advice.detachedHead=false checkout -q --force "$OOTMM_TAG" 2>/dev/null || {
  git fetch -q --depth 1 origin tag "$OOTMM_TAG"
  git -c advice.detachedHead=false checkout -q --force "$OOTMM_TAG"
}
git clean -q -fd -e node_modules -e third_party -e roms -e build -e dist
for patch in "$REPO"/ootmm-patches/*.patch; do
  [ -e "$patch" ] || continue
  git apply "$patch"
done
# Our scripts that run on OoTMM's generator (ootmm-ap/), such as the ROM patch.
mkdir -p packages/generator/lib/ap
cp "$REPO"/ootmm-ap/* packages/generator/lib/ap/

# OoTMM's build reads the ROMs (custom assets).
mkdir -p roms
cp "$REPO/roms/oot.z64" "$REPO/roms/mm.z64" roms/

if [ $# -gt 0 ]; then
  CMD="$*"
else
  CMD="pnpm install --frozen-lockfile && ./scripts/deps.sh && pnpm nx run @ootmm/generator:build --prod"
fi
# Windows drives are mounted too, so a command can read and write files there (/mnt/c/...).
podman run --rm -v "$SRC:$SRC" -v /mnt:/mnt -w "$SRC" -e CI=1 -e NX_DAEMON=false -e OOTMM_AP_SOURCE_ROOT="$REPO" "$TOOLCHAIN" sh -c "$CMD"
