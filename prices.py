"""Shop costs following OoTMM's logic/src/price.ts, carried unchanged into the ROM."""
from . import logic, ootxmm_staticdata

SETTINGS = {"priceOotShops", "priceMmShops"}


def generate(settings, random):
    data = ootxmm_staticdata.OOTxMMLogic
    result = list(data["prices"])
    maximum, beta = 100, 5
    if logic._value(settings, "colossalWallets"):
        maximum, beta = 199, 12
        if logic._value(settings, "bottomlessWallets"):
            maximum, beta = 999, 20
    for key, ranges in (("priceOotShops", ("OOT_SHOPS",)),
                        ("priceMmShops", ("MM_SHOPS", "MM_SHOPS_EX"))):
        mode = logic._value(settings, key)
        for group in ranges:
            base = data["priceRanges"][group]
            for slot in range(base, base + data["priceCounts"][group]):
                if mode == "affordable":
                    result[slot] = 10
                elif mode == "random":
                    result[slot] = random.randrange(maximum + 1) * 5
                elif mode == "weighted":
                    result[slot] = sorted(random.randrange(maximum + 1) for _ in range(beta + 1))[1] * 5
                elif mode != "vanilla":
                    raise ValueError(f"Unknown shop price mode: {mode}")
    return result
