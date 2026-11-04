"""Stage the player hub and shared guides for GitHub Pages' Jekyll build."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "dist" / "pages-source"


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
    ]:
        content = (ROOT / "docs" / source).read_text(encoding="utf-8")
        (DEST / target).write_text(
            f"---\nlayout: default\ntitle: {title}\n---\n\n{content}", encoding="utf-8")
    print(DEST)


if __name__ == "__main__":
    main()
