"""Dolphin support: play the combined ROM through Majora's Mask on the Wii Virtual Console (NARE).

"OOTxMM Dolphin Setup" puts a patched ROM into the Virtual Console title installed in Dolphin's NAND. Dolphin
keeps installed titles decrypted, so no Wii keys are needed. "OOTxMM Dolphin Client" serves the BizHawk
connector protocol from Dolphin's memory and opens the normal BizHawk Client, so the OOTxMM handler runs unchanged.
"""
from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import socket
import struct
import threading
import time
from pathlib import Path

from worlds.LauncherComponents import Component, Type, components, launch as launch_component

logger = logging.getLogger("Client")

TITLE_PATH = ("Wii", "title", "00010001", "4e415245", "content")  # Majora's Mask NTSC-U Virtual Console
GAME_SETTINGS = "NAR.ini"
# The patches below give the N64 ROM 64 MiB in MEM2, so Dolphin must emulate 128 MiB of MEM2.
GAME_SETTINGS_TEXT = "[Core]\nRAMOverrideEnable = True\nMEM1Size = 25165824\nMEM2Size = 134217728\n"
RDRAM_BASE = 0x80F1D0E0  # the emulated N64 RAM inside Wii MEM1
RDRAM_SIZE = 8 << 20
MEM1 = (0x80000000, 24 << 20)
PORTS = range(43055, 43060)


# --- Virtual Console title patching -------------------------------------------------------------------------

def lz10_decode(data: bytes) -> bytearray:
    if data[0] != 0x10:
        raise ValueError("content 1 is not LZ10 compressed")
    size = int.from_bytes(data[1:4], "little")
    out = bytearray()
    i = 4
    while len(out) < size:
        flags = data[i]
        i += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                x = data[i] << 8 | data[i + 1]
                i += 2
                start = len(out) - (x & 0xFFF) - 1
                for k in range((x >> 12) + 3):
                    out.append(out[start + k])
            else:
                out.append(data[i])
                i += 1
    return out


def lz10_encode(data: bytes) -> bytes:
    # Literal blocks only: valid LZ10, about 12% larger than the input.
    out = bytearray(b"\x10" + len(data).to_bytes(3, "little"))
    for i in range(0, len(data), 8):
        out.append(0)
        out += data[i:i + 8]
    out += bytes(-len(out) % 4)
    return bytes(out)


def dol_offset(dol: bytes, address: int) -> int:
    offsets = struct.unpack_from(">18I", dol, 0)
    addresses = struct.unpack_from(">18I", dol, 72)
    sizes = struct.unpack_from(">18I", dol, 144)
    for offset, start, size in zip(offsets, addresses, sizes):
        if size and start <= address < start + size:
            return offset + address - start
    raise ValueError(f"{address:#x} is not in the executable")


def patch_words(dol: bytearray, address: int, original: list[int], patched: list[int]) -> None:
    """Apply a patch, or accept it if it is already applied."""
    offset = dol_offset(dol, address)
    current = list(struct.unpack_from(f">{len(patched)}I", dol, offset))
    if current == patched:
        return
    if current[:len(original)] != original:
        raise ValueError(f"Unexpected code at {address:#x}: this is not the NTSC-U Majora's Mask Virtual Console")
    struct.pack_into(f">{len(patched)}I", dol, offset, *patched)


def patch_content7(dol: bytearray) -> None:
    patch_words(dol, 0x813310C4, [0x40800058], [0x48000058])


def patch_content1(dol: bytearray) -> None:
    # Room for a 64 MiB ROM: a smaller general MEM2 heap and the ROM in its own buffer at 0x93800000.
    patch_words(dol, 0x80089640, [0x3C000400], [0x3C000360])
    patch_words(dol, 0x80089650, [0x3F990400], [0x3F990360])
    patch_words(dol, 0x800528DC, [0x40800028], [0x3C009380, 0x901F0004, 0x38000000, 0x900D8F40, 0x4800004C])
    # S2DEX backgrounds: the emulator replaces every background with MM's framebuffer copy for an MM ROM ID.
    # OoT pre-rendered rooms (shops, houses) keep their image in segment 0x03; send those to the normal draw.
    patch_words(dol, 0x80070124, [0x40820044, 0x38E00000], [
        0x40820034, 0x4BFFFFA0,
        0x7CBA2B78, 0x7F23CB78, 0x7F44D378, 0x38A10058, 0x4BFFA12D,
        0x88010068, 0x28000003, 0x4082011C, 0x7F23CB78, 0x7F45D378, 0x480000F8,
        0x88010068, 0x28000003, 0x4182FF68, 0x48000004])
    patch_words(dol, 0x80070248, [0x4182001C], [0x4182FEE4])
    # Saves: write the flash image to NAND whenever it changed, not at most once every 6 minutes.
    patch_words(dol, 0x8007E580, [0x41820034], [0x48000034])


def u8_replace(archive: bytes, name: str, data: bytes) -> bytes:
    """Rebuild a U8 archive with one file's data replaced."""
    if archive[:4] != b"\x55\xAA\x38\x2D":
        raise ValueError("content 5 is not a U8 archive")
    root, header_size, data_start = struct.unpack_from(">III", archive, 4)
    count = struct.unpack_from(">I", archive, root + 8)[0]
    names = root + count * 12
    nodes = [list(struct.unpack_from(">III", archive, root + i * 12)) for i in range(count)]
    found = False
    out = bytearray()
    for node in nodes:
        if node[0] >> 24:
            continue  # directory
        node_name = archive[names + (node[0] & 0xFFFFFF):].split(b"\0", 1)[0].decode()
        content = data if node_name == name else archive[node[1]:node[1] + node[2]]
        found |= node_name == name
        out += bytes(-(data_start + len(out)) % 32)
        node[1], node[2] = data_start + len(out), len(content)
        out += content
    if not found:
        raise ValueError(f"content 5 has no {name}")
    head = bytearray(archive[:data_start])
    for i, node in enumerate(nodes):
        struct.pack_into(">III", head, root + i * 12, *node)
    return bytes(head + out)


def install(rom_path: Path, user_dir: Path) -> None:
    rom = bytearray(rom_path.read_bytes())
    if rom[:4] != b"\x80\x37\x12\x40" or not rom[0x20:0x34].startswith(b"OOT+MM COMBO"):
        raise ValueError("Choose the patched OoTMM .z64 ROM built from your Dolphin patch.")
    rom[0x3B:0x3F] = b"NZSE"  # the Virtual Console only runs this ROM with Majora's Mask's cartridge ID

    content = user_dir.joinpath(*TITLE_PATH)
    tmd_path = content / "title.tmd"
    if not tmd_path.is_file():
        raise ValueError(f"Majora's Mask Virtual Console (NARE) is not installed in {user_dir}. "
                         "In Dolphin, use Tools > Install WAD to Wii Menu with your own Majora's Mask WAD first.")
    tmd = bytearray(tmd_path.read_bytes())
    records = {}
    for i in range(struct.unpack_from(">H", tmd, 0x1DE)[0]):
        cid, index = struct.unpack_from(">IH", tmd, 0x1E4 + 36 * i)
        records[index] = (0x1E4 + 36 * i, content / f"{cid:08x}.app")

    def update(index: int, data: bytes) -> None:
        record, path = records[index]
        path.write_bytes(data)
        struct.pack_into(">Q20s", tmd, record + 8, len(data), hashlib.sha1(data).digest())

    c7 = bytearray(records[7][1].read_bytes())
    patch_content7(c7)
    c1 = lz10_decode(records[1][1].read_bytes())
    patch_content1(c1)
    c5 = u8_replace(records[5][1].read_bytes(), "romc", struct.pack(">I", len(rom) << 2) + rom)
    update(7, c7)
    update(1, lz10_encode(c1))
    update(5, c5)
    tmd_path.write_bytes(tmd)

    settings = user_dir / "GameSettings"
    settings.mkdir(exist_ok=True)
    (settings / GAME_SETTINGS).write_text(GAME_SETTINGS_TEXT, encoding="utf-8")


def dolphin_user_dirs() -> list[Path]:
    candidates = []
    if os.name == "nt":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Dolphin Emulator") as key:
                candidates.append(Path(winreg.QueryValueEx(key, "UserConfigPath")[0]))
        except OSError:
            pass
        for base in (os.environ.get("APPDATA"), Path.home() / "Documents"):
            if base:
                candidates.append(Path(base) / "Dolphin Emulator")
    else:
        candidates += [Path.home() / ".local/share/dolphin-emu", Path.home() / ".dolphin-emu",
                       Path.home() / "Library/Application Support/Dolphin"]
    return [path for path in candidates if path.joinpath(*TITLE_PATH, "title.tmd").is_file()]


def run_setup(*args: str) -> None:
    import Utils
    try:
        rom = args[0] if args else Utils.open_filename("Choose your patched OoTMM ROM (Dolphin patch)",
                                                         [("N64 ROM", [".z64"])])
        if not rom:
            return
        found = dolphin_user_dirs()
        user_dir = args[1] if len(args) > 1 else (found[0] if found else Utils.open_directory(
            "Choose Dolphin's user folder (File > Open User Folder in Dolphin)"))
        if not user_dir:
            return
        install(Path(rom), Path(user_dir))
        Utils.messagebox("OOTxMM Dolphin Setup", "Done. Start \"The Legend of Zelda: Majora's Mask\" in Dolphin, "
                         "then open OOTxMM Dolphin Client.")
    except Exception as exc:
        Utils.messagebox("OOTxMM Dolphin Setup", str(exc), error=True)
        raise


# --- BizHawk connector protocol over Dolphin memory ---------------------------------------------------------

class Bridge:
    def __init__(self) -> None:
        import dolphin_memory_engine
        self.dolphin = dolphin_memory_engine
        self.header: bytes | None = None

    def ready(self) -> bool:
        if not self.dolphin.is_hooked():
            self.header = None
            self.dolphin.hook()
            if not self.dolphin.is_hooked():
                return False
        if self.header is None:
            self.header = self.find_header()
        return self.header is not None

    def find_header(self) -> bytes | None:
        # The Virtual Console keeps copies of the ROM header in MEM1; the ROM itself is in MEM2, out of reach.
        base, size = MEM1
        for offset in range(0, size, 1 << 20):
            chunk = self.dolphin.read_bytes(base + offset, 1 << 20)
            index = chunk.find(b"OOT+MM COMBO")
            while index != -1:
                start = index - 0x20
                if start >= 0 and chunk[start:start + 4] == b"\x80\x37\x12\x40":
                    return bytes(chunk[start:start + 0x40])
                index = chunk.find(b"OOT+MM COMBO", index + 1)
        return None

    def read(self, domain: str, address: int, size: int) -> bytes:
        if domain == "ROM" and 0 <= address and address + size <= 0x40:
            return self.header[address:address + size]
        if domain != "RDRAM" or address < 0 or address + size > RDRAM_SIZE:
            raise ValueError(f"Cannot read {domain} {address:#x}+{size:#x} on Dolphin")
        return self.dolphin.read_bytes(RDRAM_BASE + address, size)

    def handle(self, req: dict) -> dict:
        kind = req["type"]
        if kind == "PING":
            return {"type": "PONG"}
        if kind == "SYSTEM":
            return {"type": "SYSTEM_RESPONSE", "value": "N64"}
        if kind == "PREFERRED_CORES":
            return {"type": "PREFERRED_CORES_RESPONSE", "value": {"N64": "Dolphin"}}
        if kind == "HASH":
            return {"type": "HASH_RESPONSE", "value": hashlib.sha1(self.header).hexdigest().upper()}
        if kind == "MEMORY_SIZE":
            return {"type": "MEMORY_SIZE_RESPONSE", "value": RDRAM_SIZE if req["domain"] == "RDRAM" else 0x40}
        if kind == "GUARD":
            expected = base64.b64decode(req["expected_data"])
            valid = self.read(req["domain"], req["address"], len(expected)) == expected
            return {"type": "GUARD_RESPONSE", "value": valid, "address": req["address"]}
        if kind == "LOCK":
            return {"type": "LOCKED"}
        if kind == "UNLOCK":
            return {"type": "UNLOCKED"}
        if kind == "READ":
            data = self.read(req["domain"], req["address"], req["size"])
            return {"type": "READ_RESPONSE", "value": base64.b64encode(data).decode("ascii")}
        if kind == "WRITE":
            data = base64.b64decode(req["value"])
            if req["domain"] != "RDRAM" or req["address"] < 0 or req["address"] + len(data) > RDRAM_SIZE:
                raise ValueError(f"Cannot write {req['domain']} {req['address']:#x} on Dolphin")
            self.dolphin.write_bytes(RDRAM_BASE + req["address"], data)
            return {"type": "WRITE_RESPONSE"}
        if kind == "DISPLAY_MESSAGE":
            return {"type": "DISPLAY_MESSAGE_RESPONSE"}
        if kind == "SET_MESSAGE_INTERVAL":
            return {"type": "SET_MESSAGE_INTERVAL_RESPONSE"}
        return {"type": "ERROR", "err": f"Unknown command: {kind}"}

    def process(self, line: str) -> str:
        if line == "VERSION":
            return "1"
        responses = []
        failed_guard = None
        for req in json.loads(line):
            if failed_guard is not None:  # like the Lua connector, a failed guard skips the rest
                responses.append(failed_guard)
                continue
            res = self.handle(req)
            if res["type"] == "GUARD_RESPONSE" and not res["value"]:
                failed_guard = res
            responses.append(res)
        return json.dumps(responses)

    def serve(self, server: socket.socket) -> None:
        waiting_logged = False
        while True:
            conn, _ = server.accept()
            with conn:
                try:
                    # Refuse the client until the game is running; it retries on its own.
                    if not self.ready():
                        if not waiting_logged:
                            logger.info("Dolphin: waiting for the OOTxMM Virtual Console game to start")
                            waiting_logged = True
                        time.sleep(1)
                        continue
                    waiting_logged = False
                    logger.info("Dolphin: game found")
                    with conn.makefile("rb") as reader:
                        for raw in reader:
                            conn.sendall(self.process(raw.decode("utf-8").strip()).encode("utf-8") + b"\n")
                except (OSError, RuntimeError, ValueError) as exc:
                    # Dolphin closed or the game stopped: drop the client and look for the game again.
                    logger.info(f"Dolphin: connection lost ({exc})")
                    self.header = None


def start_bridge() -> None:
    for port in PORTS:
        try:
            server = socket.create_server(("127.0.0.1", port))
            break
        except OSError:
            continue
    else:
        raise OSError("No free connector port between 43055 and 43059")
    threading.Thread(target=Bridge().serve, args=(server,), daemon=True, name="DolphinBridge").start()


def run_client(*args: str) -> None:
    start_bridge()
    from worlds._bizhawk.context import BizHawkClientContext, launch
    make_gui = BizHawkClientContext.make_gui

    def make_dolphin_gui(self):
        ui = make_gui(self)
        ui.base_title = "OOTxMM Dolphin Client"  # the BizHawk title made players think they had the wrong client
        return ui

    BizHawkClientContext.make_gui = make_dolphin_gui
    launch(*args)


def launch_client(*args: str) -> None:
    launch_component(run_client, name="OOTxMMDolphinClient", args=args)


def launch_setup(*args: str) -> None:
    launch_component(run_setup, name="OOTxMMDolphinSetup", args=args)


components.append(Component("OOTxMM Dolphin Client", func=launch_client, component_type=Type.CLIENT,
                            game_name="OOTxMM",
                            description="Play OOTxMM in Dolphin: connects the game to Archipelago."))
components.append(Component("OOTxMM Dolphin Setup", func=launch_setup, component_type=Type.ADJUSTER,
                            game_name="OOTxMM",
                            description="Put your patched OOTxMM ROM into Majora's Mask Virtual Console in Dolphin."))
