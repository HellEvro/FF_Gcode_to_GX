"""Извлечение PNG-thumbnail из G-code и BMP 80x60 фиксированного размера."""

from __future__ import annotations

import base64
import struct
from io import BytesIO

from PIL import Image

from gcode_to_gx import BMP_HEIGHT, BMP_WIDTH, GX_BMP_SIZE


def _raw_bmp_rgb(image: Image.Image) -> bytes:
    """Несжатый BMP (BI_RGB) ровно GX_BMP_SIZE байт — иначе съедет offset G-code."""
    img = image.convert("RGB").resize((BMP_WIDTH, BMP_HEIGHT), Image.Resampling.LANCZOS)
    row_stride = BMP_WIDTH * 3  # 240, кратно 4
    pixels = bytearray()
    # BMP снизу вверх
    for y in range(BMP_HEIGHT - 1, -1, -1):
        row = bytearray()
        for x in range(BMP_WIDTH):
            r, g, b = img.getpixel((x, y))
            row.extend((b, g, r))
        pixels.extend(row)
        pad = (-row_stride) % 4
        if pad:
            pixels.extend(b"\x00" * pad)

    file_header = struct.pack(
        "<2sIHHI",
        b"BM",
        GX_BMP_SIZE,
        0,
        0,
        54,
    )
    info_header = struct.pack(
        "<IIIHHIIIIII",
        40,
        BMP_WIDTH,
        BMP_HEIGHT,
        1,
        24,
        0,
        len(pixels),
        2835,
        2835,
        0,
        0,
    )
    data = file_header + info_header + bytes(pixels)
    if len(data) != GX_BMP_SIZE:
        raise RuntimeError(f"BMP size {len(data)} != {GX_BMP_SIZE}")
    return data


def blank_bmp() -> bytes:
    return _raw_bmp_rgb(Image.new("RGB", (BMP_WIDTH, BMP_HEIGHT), color=(255, 255, 255)))


def extract_thumbnail_bmp(lines: list[str]) -> bytes:
    chunks: list[str] = []
    inside = False
    for line in lines:
        if "thumbnail begin" in line:
            inside = True
            continue
        if "thumbnail end" in line:
            break
        if inside:
            chunks.append(line.strip().lstrip(";").strip())

    if not chunks:
        return blank_bmp()

    try:
        png_data = base64.b64decode("".join(chunks), validate=False)
        image = Image.open(BytesIO(png_data))
        return _raw_bmp_rgb(image)
    except Exception:
        return blank_bmp()
