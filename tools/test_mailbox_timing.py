import unittest

from mailbox_timing import MailboxTiming


class TestMailboxTiming(unittest.TestCase):
    def test_discovery_switch_and_same_address_recovery(self):
        now = [100.0]
        timing = MailboxTiming(lambda: now[0])
        timing.observe(None, None, 100.0)
        now[0] = 102.0
        timing.observe(0x1000, 0, 101.5)
        self.assertEqual(timing.recoveries, [])  # Initial discovery is not a recovery.
        now[0] = 110.0
        timing.observe(None, None, 109.0)
        now[0] = 112.0
        self.assertIsNone(timing.observe(None, None, 111.0))
        now[0] = 115.0
        timing.observe(0x2000, 1, 112.0)
        now[0] = 120.0
        timing.observe(None, None, 120.0)
        now[0] = 122.0
        timing.observe(0x2000, 1, 122.0)
        self.assertEqual(timing.recoveries, [
            {"from_mailbox": 0x1000, "to_mailbox": 0x2000, "seconds": 5.0},
            {"from_mailbox": 0x2000, "to_mailbox": 0x2000, "seconds": 2.0}])
        self.assertEqual(timing.history[-1]["elapsed_seconds"], 22.0)
        self.assertEqual(timing.report()["poll_count"], 7)
        self.assertEqual(timing.report()["max_poll_seconds"], 3.0)
        self.assertIsNone(timing.report()["pending_recovery_seconds"])

    def test_unfinished_recovery_is_retained_for_failed_report(self):
        now = [0.0]
        timing = MailboxTiming(lambda: now[0])
        timing.observe(0x1000, 3, 0.0)
        now[0] = 1.0
        timing.observe(None, None, 1.0)
        now[0] = 9.0
        self.assertEqual(timing.report()["pending_recovery_seconds"], 8.0)
        self.assertEqual(timing.report()["recoveries"], [])


if __name__ == "__main__":
    unittest.main()
