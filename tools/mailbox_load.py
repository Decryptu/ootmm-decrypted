"""Read-only, sampled ring pressure for disposable gameplay tests."""
import struct


class MailboxLoad:
    def __init__(self):
        self.samples = 0
        self.invalid_headers = 0
        self.disconnected_samples = 0
        self.max_outgoing_bytes = 0
        self.max_incoming_bytes = 0
        self.last = None

    def observe(self, header):
        if len(header) != 40 or header[:16] != b"OoTMM-IPC-RAM-1\x00":
            self.invalid_headers += 1
            return
        connected, alive, oh, ot, ih, it = struct.unpack_from(">6I", header, 16)
        if any(offset >= 2048 for offset in (oh, ot, ih, it)):
            self.invalid_headers += 1
            return
        outgoing, incoming = (oh - ot) % 2048, (ih - it) % 2048
        self.samples += 1
        self.disconnected_samples += connected == 0
        self.max_outgoing_bytes = max(self.max_outgoing_bytes, outgoing)
        self.max_incoming_bytes = max(self.max_incoming_bytes, incoming)
        self.last = {"alive": alive, "connected": connected,
                     "outgoing_bytes": outgoing, "incoming_bytes": incoming}

    def report(self):
        return {"samples": self.samples, "invalid_headers": self.invalid_headers,
                "disconnected_samples": self.disconnected_samples,
                "capacity_bytes": 2048, "usable_bytes": 2047,
                "max_outgoing_bytes": self.max_outgoing_bytes,
                "max_incoming_bytes": self.max_incoming_bytes, "last": self.last,
                "limits": "Snapshots around client polls; peaks between samples and packet latency are not measured"}

    async def sample(self, peer, bizhawk):
        mailbox = peer.handler.mailbox
        if mailbox is not None:
            header, = await bizhawk.read(peer.bizhawk_ctx, [(mailbox, 40, "RDRAM")])
            self.observe(header)
