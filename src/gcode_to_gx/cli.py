"""CLI для Orca post-processing: gcode_to_gx.exe <path>."""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 1:
        print(
            "Usage: gcode_to_gx <path-to-gcode-or-gx-temp-file>\n"
            "Orca передаёт один путь к временному файлу; файл перезаписывается как .gx.",
            file=sys.stderr,
        )
        return 2

    path = args[0]
    try:
        from gcode_to_gx.gx_writer import convert_file

        convert_file(path)
    except Exception as exc:  # noqa: BLE001 — нужен полный лог для Orca
        print(f"gcode_to_gx ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"gcode_to_gx OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
