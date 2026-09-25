"""Парсинг метаданных из комментариев Orca G-code."""

from __future__ import annotations

from dataclasses import dataclass

from gcode_to_gx.printers.registry import PrinterProfile


@dataclass
class PrintMetadata:
    print_time: int = 0
    filament_right_mm: int = 0
    filament_left_mm: int = 0
    layer_height_um: int = 0
    print_speed: int = 60
    bed_temp: int = 0
    nozzle_right: int = 0
    nozzle_left: int = 0
    multi_extruder_type: int = 1
    perimeter_shells: int = 2


def _parse_float_token(raw: str) -> float:
    return float(raw.strip().replace(",", "."))


def _parse_int_list(value: str) -> list[int]:
    """Разбор '220,210' или '220.0, 210.0' или одного значения с десятичной запятой."""
    parts = [p.strip() for p in value.split(",")]
    if len(parts) >= 2:
        try:
            return [int(_parse_float_token(p)) for p in parts if p]
        except ValueError:
            pass
    try:
        return [int(_parse_float_token(value))]
    except ValueError:
        return []


def _parse_print_time(value: str) -> int:
    h = m = s = 0
    for part in value.strip().split():
        if part.endswith("h"):
            h = int(part[:-1] or "0")
        elif part.endswith("m"):
            m = int(part[:-1] or "0")
        elif part.endswith("s"):
            s = int(part[:-1] or "0")
    return h * 3600 + m * 60 + s


def extract_metadata(
    lines: list[str],
    profile: PrinterProfile | None = None,
) -> PrintMetadata:
    meta = PrintMetadata()
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith(";"):
            continue
        body = stripped[1:].strip()
        if "=" not in body:
            continue
        key, _, raw = body.partition("=")
        key = key.strip().lower()
        value = raw.strip()

        if key.startswith("estimated printing time (normal mode)"):
            meta.print_time = _parse_print_time(value)
        elif key.startswith("filament used [mm]"):
            vals = _parse_int_list(value)
            if vals:
                meta.filament_right_mm = vals[0]
            if len(vals) > 1:
                meta.filament_left_mm = vals[1]
        elif key == "layer_height":
            try:
                meta.layer_height_um = int(_parse_float_token(value.split()[0]) * 1000)
            except (ValueError, IndexError):
                pass
        elif key.startswith("machine_max_speed_x"):
            vals = _parse_int_list(value)
            if vals:
                # Orca часто даёт пару лимитов; берём разумную скорость печати
                meta.print_speed = vals[-1] if len(vals) > 1 else vals[0]
        elif key in ("first_layer_bed_temperature", "bed_temperature"):
            vals = _parse_int_list(value)
            if vals:
                meta.bed_temp = vals[0]
        elif key in ("nozzle_temperature", "first_layer_temperature"):
            vals = _parse_int_list(value)
            if vals:
                meta.nozzle_right = vals[0]
            if len(vals) > 1:
                meta.nozzle_left = vals[1]
        elif key in ("wall_loops", "wall_line_count"):
            vals = _parse_int_list(value)
            if vals:
                meta.perimeter_shells = vals[0]

    if meta.print_time < 1:
        meta.print_time = 1

    if profile is not None:
        apply_profile(meta, profile)

    return meta


def apply_profile(meta: PrintMetadata, profile: PrinterProfile) -> PrintMetadata:
    """Применяет dual/single флаги профиля к уже распарсенным метаданным."""
    meta.multi_extruder_type = profile.multi_extruder_type
    if not profile.dual:
        meta.filament_left_mm = 0
        meta.nozzle_left = 0
    return meta
