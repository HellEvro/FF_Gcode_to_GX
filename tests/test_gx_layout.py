from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from gcode_to_gx import GX_BMP_SIZE, GX_GCODE_OFFSET
from gcode_to_gx.gx_writer import convert_file, parse_header, validate_gx_layout
from gcode_to_gx.metadata import extract_metadata
from gcode_to_gx.thumbnail import blank_bmp, extract_thumbnail_bmp


FIXTURE = Path(__file__).parent / "fixtures" / "sample_dual.gcode"


def test_metadata_dual():
    lines = FIXTURE.read_text(encoding="utf-8").splitlines(keepends=True)
    meta = extract_metadata(lines)
    assert meta.print_time == 3723
    assert meta.filament_right_mm == 1234
    assert meta.filament_left_mm == 678
    assert meta.layer_height_um == 200
    assert meta.bed_temp == 60
    assert meta.nozzle_right == 220
    assert meta.nozzle_left == 210
    assert meta.multi_extruder_type == 1
    assert meta.perimeter_shells == 3


def test_bmp_exact_size():
    assert len(blank_bmp()) == GX_BMP_SIZE
    lines = FIXTURE.read_text(encoding="utf-8").splitlines(keepends=True)
    bmp = extract_thumbnail_bmp(lines)
    assert len(bmp) == GX_BMP_SIZE
    assert bmp[:2] == b"BM"


def test_convert_in_place(tmp_path: Path):
    target = tmp_path / "job.gx"
    shutil.copy(FIXTURE, target)
    convert_file(str(target))
    data = target.read_bytes()
    validate_gx_layout(data)
    assert len(data) > GX_GCODE_OFFSET
    header = parse_header(data)
    assert header.multi_extruder_type == 1
    assert header.filament_left_mm == 678
    assert header.nozzle_left == 210
    # G-code payload starts at offset
    payload = data[GX_GCODE_OFFSET:]
    assert b"G28" in payload
    assert b"T1" in payload


def test_cli_main(tmp_path: Path):
    from gcode_to_gx.cli import main

    target = tmp_path / "out.gx"
    shutil.copy(FIXTURE, target)
    assert main([str(target)]) == 0
    validate_gx_layout(target.read_bytes())
    assert main([]) == 2


def test_calibrate_missing_reference(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # скрипт calibrate использует путь по умолчанию — проверяем parse только layout
    target = tmp_path / "ours.gx"
    shutil.copy(FIXTURE, target)
    convert_file(str(target))
    validate_gx_layout(target.read_bytes())
