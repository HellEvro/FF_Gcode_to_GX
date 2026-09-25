from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from gcode_to_gx import GX_BMP_SIZE, GX_GCODE_OFFSET
from gcode_to_gx.gx_writer import convert_file, parse_header, validate_gx_layout
from gcode_to_gx.metadata import extract_metadata
from gcode_to_gx.printers import PRINTER_IDS, detect_dual_from_gcode, get_profile, resolve_profile
from gcode_to_gx.thumbnail import blank_bmp, extract_thumbnail_bmp


FIXTURE_DUAL = Path(__file__).parent / "fixtures" / "sample_dual.gcode"
FIXTURE_SINGLE = Path(__file__).parent / "fixtures" / "sample_single.gcode"


def test_metadata_dual():
    lines = FIXTURE_DUAL.read_text(encoding="utf-8").splitlines(keepends=True)
    meta = extract_metadata(lines, profile=get_profile("creator3pro"))
    assert meta.print_time == 3723
    assert meta.filament_right_mm == 1234
    assert meta.filament_left_mm == 678
    assert meta.layer_height_um == 200
    assert meta.bed_temp == 60
    assert meta.nozzle_right == 220
    assert meta.nozzle_left == 210
    assert meta.multi_extruder_type == 1
    assert meta.perimeter_shells == 3


def test_metadata_single_profile_zeros_left():
    lines = FIXTURE_DUAL.read_text(encoding="utf-8").splitlines(keepends=True)
    meta = extract_metadata(lines, profile=get_profile("adventurer5m"))
    assert meta.filament_right_mm == 1234
    assert meta.filament_left_mm == 0
    assert meta.nozzle_left == 0
    assert meta.multi_extruder_type == 0


def test_bmp_exact_size():
    assert len(blank_bmp()) == GX_BMP_SIZE
    lines = FIXTURE_DUAL.read_text(encoding="utf-8").splitlines(keepends=True)
    bmp = extract_thumbnail_bmp(lines)
    assert len(bmp) == GX_BMP_SIZE
    assert bmp[:2] == b"BM"


def test_convert_dual_creator3pro(tmp_path: Path):
    target = tmp_path / "job.gx"
    shutil.copy(FIXTURE_DUAL, target)
    profile = convert_file(str(target), printer_id="creator3pro")
    assert profile.id == "creator3pro"
    data = target.read_bytes()
    validate_gx_layout(data)
    assert len(data) > GX_GCODE_OFFSET
    header = parse_header(data)
    assert header.multi_extruder_type == 1
    assert header.filament_left_mm == 678
    assert header.nozzle_left == 210
    payload = data[GX_GCODE_OFFSET:]
    assert b"G28" in payload
    assert b"T1" in payload


def test_convert_single_adventurer5m(tmp_path: Path):
    target = tmp_path / "single.gx"
    shutil.copy(FIXTURE_SINGLE, target)
    profile = convert_file(str(target), printer_id="adventurer5m")
    assert profile.id == "adventurer5m"
    data = target.read_bytes()
    validate_gx_layout(data)
    header = parse_header(data)
    assert header.multi_extruder_type == 0
    assert header.filament_right_mm == 890
    assert header.filament_left_mm == 0
    assert header.nozzle_right == 210
    assert header.nozzle_left == 0


def test_auto_detect_dual_and_single():
    dual_lines = FIXTURE_DUAL.read_text(encoding="utf-8").splitlines(keepends=True)
    single_lines = FIXTURE_SINGLE.read_text(encoding="utf-8").splitlines(keepends=True)
    assert detect_dual_from_gcode(dual_lines) is True
    assert detect_dual_from_gcode(single_lines) is False
    assert resolve_profile(lines=dual_lines).id == "generic_dual"
    assert resolve_profile(lines=single_lines).id == "generic_single"


def test_env_printer_overrides_auto(monkeypatch: pytest.MonkeyPatch):
    dual_lines = FIXTURE_DUAL.read_text(encoding="utf-8").splitlines(keepends=True)
    monkeypatch.setenv("GCODE_TO_GX_PRINTER", "adventurer3")
    assert resolve_profile(lines=dual_lines).id == "adventurer3"
    monkeypatch.delenv("GCODE_TO_GX_PRINTER")
    assert resolve_profile(printer_id="creator3pro", lines=dual_lines).id == "creator3pro"


def test_all_printer_ids_registered():
    expected = {
        "adventurer3",
        "adventurer4",
        "adventurer5m",
        "creator3pro",
        "generic_single",
        "generic_dual",
    }
    assert set(PRINTER_IDS) == expected


def test_cli_main(tmp_path: Path):
    from gcode_to_gx.cli import main

    target = tmp_path / "out.gx"
    shutil.copy(FIXTURE_DUAL, target)
    assert main([str(target)]) == 0
    validate_gx_layout(target.read_bytes())
    assert main([]) == 2


def test_cli_printer_flag(tmp_path: Path):
    from gcode_to_gx.cli import main

    target = tmp_path / "out.gx"
    shutil.copy(FIXTURE_SINGLE, target)
    assert main(["--printer", "adventurer4", str(target)]) == 0
    header = parse_header(target.read_bytes())
    assert header.multi_extruder_type == 0


def test_calibrate_missing_reference(tmp_path: Path):
    target = tmp_path / "ours.gx"
    shutil.copy(FIXTURE_DUAL, target)
    convert_file(str(target), printer_id="generic_dual")
    validate_gx_layout(target.read_bytes())
