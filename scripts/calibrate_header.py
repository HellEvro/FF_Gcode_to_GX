"""Сверка шапки нашего GX с эталоном FlashPrint (если файл положен)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gcode_to_gx.gx_writer import parse_header, validate_gx_layout


def compare(ours: Path, reference: Path) -> int:
    our_data = ours.read_bytes()
    ref_data = reference.read_bytes()
    validate_gx_layout(our_data)
    validate_gx_layout(ref_data)

    a = parse_header(our_data)
    b = parse_header(ref_data)
    print("=== Наш файл ===")
    print(a)
    print("=== FlashPrint эталон ===")
    print(b)

    fields = [
        "multi_extruder_type",
        "filament_right_mm",
        "filament_left_mm",
        "nozzle_right",
        "nozzle_left",
        "bed_temp",
        "layer_height_um",
    ]
    diffs = []
    for name in fields:
        va, vb = getattr(a, name), getattr(b, name)
        if va != vb:
            diffs.append(f"  {name}: ours={va} ref={vb}")

    # offsets / magic уже через validate
    print("=== Diff (ключевые поля) ===")
    if diffs:
        print("\n".join(diffs))
        print(
            "Отличия в числах нормальны (разный слайс); "
            "важно: multi_extruder_type и наличие dual temps/filament."
        )
    else:
        print("Ключевые поля совпали.")

    if a.multi_extruder_type != b.multi_extruder_type:
        print(
            "ВНИМАНИЕ: multi_extruder_type отличается — "
            "проверьте dual-режим на принтере.",
            file=sys.stderr,
        )
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Сверка GX header с FlashPrint")
    parser.add_argument("ours", type=Path, help="Наш .gx")
    parser.add_argument(
        "reference",
        type=Path,
        nargs="?",
        default=Path("tests/fixtures/flashprint_dual.gx"),
        help="Эталон FlashPrint (по умолчанию tests/fixtures/flashprint_dual.gx)",
    )
    args = parser.parse_args()
    if not args.reference.exists():
        print(
            f"Эталон не найден: {args.reference}\n"
            "Сохраните двухголовый .gx из FlashPrint (Creator 3 Pro) по этому пути "
            "и запустите снова.",
            file=sys.stderr,
        )
        return 2
    if not args.ours.exists():
        print(f"Нет файла: {args.ours}", file=sys.stderr)
        return 2
    return compare(args.ours, args.reference)


if __name__ == "__main__":
    raise SystemExit(main())
