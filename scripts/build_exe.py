"""Сборка standalone gcode_to_gx для Orca post-processing (текущая ОС)."""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "src" / "gcode_to_gx" / "cli.py"
DIST = ROOT / "dist"
BASE_NAME = "gcode_to_gx"


def _platform_tag() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if machine in ("amd64", "x86_64"):
        arch = "x64"
    elif machine in ("arm64", "aarch64"):
        arch = "arm64"
    else:
        arch = machine
    if system == "windows":
        return f"windows-{arch}"
    if system == "darwin":
        return f"macos-{arch}"
    if system == "linux":
        return f"linux-{arch}"
    return f"{system}-{arch}"


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        BASE_NAME,
        "--paths",
        str(ROOT / "src"),
        str(ENTRY),
    ]
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        return result.returncode

    if sys.platform == "win32":
        local = DIST / f"{BASE_NAME}.exe"
        release_name = f"{BASE_NAME}-{_platform_tag()}.exe"
    else:
        local = DIST / BASE_NAME
        release_name = f"{BASE_NAME}-{_platform_tag()}"

    if not local.exists():
        print(f"PyInstaller finished but binary not found: {local}", file=sys.stderr)
        return 1

    release = DIST / release_name
    shutil.copy2(local, release)
    print(f"OK: {local}")
    print(f"OK: {release}")
    print("Orca / Process / Other / Post-processing scripts:")
    print(f'  "{local}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
