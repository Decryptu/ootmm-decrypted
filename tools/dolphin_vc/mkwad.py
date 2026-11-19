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
# S2DEX G_BG_COPY/G_BG_1CYC: for an MM ROM ID the emulator replaces every background with MM's
# framebuffer-copy effect, which draws a mirrored previous frame. OoT pre-rendered rooms (shops,
# houses) use images in room segment 0x03, so send those to the normal background draw.
# 0x80070128 duplicated the call at 0x800700c8; it becomes a branch there and frees room for the checks.
assert c1[off(c1, 0x80070124):][:8] == bytes.fromhex('4082004438e00000')
assert c1[off(c1, 0x80070248):][:4] == bytes.fromhex('4182001c')
put(c1, 0x80070124, [0x40820034, 0x4bffffa0,
    0x7cba2b78, 0x7f23cb78, 0x7f44d378, 0x38a10058, 0x4bffa12d,   # fill bg; imagePtr at 0x68(r1)
    0x88010068, 0x28000003, 0x4082011c, 0x7f23cb78, 0x7f45d378, 0x480000f8,   # BG_COPY
    0x88010068, 0x28000003, 0x4182ff68, 0x48000004])   # BG_1CYC
put(c1, 0x80070248, [0x4182fee4])
# Save store: the emulator writes the flash image to NAND at most once every 6 minutes and
# otherwise only on a clean exit. Stopping Dolphin loses newer saves, so flush whenever dirty.
assert c1[off(c1, 0x8007e580):][:4] == bytes.fromhex('41820034')
put(c1, 0x8007e580, [0x48000034])
(outdir / 'content1.app').write_bytes(lz10_enc(bytes(c1)))

r = bytearray(rom.read_bytes())
r[0x3b:0x3f] = b'NZSE'
(outdir / 'content5' / 'romc').write_bytes(struct.pack('>I', len(r) << 2) + r)
