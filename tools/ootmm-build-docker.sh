#!/bin/sh
# Builds OoTMM with our patches (ootmm-patches/) in OoTMM's own toolchain image with Docker, for macOS and
# Linux hosts. Same steps as tools/ootmm-build.sh (the WSL build); see "OoTMM build" in DEVELOPMENT.md.
# Usage: sh tools/ootmm-build-docker.sh [--seed <seed folder>] [command run in the checkout instead of the build]
# The seed folder, if given, is mounted at /seed. The checkout lives in $OOTMM_SRC
# (default ~/.cache/ootmm-decrypted/ootmm) and keeps its build outputs between runs.
set -eu

REPO=$(cd "$(dirname "$0")/.." && pwd)
OOTMM_TAG=v33.0
TOOLCHAIN=ghcr.io/ootmm/toolchain:1.4
SRC=${OOTMM_SRC:-$HOME/.cache/ootmm-decrypted/ootmm}

SEED=""
if [ "${1:-}" = "--seed" ]; then
  [ $# -ge 2 ] || { echo "--seed needs a folder" >&2; exit 2; }
  [ -d "$2" ] || { echo "Seed folder not found: $2" >&2; exit 2; }
  SEED=$(cd "$2" && pwd)
  shift 2
fi

command -v docker >/dev/null || { echo "Docker is required" >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "The Docker daemon is not running; start Docker first" >&2; exit 1; }
for rom in oot mm; do
  [ -f "$REPO/roms/$rom.z64" ] || { echo "Missing $REPO/roms/$rom.z64" >&2; exit 1; }
done

# A clean checkout of the tracked release with our patches on top. Reset on every run, so the patches
# are the only changes; build outputs and installed packages are ignored by git and survive.
if [ ! -d "$SRC/.git" ]; then
  mkdir -p "$(dirname "$SRC")"
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
mkdir -p packages/generator/lib/ap roms
cp "$REPO"/ootmm-ap/* packages/generator/lib/ap/
cp "$REPO/roms/oot.z64" "$REPO/roms/mm.z64" roms/

if [ $# -gt 0 ]; then
  CMD="$*"
else
  CMD="pnpm install --frozen-lockfile && ./scripts/deps.sh && pnpm nx run @ootmm/generator:build --prod"
fi
# The image is x86-64 only; Apple Silicon runs it through emulation. The checkout is mounted at the same
# path, so CMake caches stay valid, and the repository read-only for the build receipt's input hashes.
set -- --rm --platform linux/amd64 -v "$SRC:$SRC" -v "$REPO:/repo:ro" -w "$SRC" \
  -e CI=1 -e NX_DAEMON=false -e OOTMM_AP_SOURCE_ROOT=/repo
[ -z "$SEED" ] || set -- "$@" -v "$SEED:/seed"
docker run "$@" "$TOOLCHAIN" sh -c "$CMD"
