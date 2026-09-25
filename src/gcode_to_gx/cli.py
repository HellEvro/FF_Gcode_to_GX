"""CLI для Orca post-processing: gcode_to_gx [--printer ID] PATH."""

from __future__ import annotations

import argparse
import sys

from gcode_to_gx.gx_writer import convert_file
from gcode_to_gx.printers.registry import PRINTER_IDS


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gcode_to_gx",
        description=(
            "Конвертер Orca G-code → Flashforge .gx. "
            "Orca передаёт путь к временному файлу последним аргументом; "
            "файл перезаписывается как .gx."
        ),
    )
    parser.add_argument(
        "--printer",
        "-p",
        metavar="ID",
        help=(
            "ID профиля принтера. "
            f"Доступно: {', '.join(PRINTER_IDS)}. "
            "Либо переменная окружения GCODE_TO_GX_PRINTER. "
            "Без флага — auto-detect dual/single по G-code."
        ),
    )
    parser.add_argument(
        "path",
        help="Путь к временному G-code / .gx от Orca (последний аргумент).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args_list = list(sys.argv[1:] if argv is None else argv)
    if not args_list:
        _build_parser().print_help(sys.stderr)
        return 2

    parser = _build_parser()
    try:
        args = parser.parse_args(args_list)
    except SystemExit as exc:
        code = exc.code
        return int(code) if isinstance(code, int) else 2

    try:
        profile = convert_file(args.path, printer_id=args.printer)
    except Exception as exc:  # noqa: BLE001 — нужен полный лог для Orca
        print(f"gcode_to_gx ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"gcode_to_gx OK: {args.path} (printer={profile.id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
