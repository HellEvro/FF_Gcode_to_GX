# Optional machine G-code — Flashforge Creator 3 Pro

**OPTIONAL templates only.** Not official Flashforge firmware or documentation.
Not affiliated with or endorsed by Flashforge. Copy into your Orca (or other slicer)
machine start / end / toolchange fields and **adapt** for your firmware revision,
firmware quirks, and print mode (single vs dual IDEX).

These snippets are derived from public community Cura profiles for Creator 3 / Creator 3 Pro
(notably [tdwiser/ffc3pro_cura](https://github.com/tdwiser/ffc3pro_cura), itself based on
community Thingiverse profiles) plus forum notes about Flashforge temperature ordering
(`M104 S… T…`). They are **starting points**, not guaranteed working profiles.

## Files

| File | Paste into (Orca) |
|------|-------------------|
| [`start.gcode`](start.gcode) | Machine start G-code (dual / IDEX-oriented) |
| [`end.gcode`](end.gcode) | Machine end G-code |
| [`toolchange.gcode`](toolchange.gcode) | Tool change / filament change G-code |

## How to use with Orca

1. Create or import a dual-extruder printer profile for Creator 3 Pro (community discussion:
   [OrcaSlicer#9577](https://github.com/SoftFever/OrcaSlicer/issues/9577)).
2. Paste the snippets into the matching custom G-code fields.
3. Replace or verify placeholders (`{…}`) for your Orca version.
4. Still use this repo’s converter as a **post-processing script** so the file becomes `.gx`
   (see root README). Machine G-code alone does **not** add the Flashforge binary header.

## Safety notes

- Creator 3 Pro firmware is picky about command order (e.g. `M104 S220 T0`, not `M104 T0 S220`).
- Some lines use Flashforge-specific codes (`M118`, `M6`, `M7`, `M108`, `M651` / `M652`, `G162`).
  If your firmware rejects a command, remove or replace it after checking a known-good FlashPrint export.
- Prime-line coordinates assume a roughly centered bed (~±145 X, ±120 Y). Adjust for your
  printable area and nozzle offsets.
- Always dry-run / first-layer watch when trying a new start G-code.
