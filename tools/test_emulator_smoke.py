import asyncio
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

spec = importlib.util.spec_from_file_location("emulator_smoke", Path(__file__).with_name("emulator-smoke.py"))
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


class TestObserverAttachment(unittest.TestCase):
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
