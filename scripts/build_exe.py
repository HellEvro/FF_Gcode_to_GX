"""Сборка standalone gcode_to_gx.exe для Orca post-processing."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "src" / "gcode_to_gx" / "cli.py"
DIST = ROOT / "dist"


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        "gcode_to_gx",
        "--paths",
        str(ROOT / "src"),
        str(ENTRY),
    ]
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        return result.returncode
    exe = DIST / "gcode_to_gx.exe"
    if exe.exists():
        print(f"OK: {exe}")
        print("Orca / Process / Other / Post-processing scripts:")
        print(f'  "{exe}"')
    else:
        print("PyInstaller finished but exe not found", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
