"""Make a test WAD dir: copy extracted NARE, apply the 128 MiB donor patches, inject a ROM as type-0 romc with NZSE."""
import shutil, struct, sys, subprocess, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from dol import lz10_dec, lz10_enc, off

src, rom, outdir = map(pathlib.Path, sys.argv[1:4])
if outdir.exists(): shutil.rmtree(outdir)
shutil.copytree(src, outdir)

def put(dol, addr, words):
    o = off(dol, addr)
    for i, w in enumerate(words): dol[o+4*i:o+4*i+4] = struct.pack('>I', w)

c7 = bytearray((outdir / 'content7.app').read_bytes())
assert c7[off(c7, 0x813310c4):][:4] == bytes.fromhex('40800058')
put(c7, 0x813310c4, [0x48000058])
(outdir / 'content7.app').write_bytes(c7)

c1 = bytearray(lz10_dec((outdir / 'content1.app').read_bytes()))
assert c1[off(c1, 0x80089640):][:4] == bytes.fromhex('3c000400')
assert c1[off(c1, 0x800528dc):][:4] == bytes.fromhex('40800028')
put(c1, 0x80089640, [0x3c000360])
put(c1, 0x80089650, [0x3f990360])
put(c1, 0x800528dc, [0x3c009380, 0x901f0004, 0x38000000, 0x900d8f40, 0x4800004c])
(outdir / 'content1.app').write_bytes(lz10_enc(bytes(c1)))

r = bytearray(rom.read_bytes())
r[0x3b:0x3f] = b'NZSE'
(outdir / 'content5' / 'romc').write_bytes(struct.pack('>I', len(r) << 2) + r)
