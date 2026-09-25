# Optional Orca machine G-code — Flashforge Creator 3 Pro

**Optional.** Paste into Orca printer custom G-code fields. Not official Flashforge
firmware or documentation; not endorsed by Flashforge. Adapt placeholders to your
Orca version and firmware.

These files do **not** replace the G-code→`.gx` post-processing converter in this repo.
You still need the binary / script in **Post-processing scripts**.

## Files

| File | Orca field (RU UI ≈) |
|------|----------------------|
| [`machine_start.gcode`](machine_start.gcode) | Machine start G-code / стартовый G-код |
| [`machine_end.gcode`](machine_end.gcode) | Machine end G-code / завершающий G-код |
| [`machine_pause.gcode`](machine_pause.gcode) | Print pause G-code / G-код паузы печати |

## Notes

- **Start** — provided by the printer owner (Creator 3 Pro); use as-is in Orca, then tune.
- **End** — owner’s “end” paste was identical to start. `machine_end.gcode` is a **short
  cooling/present placeholder** until a real end snippet is supplied. **Review before use.**
- **Pause** — from owner’s Orca UI: `; pause print` + `M2000`.
