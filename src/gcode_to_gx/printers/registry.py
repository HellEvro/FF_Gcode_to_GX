"""Реестр профилей принтеров Flashforge (shared GX layout)."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PrinterProfile:
    """Профиль принтера. Разметка GX общая; отличается dual/single metadata."""

    id: str
    name: str
    dual: bool
    # Flashforge: 0 = single, 1 = dual (independent / IDEX-style)
    multi_extruder_type: int


_PROFILES: dict[str, PrinterProfile] = {
    "adventurer3": PrinterProfile(
        id="adventurer3",
        name="Flashforge Adventurer 3",
        dual=False,
        multi_extruder_type=0,
    ),
    "adventurer4": PrinterProfile(
        id="adventurer4",
        name="Flashforge Adventurer 4",
        dual=False,
        multi_extruder_type=0,
    ),
    "adventurer5m": PrinterProfile(
        id="adventurer5m",
        name="Flashforge Adventurer 5M",
        dual=False,
        multi_extruder_type=0,
    ),
    "creator3pro": PrinterProfile(
        id="creator3pro",
        name="Flashforge Creator 3 Pro",
        dual=True,
        multi_extruder_type=1,
    ),
    "generic_single": PrinterProfile(
        id="generic_single",
        name="Generic Flashforge (single extruder)",
        dual=False,
        multi_extruder_type=0,
    ),
    "generic_dual": PrinterProfile(
        id="generic_dual",
        name="Generic Flashforge (dual extruder)",
        dual=True,
        multi_extruder_type=1,
    ),
}

PRINTER_IDS: tuple[str, ...] = tuple(_PROFILES.keys())

_ENV_PRINTER = "GCODE_TO_GX_PRINTER"


def list_profiles() -> list[PrinterProfile]:
    return [_PROFILES[pid] for pid in PRINTER_IDS]


def get_profile(printer_id: str) -> PrinterProfile:
    key = printer_id.strip().lower()
    if key not in _PROFILES:
        known = ", ".join(PRINTER_IDS)
        raise ValueError(f"Unknown printer '{printer_id}'. Known IDs: {known}")
    return _PROFILES[key]


def detect_dual_from_gcode(lines: list[str]) -> bool:
    """Определяет dual по комментариям Orca / toolchange T1."""
    filament_vals: list[float] = []
    nozzle_vals: list[float] = []
    has_t1 = False

    for line in lines:
        stripped = line.strip()
        if re.match(r"^T1\b", stripped, flags=re.IGNORECASE):
            has_t1 = True
        if not stripped.startswith(";"):
            continue
        body = stripped[1:].strip()
        if "=" not in body:
            continue
        key, _, raw = body.partition("=")
        key = key.strip().lower()
        value = raw.strip()
        if key.startswith("filament used [mm]"):
            filament_vals = _float_list(value)
        elif key in ("nozzle_temperature", "first_layer_temperature"):
            nozzle_vals = _float_list(value)

    if len(filament_vals) >= 2 and filament_vals[1] > 0:
        return True
    if len(nozzle_vals) >= 2:
        return True
    if has_t1:
        return True
    return False


def resolve_profile(
    printer_id: str | None = None,
    *,
    lines: list[str] | None = None,
    env: dict[str, str] | None = None,
) -> PrinterProfile:
    """
    Приоритет: явный printer_id → env GCODE_TO_GX_PRINTER → auto-detect → generic_*.
    """
    if printer_id:
        return get_profile(printer_id)

    environ = env if env is not None else os.environ
    env_id = (environ.get(_ENV_PRINTER) or "").strip()
    if env_id:
        return get_profile(env_id)

    if lines is not None:
        dual = detect_dual_from_gcode(lines)
        return get_profile("generic_dual" if dual else "generic_single")

    return get_profile("generic_dual")


def _float_list(value: str) -> list[float]:
    parts = [p.strip() for p in value.split(",") if p.strip()]
    out: list[float] = []
    for part in parts:
        try:
            out.append(float(part.replace(",", ".")))
        except ValueError:
            continue
    return out
