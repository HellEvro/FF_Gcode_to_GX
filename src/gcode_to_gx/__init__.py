"""Конвертер Orca G-code → Flashforge .gx (dual + превью)."""

__version__ = "1.0.0"

GX_HEADER_SIZE = 58
GX_BMP_OFFSET = 58
GX_GCODE_OFFSET = 14512
GX_BMP_SIZE = GX_GCODE_OFFSET - GX_BMP_OFFSET  # 14454
BMP_WIDTH = 80
BMP_HEIGHT = 60
