set -e
R=/mnt/c/path/to/ootmm-decrypted
cd /root/ootmm
git checkout -q --force .
git clean -q -fd -e node_modules -e third_party -e roms -e build -e dist
for p in "$R"/ootmm-patches/*.patch "$R"/ootmm-patches/experimental/dolphin-vc.patch; do git apply "$p"; done
git add -A packages/generator/src
python3 /mnt/c/t/vc/mkfix.py
git add -N packages/generator/src
git diff -- packages/generator/src > /mnt/c/t/vc/fix.patch
git add -A packages/generator/src
if [ "${1:-}" != "nodiag" ]; then python3 /mnt/c/t/vc/mkdiag.py; fi
git diff -- packages/generator/src packages/generator/CMakeLists.txt > /mnt/c/t/vc/diag.patch
git reset -q
git checkout -q --force .
git clean -q -fd -e node_modules -e third_party -e roms -e build -e dist
