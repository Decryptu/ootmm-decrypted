"""Follow the diagnostic marker: 0x1xx = OoT play frames, 0x2xx = MM play frames, small = switch stages."""
import time, sys, dolphin_memory_engine as dme
secs = float(sys.argv[1]) if len(sys.argv) > 1 else 300
B = 0x80f1d0e0
while True:
    dme.hook()
    if dme.is_hooked(): break
    time.sleep(1)
t0 = time.time(); last = None; game = None; switches = 0
while time.time() - t0 < secs:
    try:
        if dme.read_word(B + 0x3f0) != 0x44494147:
            time.sleep(0.5); continue
        st = dme.read_word(B + 0x3f4)
    except Exception:
        time.sleep(0.5); continue
    g = 'OoT' if st & 0xf00 == 0x100 else 'MM' if st & 0xf00 == 0x200 else f'switch {st}'
    if g != game:
        print(f'{time.time()-t0:6.1f}s {g}', flush=True); game = g
        if g.startswith('switch'): switches += 1
    time.sleep(0.25)
print('done')
