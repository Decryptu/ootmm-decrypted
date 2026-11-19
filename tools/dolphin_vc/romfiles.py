import struct

def yaz0(d):
    assert d[:4] == b'Yaz0'
    size = struct.unpack_from('>I', d, 4)[0]; out = bytearray(); i = 16
    while len(out) < size:
        f = d[i]; i += 1
        for b in range(8):
            if len(out) >= size: break
            if f & (0x80 >> b):
                out.append(d[i]); i += 1
            else:
                x = d[i] << 8 | d[i + 1]; i += 2
                dist = (x & 0xfff) + 1; n = x >> 12
                if n == 0: n = d[i] + 0x12; i += 1
                else: n += 2
                for _ in range(n): out.append(out[-dist])
    return bytes(out)

def files(rom, dmadata):
    o = dmadata; out = []
    while True:
        vs, ve, ps, pe = struct.unpack_from('>4I', rom, o); o += 16
        if vs == 0 and ve == 0 and o > dmadata + 16: break
        if ps == 0xffffffff: continue
        data = rom[ps:ps + (ve - vs)] if pe == 0 else yaz0(rom[ps:pe])
        out.append((vs, data))
    return out
