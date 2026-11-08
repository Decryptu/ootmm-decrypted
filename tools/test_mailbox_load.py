import struct
import unittest

from mailbox_load import MailboxLoad


def header(oh=0, ot=0, ih=0, it=0, connected=1):
    return b"OoTMM-IPC-RAM-1\x00" + struct.pack(">6I", connected, 123, oh, ot, ih, it)


class TestMailboxLoad(unittest.TestCase):
    def test_wrapped_rings_and_high_water_survive_drain(self):
        load = MailboxLoad()
        load.observe(header(oh=10, ot=2040, ih=2047))
        load.observe(header())
        report = load.report()
        self.assertEqual(report["max_outgoing_bytes"], 18)
        self.assertEqual(report["max_incoming_bytes"], 2047)
        self.assertEqual(report["last"]["incoming_bytes"], 0)
        self.assertEqual(report["samples"], 2)

    def test_reject_stale_or_invalid_headers(self):
        load = MailboxLoad()
        for value in (b"", bytes(40), header(ot=2048), header(ih=0xffffffff)):
            load.observe(value)
        self.assertEqual(load.report()["invalid_headers"], 4)
        self.assertEqual(load.report()["samples"], 0)
        self.assertIsNone(load.report()["last"])

    def test_disconnect_and_empty_ring(self):
        load = MailboxLoad()
        load.observe(header(oh=2047, ot=2047, connected=0))
        self.assertEqual(load.report()["disconnected_samples"], 1)
        self.assertEqual(load.report()["max_outgoing_bytes"], 0)
