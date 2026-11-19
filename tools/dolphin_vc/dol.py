import struct, sys, capstone

def lz10_dec(d):
    assert d[0] == 0x10
    size = d[1] | d[2] << 8 | d[3] << 16
    out = bytearray(); i = 4
    while len(out) < size:
        flags = d[i]; i += 1
        for b in range(8):
            if len(out) >= size: break
            if flags & (0x80 >> b):
                x = d[i] << 8 | d[i+1]; i += 2
                n = (x >> 12) + 3; disp = (x & 0xfff) + 1
                for _ in range(n): out.append(out[-disp])
            else:
                out.append(d[i]); i += 1
    return bytes(out)

def lz10_enc(d):
    # literal-only encoding, valid and simple
    out = bytearray([0x10, len(d) & 0xff, (len(d) >> 8) & 0xff, (len(d) >> 16) & 0xff])
    for i in range(0, len(d), 8):
        out.append(0); out += d[i:i+8]
    while len(out) % 4: out.append(0)
    return bytes(out)

def sections(dol):
    offs = struct.unpack('>18I', dol[0:72]); addrs = struct.unpack('>18I', dol[72:144]); sizes = struct.unpack('>18I', dol[144:216])
    return [(o, a, s) for o, a, s in zip(offs, addrs, sizes) if s]

def off(dol, addr):
    for o, a, s in sections(dol):
        if a <= addr < a + s: return o + addr - a
    raise KeyError(hex(addr))

def dis(dol, addr, n=16):
    md = capstone.Cs(capstone.CS_ARCH_PPC, capstone.CS_MODE_32 | capstone.CS_MODE_BIG_ENDIAN)
    o = off(dol, addr)
    for ins in md.disasm(dol[o:o+4*n], addr):
        print(f"{ins.address:08x}: {ins.bytes.hex()} {ins.mnemonic} {ins.op_str}")

if __name__ == '__main__':
    path = sys.argv[1]; d = open(path, 'rb').read()
    if d[0] == 0x10: d = lz10_dec(d)
    for i in range(2, len(sys.argv), 2):
        print('--', sys.argv[i]); dis(d, int(sys.argv[i], 16), int(sys.argv[i+1]))
