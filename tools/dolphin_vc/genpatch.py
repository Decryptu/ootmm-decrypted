"""Generate OoTMM PATCH_START files that move libultra's scheduler variables to a shared low-memory block."""
import sys, struct
sys.path.insert(0, r'C:\t\vc')
from romfiles import files
from reloc import scan, remap

R = r'C:\path\to\ootmm-decrypted\roms'
SHARED_Q, SHARED_MASK, SHARED_EVT = 0x80000200, 0x80000210, 0x80000220

GAMES = {
    'oot': dict(dma=0x7430, files={0x1060: 0x80000460, 0xa87000: 0x800110a0},
                q=0x80006338, mask=0x80006360, evt=0x80009de0),
    'mm': dict(dma=0x1a500, files={0x1060: 0x80080060},
               q=0x80097e18, mask=0x80097e60, evt=0x8009e510),
}

def gen(name, g):
    rom = open(rf'{R}\{name}.z64', 'rb').read()
    maps = [(g['q'], g['q'] + 0x10, SHARED_Q), (g['mask'], g['mask'] + 4, SHARED_MASK), (g['evt'], g['evt'] + 0x80, SHARED_EVT)]
    out = []
    for vs, data in files(rom, g['dma']):
        if vs not in g['files']: continue
        vram = g['files'][vs]
        data = data[:len(data) // 4 * 4]
        w, sites = scan(data, vram, maps)
        new = list(w)
        for i, hi, uses, hits in sites:
            vals = [remap(a, maps) for j, a in uses]
            assert all(v is not None for v in vals), (name, hex(vram + 4 * i))
            nh = {((v + 0x8000) >> 16) & 0xffff for v in vals}
            assert len(nh) == 1
            nh = nh.pop()
            new[i] = (w[i] & 0xffff0000) | nh
            for (j, a), v in zip(uses, vals):
                new[j] = (w[j] & 0xffff0000) | ((v - (nh << 16)) & 0xffff)
        for i, (a, b) in enumerate(zip(w, new)):
            if a != b: out.append((vram + 4 * i, b))
    return out

for name, g in GAMES.items():
    p = gen(name, g)
    lines = ['#include <combo.h>', '',
             '/* Move libultra scheduler variables to a block shared by both games (see switch.c),',
             '   generated from the vanilla ROM. */', '']
    for a, v in p:
        lines += [f'PATCH_START 0x{a:08x}', f'  .word 0x{v:08x}', 'PATCH_END', '']
    open(rf'C:\t\vc\vc_libultra_{name}.S', 'w', newline='\n').write('\n'.join(lines))
    print(name, len(p), 'words')
