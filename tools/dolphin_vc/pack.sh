set -e
cd /mnt/c/t/vc
/root/gzinject/gzinject -a pack -w "$2" -k /mnt/c/path/to/ootmm-decrypted/roms/vc/common-key.bin -d "$1" >/dev/null
ls -la "$2"
