"""ROM identity and pickup checks shared by isolated gameplay observers."""
import asyncio


async def wait_for_rom(peer, bizhawk, expected_sha1=None, timeout=30, connect=None):
    """The Lua socket can be ready before the N64 core exposes its ROM domain."""
    connect = connect or (lambda: bizhawk.connect(peer.bizhawk_ctx))
    async with asyncio.timeout(timeout):
        while True:
            try:
                if peer.bizhawk_ctx.streams is None and not await connect():
                    await asyncio.sleep(0.25)
                    continue
                if await peer.handler.validate_rom(peer):
                    if expected_sha1 is not None:
                        actual = (await bizhawk.get_hash(peer.bizhawk_ctx)).upper()
                        if actual != expected_sha1.upper():
                            raise ValueError(f"Connector ROM hash mismatch: {actual}")
                        return actual
                    return
            except (bizhawk.RequestFailedError, bizhawk.NotConnectedError):
                pass
            await asyncio.sleep(0.25)


def verify_pickup_award(context, get_received_items, source, location):
    item, recipient, _flags = context.locations[source][location]
    for target in context.slot_set(recipient):
        queued = get_received_items(context, 0, target, True)
        assert sum(entry.location == location and entry.player == source and entry.item == item
                   for entry in queued) == 1, f"Pickup must queue exactly one award for slot {target}"
    return item, recipient
