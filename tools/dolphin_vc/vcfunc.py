"""Check GCC functions against Wii VC's function end rule (oot-vc cpuFindFunction).
Usage: vcfunc.py file.elf|file.o ...  Prints functions whose VC end differs from the symbol end."""
import struct, sys

def sections(d):
    shoff, = struct.unpack_from('>I', d, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from('>HHH', d, 0x2e)
    secs = [struct.unpack_from('>10I', d, shoff + i * shentsize) for i in range(shnum)]
    names = secs[shstrndx]
    nm = lambda o: d[names[4] + o:d.index(b'\0', names[4] + o)].decode()
    return [(nm(s[0]),) + s for s in secs]

def funcs(path):
    d = open(path, 'rb').read()
    secs = sections(d)
    out = []
    for s in secs:
        if s[2] != 2: continue  # SHT_SYMTAB
        strtab = secs[s[7]]
        for i in range(s[6] // 16):
            name, value, size, info, other, shndx = struct.unpack_from('>IIIBBH', d, s[5] + i * 16)
            if info & 0xf != 2 or size == 0 or shndx >= len(secs): continue
            sec = secs[shndx]
            if not sec[3] & 4: continue  # executable
            nm = d[strtab[5] + name:d.index(b'\0', strtab[5] + name)].decode()
            off = value - sec[4] if sec[4] else value
            out.append((nm, value, size, d[sec[5]:sec[5] + sec[6]], off, sec[4] if sec[4] else 0))
    return out

def s16(x): return x - 0x10000 if x & 0x8000 else x

def vc_end(code, base, start):
    def op(a):
        o = a - base
        return struct.unpack_from('>I', code, o)[0] if 0 <= o <= len(code) - 4 else 0
    a1 = a2 = 0; save = False; cur = start
    for _ in range(100000):
        w = op(cur); o = w >> 26; end = False
        def fwd(t):
            nonlocal a1
            a1 = t if a1 == 0 or t > a1 else a1
        if o == 0:
            f = w & 0x3f
            if f == 8 and not save and (a1 == 0 or cur > a1) and (a2 == 0 or cur >= a2): end = True
            if f == 0xd and (a1 == 0 or cur > a1) and (a2 == 0 or cur >= a2): end = True; save = False
        elif o == 2:
            t = ((w & 0x3ffffff) << 2) | (cur & 0xf0000000)
            if t >= cur and t - cur <= 0x1000: a2 = t if a2 == 0 or t > a2 else a2
        elif o in (1, 5, 6, 7, 0x15, 0x16, 0x17) or (o == 0x11 and (w >> 21) & 0x1f == 8):
            if o == 1 and (w >> 16) & 0x1f not in (0, 1, 2, 3, 0x10, 0x11, 0x12, 0x13): pass
            else:
                b = s16(w & 0xffff) * 4
                if b < 0:
                    if cur + b + 4 < start: return ('before', cur)
                else: fwd(cur + b)
        elif o in (4, 0x14):
            b = s16(w & 0xffff) * 4
            if b < 0:
                if cur + b + 4 < start: return ('before', cur)
                t = cur + 8
                if op(t) == 0:
                    while op(t) == 0 and t - base < len(code): t += 4
                    if op(t) >> 26 != 0x23 or (t - base >= len(code)):
                        cur2 = t - 8
                        if (a1 == 0 or cur2 > a1) and (a2 == 0 or cur2 >= a2):
                            return ('end', cur2 + 8)
                        cur = cur2
                    else:
                        cur = t - 4
            else: fwd(cur + b)
        elif o == 0x2b and (w >> 16) & 0x1f == 31: save = True
        elif o == 0x23 and (w >> 16) & 0x1f == 31: save = False
        if end: return ('end', cur + 8)
        cur += 4
        if cur - base > len(code) + 8: return ('eof', cur)
    return ('loop', cur)

bad = 0; total = 0
for path in sys.argv[1:]:
    for nm, value, size, code, off, secaddr in funcs(path):
        base = value - off
        kind, e = vc_end(code, base, value)
        real = value + size
        total += 1
        if kind == 'end':
            # allow trailing zero padding inside the symbol
            if e == real: continue
            if e < real and all(b == 0 for b in code[e - base:real - base]): continue
        bad += 1
        print(f'{path.split("/")[-1]}: {nm} {value:08x}+{size:x} vc {kind} {e:08x} ({e - real:+x})')
print(f'{bad} of {total} functions differ', file=sys.stderr)
