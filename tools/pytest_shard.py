"""Pytest plugin: run one shard of the suite, so CI can split it across parallel jobs.

Load it with `-p pytest_shard` (tools/ on PYTHONPATH) and set PYTEST_SHARD=<index>/<count>, 1-based. Each test
class lands in exactly one shard, by a stable hash of its name, so every shard together runs the whole suite
and no list of tests needs maintaining. Without PYTEST_SHARD it does nothing.
"""
import os
import zlib


def pytest_collection_modifyitems(config, items) -> None:
    shard = os.environ.get("PYTEST_SHARD")
    if not shard:
        return
    index, count = map(int, shard.split("/"))
    kept, dropped = [], []
    for item in items:
        test_class = item.nodeid.rsplit("::", 1)[0]
        (kept if zlib.crc32(test_class.encode()) % count == index - 1 else dropped).append(item)
    config.hook.pytest_deselected(items=dropped)
    items[:] = kept
