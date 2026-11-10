"""Bundle the Windows host helper with this checkout's matching patch sources."""
import argparse
import hashlib
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def package(output):
    files = [ROOT / name for name in (
        "Host Setup.cmd", "tools/host-setup.ps1", "tools/ootmm-build.sh",
        "docs/setup_en.md", "LICENSE",
    )]
    for folder in ("ootmm-ap", "ootmm-patches"):
        files.extend(p for p in sorted((ROOT / folder).iterdir()) if p.is_file())
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED) as archive:
        for source in files:
            archive.writestr("ootxmm-host/" + source.relative_to(ROOT).as_posix(),
                             source.read_bytes().replace(b"\r\n", b"\n"))
    output.with_suffix(output.suffix + ".sha256").write_text(
        hashlib.sha256(output.read_bytes()).hexdigest() + "  " + output.name + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    package(parser.parse_args().output)
