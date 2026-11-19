"""Locate the five thread functions the VC emulator patches (libraryFindFunctions), from a boot image."""
import struct

def op(x): return x >> 26

def find_funcs(rd, exc):
    """rd(addr) -> u32. Returns dict name -> patch address (where VC writes its opcode)."""
    out = {}
    a = exc; enq = disp = None
    while True:
        o = rd(a)
        if op(o) == 3:
            last = (a & 0xf0000000) | ((o & 0x3ffffff) << 2)
            o2 = rd(a + 8)
            if op(o2) == 2:
                enq = last; disp = (a & 0xf0000000) | ((o2 & 0x3ffffff) << 2)
        a += 4
        if o == 0x400A4000: break
    out['send_mesg'] = a + 0x14
    if enq is not None:
        b = enq
        while True:
            b -= 4
            if rd(b) == 0x40086000: break
        while True:
            b -= 4; o = rd(b)
            if not (op(o) != 0x02 and (o & 0xFFFF0000) != 0x10000000 and op(o) != 0x00 and (o & 0x3f) != 0x08): break
        out['__osEnqueueAndYield'] = b + 8
        out['__osEnqueueThread'] = enq
        b = enq + 8
        while True:
            o = rd(b); b += 4
            if o == 0x03E00008: break
        out['__osPopThread'] = b + 4
        out['__osDispatchThread'] = disp
    return out
