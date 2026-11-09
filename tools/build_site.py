"""Stage the player hub and shared guides for GitHub Pages' Jekyll build."""
import ast
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "dist" / "pages-source"


def option_specs() -> dict:
    """The world's options as the hub's settings import needs them, read from options.py without Archipelago."""
    tree = ast.parse((ROOT / "options.py").read_text(encoding="utf-8"))
    names = next(ast.literal_eval(node.value) for node in tree.body
                 if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "OOTMM_SETTINGS")
    specs = {}
    for node in tree.body:
        if not isinstance(node, ast.ClassDef) or not node.name.startswith("OOTxMM_"):
            continue
        key = node.name.removeprefix("OOTxMM_")
        if key not in names:
            continue
        kind = node.bases[0].id
        fields = {target.id: stmt.value for stmt in node.body if isinstance(stmt, ast.Assign)
                  for target in stmt.targets if isinstance(target, ast.Name)}
        if kind == "Choice":
            values = ast.literal_eval(fields["ootmm_values"])
            default = fields.get("default")
            index = 0 if default is None else ast.literal_eval(fields[default.id]) if isinstance(
                default, ast.Name) else ast.literal_eval(default)
            specs[key] = {"type": "choice", "values": values, "default": values[index]}
            aliases = {value: name.removeprefix("option_").lower()
                       for name, expr in fields.items() if name.startswith("option_")
                       for value in [values[ast.literal_eval(expr)]]
                       if value.lower() != name.removeprefix("option_").lower()}
            if aliases:
                specs[key]["aliases"] = aliases
        elif kind in ("Toggle", "DefaultOnToggle"):
            specs[key] = {"type": "toggle", "default": kind == "DefaultOnToggle"}
        elif kind == "OptionSet":
            specs[key] = {"type": "set", "values": ast.literal_eval(fields["valid_keys"]), "default": []}
        else:
            raise ValueError(f"{node.name}: unsupported option type {kind}")
    missing = set(names) - set(specs)
    if missing:
        raise ValueError(f"Options without a class: {sorted(missing)}")
    return specs


def item_names() -> dict:
    """OoTMM item IDs to the world's item names (items.py names items from the same dump)."""
    items = json.loads((ROOT / "raw" / "GreatItemJSONdump.json").read_text(encoding="utf-8"))
    return {item["id"]: item["name"] for item in items}


def main():
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "site", DEST, dirs_exist_ok=True)
    (DEST / "assets").mkdir(exist_ok=True)
    shutil.copy2(ROOT / "assets" / "ootmm-decrypted.png", DEST / "assets")
    for source, target, title in [
        ("setup_en.md", "setup.md", "Setup guide"),
        ("en_OOTxMM.md", "game.md", "About the game"),
        ("playtest_en.md", "playtest.md", "Playtest checklist"),
    ]:
        content = (ROOT / "docs" / source).read_text(encoding="utf-8")
        content = content.replace("](setup_en.md)", "](setup.html)")
        (DEST / target).write_text(
            f"---\nlayout: default\ntitle: {title}\n---\n\n{content}", encoding="utf-8")
    # The settings import needs the world's options, and OoTMM's defaults to tell which other settings a player changed.
    defaults = json.loads((ROOT / "raw" / "GreatSettingsJSONdump.json").read_text(encoding="utf-8"))["defaults"]
    (DEST / "options.json").write_text(json.dumps(
        {"options": option_specs(), "ootmmDefaults": defaults, "itemNames": item_names()},
        separators=(",", ":")), encoding="utf-8")
    print(DEST)


if __name__ == "__main__":
    main()
