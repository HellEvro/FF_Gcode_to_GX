"""Сборка и разбор Flashforge .gx (xgcode 1.0)."""

from __future__ import annotations

import os
import shutil
import struct
from dataclasses import dataclass

from gcode_to_gx import GX_BMP_OFFSET, GX_BMP_SIZE, GX_GCODE_OFFSET, GX_HEADER_SIZE
from gcode_to_gx.metadata import PrintMetadata, extract_metadata
from gcode_to_gx.printers.registry import PrinterProfile, resolve_profile
from gcode_to_gx.thumbnail import extract_thumbnail_bmp


MAGIC = b"xgcode 1.0\n\0"


@dataclass
class GxHeader:
    print_time: int
    filament_right_mm: int
    filament_left_mm: int
    multi_extruder_type: int
    layer_height_um: int
    reserved0: int
    perimeter_shells: int
    print_speed: int
    bed_temp: int
    nozzle_right: int
    nozzle_left: int
    reserved1: int


def build_header(meta: PrintMetadata) -> bytes:
    buff = MAGIC
    buff += struct.pack("<4i", 0, GX_BMP_OFFSET, GX_GCODE_OFFSET, GX_GCODE_OFFSET)
    buff += struct.pack(
        "<iiih",
        max(meta.print_time, 1),
        meta.filament_right_mm,
        meta.filament_left_mm,
        meta.multi_extruder_type,
    )
    buff += struct.pack(
        "<8h",
        meta.layer_height_um,
        0,
        meta.perimeter_shells,
        meta.print_speed,
        meta.bed_temp,
        meta.nozzle_right,
        meta.nozzle_left,
        1,
    )
    if len(buff) != GX_HEADER_SIZE:
        raise RuntimeError(f"Header size {len(buff)} != {GX_HEADER_SIZE}")
    return buff


def encode_gx(meta: PrintMetadata, bmp: bytes, gcode_text: str) -> bytes:
    if len(bmp) != GX_BMP_SIZE:
        raise ValueError(f"BMP must be {GX_BMP_SIZE} bytes, got {len(bmp)}")
    gcode_bytes = gcode_text.encode("latin-1", errors="replace")
    return build_header(meta) + bmp + gcode_bytes


def parse_header(data: bytes) -> GxHeader:
    if len(data) < GX_HEADER_SIZE:
        raise ValueError("File too short for GX header")
    if not data.startswith(b"xgcode"):
        raise ValueError("Not an xgcode file")
    print_time, fil_r, fil_l, multi = struct.unpack_from("<iiih", data, 28)
    (
        layer_um,
        reserved0,
        shells,
        speed,
        bed,
        noz_r,
        noz_l,
        reserved1,
    ) = struct.unpack_from("<8h", data, 42)
    return GxHeader(
        print_time=print_time,
        filament_right_mm=fil_r,
        filament_left_mm=fil_l,
        multi_extruder_type=multi,
        layer_height_um=layer_um,
        reserved0=reserved0,
        perimeter_shells=shells,
        print_speed=speed,
        bed_temp=bed,
        nozzle_right=noz_r,
        nozzle_left=noz_l,
        reserved1=reserved1,
    )


def validate_gx_layout(data: bytes) -> None:
    if len(data) < GX_GCODE_OFFSET:
        raise ValueError("GX shorter than gcode offset")
    if data[0:11] != b"xgcode 1.0\n":
        raise ValueError("Bad magic")
    _unk, bmp_off, gcode_off, _dup = struct.unpack_from("<4i", data, 12)
    if bmp_off != GX_BMP_OFFSET or gcode_off != GX_GCODE_OFFSET:
        raise ValueError(f"Unexpected offsets bmp={bmp_off} gcode={gcode_off}")
    if data[GX_BMP_OFFSET : GX_BMP_OFFSET + 2] != b"BM":
        raise ValueError("BMP signature missing at offset 58")


def convert_file(path: str, printer_id: str | None = None) -> PrinterProfile:
    """Читает G-code по path и перезаписывает тем же путём как .gx (для Orca post-process)."""
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        lines = fh.readlines()
    if not lines:
        raise ValueError(f"Empty or unreadable file: {path}")

    profile = resolve_profile(printer_id, lines=lines)
    meta = extract_metadata(lines, profile=profile)
    bmp = extract_thumbnail_bmp(lines)
    gcode_text = "".join(lines)
    gx_data = encode_gx(meta, bmp, gcode_text)

    temp_path = path + ".tmp"
    with open(temp_path, "wb") as out:
        out.write(gx_data)
    shutil.move(temp_path, path)
    if os.path.exists(temp_path):
        os.remove(temp_path)
    return profile
