import struct, dolphin_memory_engine as dme
dme.hook()
ctx = dme.read_word(0x800000d4)
d = dme.read_bytes(ctx, 0x1c8); w = struct.unpack('>114I', d)
print(' '.join(f'r{i}={w[i]:08x}' for i in range(32)))
print('cr lr ctr xer', [hex(x) for x in w[32:36]], 'srr0 srr1', hex(w[0x198 // 4]), hex(w[0x19c // 4]))
sp = w[1]
for i in range(10):
    bc = dme.read_word(sp)
    if not (0x80000000 <= bc < 0x81800000): break
    print(hex(sp), '->', hex(bc), 'lr', hex(dme.read_word(bc + 4))); sp = bc
