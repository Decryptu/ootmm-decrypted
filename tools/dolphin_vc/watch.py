"""Find N64 RDRAM in Wii MEM1 via the DIAG marker at N64 0x3f0 and report marker stage, MM header bytes, and RDRAM activity."""
import time, sys, hashlib, struct
import dolphin_memory_engine as dme

secs = float(sys.argv[1]) if len(sys.argv) > 1 else 60
for _ in range(60):
    dme.hook()
    if dme.is_hooked(): break
    time.sleep(1)
print('hooked', dme.is_hooked())
MEM1 = 0x80000000; SIZE = 0x1800000
base = None
t0 = time.time(); last = None
while time.time() - t0 < secs:
    try:
        if base is None:
            blob = dme.read_bytes(MEM1, SIZE)
            i = blob.find(b'DIAG')
            while i >= 0:
                if (i - 0x3f0) % 4 == 0 and i >= 0x3f0:
                    base = MEM1 + i - 0x3f0; print(f'{time.time()-t0:5.1f}s rdram base {base:08x}'); break
                i = blob.find(b'DIAG', i + 1)
        if base is not None:
            stage = dme.read_word(base + 0x3f4)
            ctx = dme.read_bytes(base + 0x80000, 16).hex()
            h = hashlib.md5(dme.read_bytes(base, 0x800000)).hexdigest()[:8]
            cur = (stage, ctx, h)
            if cur != last:
                print(f'{time.time()-t0:5.1f}s stage {stage:#x} 0x80080000={ctx} rdram={h}'); last = cur
    except Exception as e:
        print('err', e); dme.un_hook(); dme.hook()
    time.sleep(0.5)
