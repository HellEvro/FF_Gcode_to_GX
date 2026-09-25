"""Профили Flashforge-принтеров для GX-конвертера."""

from __future__ import annotations

from gcode_to_gx.printers.registry import (
    PRINTER_IDS,
    PrinterProfile,
    detect_dual_from_gcode,
    get_profile,
    list_profiles,
    resolve_profile,
)

__all__ = [
    "PRINTER_IDS",
    "PrinterProfile",
    "detect_dual_from_gcode",
    "get_profile",
    "list_profiles",
    "resolve_profile",
]
