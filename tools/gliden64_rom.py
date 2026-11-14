"""Create a combined ROM copy that GLideN64 recognizes as a Zelda game."""

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rom", type=Path, help="Combined OoTMM .z64 ROM")
    parser.add_argument("output_directory", type=Path, help="Directory for the new ROM copy")
    args = parser.parse_args()

    try:
        rom = bytearray(args.rom.read_bytes())
        if rom[:4] != b"\x80\x37\x12\x40" or rom[0x20:0x34] != b"OOT+MM COMBO        ":
            parser.error("Expected a big-endian OoTMM ROM with the original combined title")

        # GLideN64's MASK match enables both Zelda monochrome and MM rendering behavior.
        # Keep the prefix the Archipelago client uses to recognize the combined ROM.
        rom[0x20:0x34] = b"OOT+MM COMBO MASK   "
        args.output_directory.mkdir(parents=True, exist_ok=True)
        output = args.output_directory / args.rom.name
        file = output.open("xb")
        try:
            with file:
                file.write(rom)
        except OSError:
            output.unlink()
            raise
    except OSError as error:
        parser.exit(1, f"{error}\n")
    print(output)


if __name__ == "__main__":
    main()
