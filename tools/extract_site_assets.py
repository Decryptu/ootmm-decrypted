"""Export the player hub's original game UI assets from the owner's NTSC-U ROMs.

Requires Pillow. Run from any directory; ROMs default to the ignored roms/ folder.
Only the PNG assets listed here are written. ROM data is never copied into the site.
"""
import argparse
import json
from pathlib import Path
import struct
import zlib

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'site' / 'assets'


def yaz0(data):
    if data[:4] != b'Yaz0':
        raise ValueError('Expected a Yaz0 texture archive member')
    size = int.from_bytes(data[4:8], 'big')
    result = bytearray()
    pos = 16
    while len(result) < size:
        code = data[pos]
        pos += 1
        for bit in range(7, -1, -1):
            if len(result) >= size:
                break
            if code & (1 << bit):
                result.append(data[pos])
                pos += 1
            else:
                first, second = data[pos:pos + 2]
                pos += 2
                distance = ((first & 15) << 8) | second
                count = first >> 4
                if count == 0:
                    count = data[pos] + 18
                    pos += 1
                else:
                    count += 2
                for _ in range(count):
                    result.append(result[-distance - 1])
    return bytes(result)


def decode(data, width, height, fmt):
    if fmt == 'rgba32':
        return Image.frombytes('RGBA', (width, height), data[:width * height * 4])
    pixels = []
    for i in range(width * height):
        if fmt == 'ia8':
            intensity, alpha = (data[i] >> 4) * 17, (data[i] & 15) * 17
        elif fmt in ('ia4', 'i4'):
            value = (data[i // 2] >> (4 if i % 2 == 0 else 0)) & 15
            if fmt == 'ia4':
                intensity, alpha = (value >> 1) * 255 // 7, (value & 1) * 255
            else:
                intensity = alpha = value * 17
        elif fmt == 'i8':
            intensity = alpha = data[i]
        else:
            raise ValueError(f'Unsupported texture format: {fmt}')
        pixels.append((intensity, intensity, intensity, alpha))
    image = Image.new('RGBA', (width, height))
    image.putdata(pixels)
    return image


def tint(image, color):
    result = image.copy()
    result.putdata([(r * color[0] // 255, g * color[1] // 255,
                     b * color[2] // 255, a)
                    for r, g, b, a in image.get_flattened_data()])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rom-dir', type=Path, default=ROOT / 'roms')
    args = parser.parse_args()
    roms = {}
    for game, crc in [('oot', 0xcd16c529), ('mm', 0xb428d8a7)]:
        data = (args.rom_dir / f'{game}.z64').read_bytes()
        if zlib.crc32(data) != crc:
            raise ValueError(f'{game}: expected the supported big-endian NTSC-U ROM')
        roms[game] = data
    manifest = json.loads((ASSETS / 'game-assets.json').read_text())
    banks, textures = {}, {}
    for name, spec in manifest.items():
        game, index = spec['game'], spec['dma_index']
        key = (game, index)
        if key not in banks:
            table = 0x7430 if game == 'oot' else 0x1a500
            start, end, physical, compressed_end = struct.unpack_from(
                '>4I', roms[game], table + index * 16)
            if physical == 0xffffffff:
                raise ValueError(f'{name}: file is not present in this ROM')
            data = roms[game][physical:compressed_end or physical + end - start]
            banks[key] = yaz0(data) if compressed_end else data
        data = banks[key]
        if 'archive_index' in spec:
            member = spec['archive_index']
            base = struct.unpack_from('>I', data, 0)[0]
            offset = struct.unpack_from('>I', data, member * 4)[0] if member else 0
            data = yaz0(data[base + offset:])
        else:
            data = data[int(spec['Offset'], 16):]
        textures[name] = decode(data, int(spec['Width']), int(spec['Height']), spec['Format'])

    def save(image, name):
        image.save(ASSETS / name)

    for symbol, name in [
        ('oot-gQuestIconDungeonMapTex', 'menu-guide.png'),
        ('oot-gItemIconOcarinaOfTimeTex', 'menu-ocarina.png'),
        ('oot-gQuestIconDungeonBossKeyTex', 'menu-package.png'),
        ('oot-gItemIconHammerTex', 'menu-tools.png'),
        ('mm-gItemIconBombersNotebookTex', 'menu-notebook.png'),
        ('mm-gItemIconMaskOfTruthTex', 'menu-mask.png'),
    ]:
        save(textures[symbol], name)
    stone = textures['oot-gPauseGameOver10Tex']
    material = stone.crop((0, 2, 80, 18))
    save(tint(material, (175, 181, 123)), 'pause-stone.png')
    save(tint(material, (43, 56, 38)), 'pause-dark.png')
    frame = Image.new('RGBA', (240, 160))
    for row in range(5):
        for col in range(3):
            # The blank game-over stone replaces the SAVE caption; page titles are HTML.
            tile = stone if (col, row) == (1, 0) else textures[f'oot-gPauseSave{col}{row}Tex']
            frame.paste(tint(tile, (175, 181, 123)), (col * 80, row * 32))
    save(frame, 'pause-frame.png')
    for name, color, glyph in [('a', (70, 100, 255), 'gABtnSymbolTex'),
                               ('b', (0, 170, 0), 'gBBtnSymbolTex')]:
        button = tint(textures['oot-gButtonBackgroundTex'], color)
        symbol = textures['oot-' + glyph]
        button.alpha_composite(symbol, ((32 - symbol.width) // 2, (32 - symbol.height) // 2))
        save(button, f'button-{name}.png')
    save(tint(textures['oot-gOcarinaBtnIconCDownTex'], (255, 210, 0)), 'button-c.png')
    save(tint(textures['oot-gHeartFullTex'], (255, 70, 50)), 'heart.png')
    cursor = Image.new('RGBA', (32, 32))
    for corner, xy in [('TopLeft', (0, 0)), ('TopRight', (16, 0)),
                       ('BottomLeft', (0, 16)), ('BottomRight', (16, 16))]:
        cursor.paste(textures[f'oot-gPauseMenuCursor{corner}Tex'], xy)
    save(cursor, 'cursor.png')
    caption = Image.new('RGBA', (144, 24))
    for side, x in [('Left', 0), ('Right', 72)]:
        caption.paste(tint(textures[f'oot-gNamePanel{side}Tex'], (80, 100, 150)), (x, 0))
    save(caption, 'name-panel.png')
    message = textures['oot-gDefaultMessageBackgroundTex'].copy()
    message.putdata([(5, 10, 8, a) for _, _, _, a in message.get_flattened_data()])
    save(message, 'message-box.png')
    print('Exported player hub icons and UI textures.')


if __name__ == '__main__':
    main()
