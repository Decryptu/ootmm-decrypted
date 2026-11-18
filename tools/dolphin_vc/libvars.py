"""Find libultra exception-handler variables the way the VC emulator does, in a RAM image of a game's boot segment."""
import struct, sys

def op(x): return x >> 26
def imm_u(x): return x & 0xffff
def imm_s(x): v = x & 0xffff; return v - 0x10000 if v & 0x8000 else v

class Img:
    def __init__(s, data, base): s.d = data; s.base = base
    def w(s, a): o = (a & 0x7fffffff) - (s.base & 0x7fffffff); return struct.unpack_from('>I', s.d, o)[0]

def find(img, exc):
    r = {'exc': exc}
    a0, a1 = img.w(exc), img.w(exc + 4)
    assert op(a0) == 0x0f and op(a1) == 0x09
    r[6] = 0x80000000 | ((imm_u(a0) << 16) + imm_s(a1))
    a = exc + 8
    while True:
        o = img.w(a); a += 4
        if o in (0x03404021, 0x03404025): break
    c = [img.w(a), img.w(a + 4), img.w(a + 8)]; last = a
    x = (imm_u(c[0]) << 16) + imm_s(c[1]) if op(c[0]) == 0x0f else (imm_u(c[1]) << 16) + imm_s(c[2])
    x |= 0x80000000
    r[8], r[7], r[5], r[4] = x, x + 4, x - 4, x - 8
    a = last
    while True:
        o = img.w(a); a += 4
        if o in (0x11200013, 0x11200011, 0x1120000D, 0x1120000B, 0x11200009): break
    last = a
    c = [img.w(a + 4), img.w(a + 8)]
    x = 0x80000000 | ((imm_u(c[0]) << 16) + imm_s(c[1]))
    r[3], r[2], r[1], r[0] = x, x - 4, x - 8, x - 16
    a = last
    while True:
        o = img.w(a); a += 4
        if o == 0x40895800: break
    c = [img.w(a), img.w(a + 4)]
    t = ((a & 0xf0000000) | ((c[0] & 0x3ffffff) << 2)) if op(c[0]) == 3 else (((a + 4) & 0xf0000000) | ((c[1] & 0x3ffffff) << 2))
    c = [img.w(t), img.w(t + 4), img.w(t + 8)]
    x = (imm_u(c[0]) << 16) + imm_s(c[1]) if op(c[0]) == 0x0f else (imm_u(c[1]) << 16) + imm_s(c[2])
    r[9] = 0x80000000 | x
    return r

def exc_from_vector(img, vec):
    c = [img.w(vec + 4 * i) for i in range(4)]
    assert op(c[0]) == 0x0f and op(c[1]) == 0x09, [hex(x) for x in c]
    return 0x80000000 | ((imm_u(c[0]) << 16) + imm_s(c[1]))

if __name__ == '__main__':
    rom = open(sys.argv[1], 'rb').read()
    off, base, size = int(sys.argv[2], 16), int(sys.argv[3], 16), int(sys.argv[4], 16)
    img = Img(rom[off:off + size], base)
    # __osExceptionPreamble: lui k0; addiu k0; jr k0; nop  -- search the image for it
    for a in range(base, base + size - 16, 4):
        c = [img.w(a + 4 * i) for i in range(4)]
        if op(c[0]) == 0x0f and (c[0] >> 16 & 31) == 26 and op(c[1]) == 0x09 and c[2] == 0x03400008 and c[3] == 0:
            exc = 0x80000000 | ((imm_u(c[0]) << 16) + imm_s(c[1]))
            print(f'preamble {a:08x} -> exc {exc:08x}')
            try:
                r = find(img, exc); print({k: hex(v) for k, v in r.items()})
            except Exception as e: print('fail', e)
