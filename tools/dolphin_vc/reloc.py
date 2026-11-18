"""Find and rewrite %hi/%lo references in MIPS code. map: list of (old_start, old_end, new_start)."""
import struct

MEMOPS = {0x20, 0x21, 0x23, 0x24, 0x25, 0x27, 0x28, 0x29, 0x2b, 0x31, 0x35, 0x37, 0x39, 0x3d, 0x3f, 0x09}

def simm(x): v = x & 0xffff; return v - 0x10000 if v & 0x8000 else v

def scan(code, base, maps, window=64):
    n = len(code) // 4
    w = list(struct.unpack(f'>{n}I', code))
    sites = []
    for i in range(n):
        x = w[i]
        if x >> 26 != 0x0f: continue
        rt = (x >> 16) & 31; hi = x & 0xffff
        uses = []
        for j in range(i + 1, min(n, i + window)):
            y = w[j]; o = y >> 26
            if o in MEMOPS and ((y >> 21) & 31) == rt:
                addr = ((hi << 16) + simm(y)) & 0xffffffff
                uses.append((j, addr))
                if o == 0x09 and ((y >> 16) & 31) == rt: break
                if o in (0x20, 0x21, 0x23, 0x24, 0x25, 0x27) and ((y >> 16) & 31) == rt: break
                continue
            # rt overwritten?
            if o == 0 and ((y >> 11) & 31) == rt and (y & 0x3f) not in (0x08, 0x09, 0x18, 0x19, 0x1a, 0x1b): break
            if o in (0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f) and ((y >> 16) & 31) == rt: break
            if o in (0x20, 0x21, 0x23, 0x24, 0x25, 0x27) and ((y >> 16) & 31) == rt: break
            if o == 0 and (y & 0x3f) == 0x08: break  # jr
            if o == 2 or o == 3: pass
        hits = [(j, a) for j, a in uses if any(s <= a < e for s, e, _ in maps)]
        if hits:
            sites.append((i, hi, uses, hits))
    return w, sites

def remap(a, maps):
    for s, e, n in maps:
        if s <= a < e: return n + (a - s)
    return None

def apply(code, base, maps, verbose=True):
    w, sites = scan(code, base, maps)
    bad = 0
    for i, hi, uses, hits in sites:
        news = [remap(a, maps) for j, a in uses]
        if any(v is None for v in news):
            print(f'  mixed lui at {base + 4*i:08x}: uses', [(hex(base + 4*j), hex(a)) for j, a in uses]); bad += 1; continue
        his = {((v + 0x8000) >> 16) & 0xffff for v in news}
        if len(his) != 1:
            print(f'  split hi at {base + 4*i:08x}'); bad += 1; continue
        nh = his.pop()
        w[i] = (w[i] & 0xffff0000) | nh
        for (j, a), v in zip(uses, news):
            w[j] = (w[j] & 0xffff0000) | ((v - (nh << 16)) & 0xffff)
        if verbose: print(f'  {base + 4*i:08x}: ' + ', '.join(f'{base + 4*j:08x} {a:08x}->{v:08x}' for (j, a), v in zip(uses, news)))
    return struct.pack(f'>{len(w)}I', *w), len(sites), bad
