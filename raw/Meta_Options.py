# Settings the world never offers, whatever raw/GenerateMetadata.py finds about them.
# The generator decides the rest itself (see "Options" in DEVELOPMENT.md): a setting OoTMM's code reads
# outside conditions is not offered until the world ports its effect.

# Meaningless in a multiworld: Archipelago runs the multiworld, writes the spoiler and places the hints.
NotOffered = [
    "games",
    "mode",
    "players",
    "teams",
    "distinctWorlds",
    "triforceSharedMulti",
    "generateSpoilerLog",
    "probabilisticFoolishness",
    "noPlandoHints",
    "noDuplicatePlaythroughHints",
    "extraHintRegions",
    "hintPathDungeons",
    "hintPathBoss",
    "hintPathEndBoss",
    "hintPathEvents",
    "hintImportance",
    # Their "custom" value takes its requirements from specialConds, which is not ported.
    "lacs",
    "rainbowBridge",
    "majoraChild",
]

# Categories whose settings OoTMM reads through computed keys, which the source scan can't see:
# items.mmAgeRequirements (core/src/mm-age-requirements.ts) changes what each age can use in MM.
NotOfferedCategories = [
    "items.mmAgeRequirements",
]
