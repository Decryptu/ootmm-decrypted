"""Find the OOTxMM mailbox in a running Wii Virtual Console game without writing to RAM."""

import argparse
import struct
import time
from collections.abc import Callable


MAGIC = b"OoTMM-IPC-RAM-1\x00"
HEADER_SIZE = 0x28
RING_SIZE = 0x800
CHUNK_SIZE = 0x100000
REGIONS = {"MEM1": (0x80000000, 24 << 20), "MEM2": (0x90000000, 64 << 20)}
ReadMemory = Callable[[int, int], bytes]


def reverse_words(data: bytes) -> bytes:
    swapped = bytearray(len(data))
    for index in range(4):
        swapped[index::4] = data[3 - index::4]
    return bytes(swapped)


SIGNATURES = {"big-endian": MAGIC, "word-swapped": reverse_words(MAGIC)}


def find_candidates(read: ReadMemory, base: int, size: int) -> list[tuple[int, str]]:
    candidates = []
    for offset in range(0, size, CHUNK_SIZE):
        data = read(base + offset, min(CHUNK_SIZE, size - offset))
        # Each chunk starts on a 16-byte boundary, so an aligned signature fits in one chunk.
        for layout, signature in SIGNATURES.items():
            match = data.find(signature)
            while match != -1:
                if match % 16 == 0 and offset + match + HEADER_SIZE + 2 * RING_SIZE <= size:
                    candidates.append((base + offset + match, layout))
                match = data.find(signature, match + 1)
    return candidates


def sample(read: ReadMemory, candidates: list[tuple[int, str]]) -> dict[tuple[int, str], int]:
    counters = {}
    for address, layout in candidates:
        header = read(address, HEADER_SIZE)
        if layout == "word-swapped":
            header = reverse_words(header)
        if header[:16] == MAGIC:
            connected, alive, *offsets = struct.unpack_from(">6I", header, 16)
            if connected in (0, 1) and all(offset < RING_SIZE for offset in offsets):
                counters[address, layout] = alive
    return counters


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", choices=REGIONS, help="scan only this Wii RAM bank")
    args = parser.parse_args()

    try:
        import dolphin_memory_engine as dolphin
    except ImportError:
        parser.exit(2, "Install dolphin-memory-engine in the Python environment running this probe.\n")

    dolphin.hook()
    if not dolphin.is_hooked():
        parser.exit(2, "Could not attach to Dolphin. Start the WAD and enter gameplay first.\n")

    candidates = []
    failed_reads = 0
    try:
        for region in (args.region,) if args.region else REGIONS:
            try:
                candidates.extend(find_candidates(dolphin.read_bytes, *REGIONS[region]))
            except RuntimeError as error:
                failed_reads += 1
                print(f"Could not scan {region}: {error}")
        before = sample(dolphin.read_bytes, candidates)
        time.sleep(0.25)
        after = sample(dolphin.read_bytes, candidates)
    except RuntimeError as error:
        parser.exit(2, f"Could not sample the mailbox: {error}\n")
    finally:
        dolphin.un_hook()

    live = False
    for (address, layout), alive in before.items():
        current = after.get((address, layout))
        if current is not None and current != alive:
            print(f"Live mailbox at 0x{address:08X} ({layout}), alive {alive} -> {current}")
            live = True
    if not live:
        print(f"No live mailbox observed ({len(candidates)} aligned signature matches). "
              "Retry while actively playing, after the title screen and file select.")
    if live:
        return 0
    return 2 if failed_reads else 1


if __name__ == "__main__":
    raise SystemExit(main())
