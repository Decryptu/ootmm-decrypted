import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, Mock, patch

spec = importlib.util.spec_from_file_location("emulator_smoke", Path(__file__).with_name("emulator-smoke.py"))
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


class TestObserverAttachment(unittest.TestCase):
    def test_stability_requires_successful_polls_and_rejects_changed_receipts(self):
        poll = AsyncMock(side_effect=[False, None, True, False, *([True] * 15)])
        verify = Mock()
        with patch.object(smoke.asyncio, "sleep", new_callable=AsyncMock):
            asyncio.run(smoke.verify_stable_polls(poll, verify))
        self.assertEqual(poll.await_count, 19)
        self.assertEqual(verify.call_count, 16)
        with patch.object(smoke.asyncio, "sleep", new_callable=AsyncMock):
            with self.assertRaisesRegex(AssertionError, "changed"):
                asyncio.run(smoke.verify_stable_polls(
                    AsyncMock(return_value=True), Mock(side_effect=AssertionError("changed"))))

    def test_pickup_abort_boundaries_retain_and_retry_only_once(self):
        for boundary in ("before-send", "after-accept"):
            with self.subTest(boundary=boundary):
                accepted = set()
                socket = SimpleNamespace(transport=SimpleNamespace(abort=Mock()), wait_closed=AsyncMock())
                peer = SimpleNamespace(locations_checked={12}, server=SimpleNamespace(socket=socket),
                                       disconnect=AsyncMock())

                async def send(messages):
                    if not socket.transport.abort.called:
                        accepted.add(12)

                peer.send_msgs = AsyncMock(side_effect=send)
                fault = smoke.PickupInterruption(peer, {12}, lambda: accepted, boundary)
                message = [{"cmd": "LocationChecks", "locations": [12]}]
                asyncio.run(fault.send_msgs(message))
                self.assertEqual(fault.evidence["server_accepted_at_abort"], boundary == "after-accept")
                self.assertEqual(peer.locations_checked, {12})
                asyncio.run(fault.send_msgs(message))
                socket.transport.abort.assert_called_once()
                peer.disconnect.assert_awaited_once()
                self.assertEqual(peer.send_msgs.await_count, 2)

    def test_pickup_abort_requires_retention_and_new_check(self):
        for retained, accepted in ((set(), set()), ({12}, {12})):
            peer = SimpleNamespace(locations_checked=retained, send_msgs=AsyncMock())
            fault = smoke.PickupInterruption(peer, {12}, lambda: accepted, "before-send")
            with self.assertRaises(AssertionError):
                asyncio.run(fault.send_msgs([{"cmd": "LocationChecks", "locations": [12]}]))
            peer.send_msgs.assert_not_awaited()

    def test_pickup_abort_ignores_login_and_other_checks(self):
        peer = SimpleNamespace(send_msgs=AsyncMock())
        fault = smoke.PickupInterruption(peer, {12}, lambda: set(), "before-send")
        for messages in ([{"cmd": "Connect"}], [{"cmd": "LocationChecks", "locations": [13]}]):
            asyncio.run(fault.send_msgs(messages))
        self.assertIsNone(fault.evidence)
        self.assertEqual(peer.send_msgs.await_count, 2)

    def test_disconnect_checks_original_mailbox_after_watcher_clears_cache(self):
        peer = SimpleNamespace(handler=SimpleNamespace(mailbox=0x1000, last_query=2),
                               disconnect=AsyncMock(), bizhawk_ctx=object())

        async def poll():
            peer.handler.mailbox = peer.handler.last_query = None

        api = SimpleNamespace(read=AsyncMock(return_value=[bytes(4)]))
        self.assertEqual(asyncio.run(smoke.disconnect_game(peer, poll, api)), 2)
        api.read.assert_awaited_once_with(peer.bizhawk_ctx, [(0x1010, 4, "RDRAM")])
        api.read.return_value = [b'\0\0\0\1']
        peer.handler.mailbox = 0x1000
        with self.assertRaisesRegex(AssertionError, "disconnected server"):
            asyncio.run(smoke.disconnect_game(peer, poll, api))

    def test_offline_save_waits_for_complete_successful_result(self):
        path = Mock()
        path.read_text.side_effect = [FileNotFoundError(), '{"passed":', '{"passed": true}']
        with patch.object(smoke.asyncio, "sleep", new_callable=AsyncMock) as sleep:
            self.assertEqual(asyncio.run(smoke.wait_for_scenario_result(path, 1)), {"passed": True})
        self.assertEqual(sleep.await_count, 2)

    def test_offline_save_rejects_failed_or_missing_result(self):
        for value in ('{"passed": false}', '{}'):
            with self.subTest(value=value), self.assertRaisesRegex(AssertionError, "scenario failed"):
                asyncio.run(smoke.wait_for_scenario_result(Mock(read_text=Mock(return_value=value)), 1))
        with self.assertRaises(TimeoutError):
            asyncio.run(smoke.wait_for_scenario_result(Mock(read_text=Mock(side_effect=FileNotFoundError())), 0))

    def setup_peer(self, validation):
        peer = SimpleNamespace(bizhawk_ctx=SimpleNamespace(streams=True),
                               handler=SimpleNamespace(validate_rom=AsyncMock(side_effect=validation)))
        api = SimpleNamespace(RequestFailedError=OSError, NotConnectedError=ConnectionError,
                              get_hash=AsyncMock(return_value="AB" * 20), connect=AsyncMock(return_value=True))
        return peer, api

    def test_waits_for_rom_domain_and_checks_identity(self):
        peer, api = self.setup_peer([False, OSError("Core is loading"), True])
        with patch.object(smoke.asyncio, "sleep", new_callable=AsyncMock):
            actual = asyncio.run(smoke.wait_for_rom(peer, api, "ab" * 20))
        self.assertEqual(actual, "AB" * 20)
        self.assertEqual(peer.handler.validate_rom.await_count, 3)
        api.get_hash.assert_awaited_once()

    def test_wrong_rom_fails_before_gameplay(self):
        peer, api = self.setup_peer([True])
        with self.assertRaisesRegex(ValueError, "ROM hash mismatch"):
            asyncio.run(smoke.wait_for_rom(peer, api, "cd" * 20))

    def test_coordinator_reconnects_with_its_own_port_range(self):
        peer, api = self.setup_peer([True])
        peer.bizhawk_ctx.streams = None

        async def connect():
            peer.bizhawk_ctx.streams = True
            return True

        connector = AsyncMock(side_effect=connect)
        actual = asyncio.run(smoke.wait_for_rom(peer, api, "ab" * 20, connect=connector))
        self.assertEqual(actual, "AB" * 20)
        connector.assert_awaited_once()
        api.connect.assert_not_awaited()

    def test_startup_has_a_wall_clock_bound(self):
        peer, api = self.setup_peer([False])
        with self.assertRaises(TimeoutError):
            asyncio.run(smoke.wait_for_rom(peer, api, timeout=0))


if __name__ == "__main__":
    unittest.main()
