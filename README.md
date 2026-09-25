# G-code → GX for Orca Slicer (Flashforge)

[Русский](README.ru.md)

Converter for Orca’s **Post-processing scripts** field: takes the temporary file after slicing, embeds a Flashforge header and an 80×60 thumbnail, and overwrites the file as `.gx`. Save/send afterward with Orca’s normal buttons.

Supports single- and dual-extruder Flashforge printers (see profiles below). The converter does **not** configure IDEX/toolchange — use a matching Orca profile (community dual: [OrcaSlicer#9577](https://github.com/OrcaSlicer/OrcaSlicer/issues/9577)).

## Printer profiles

| ID | Printer | Mode |
|----|---------|------|
| `adventurer3` | Adventurer 3 | single |
| `adventurer4` | Adventurer 4 | single |
| `adventurer5m` | Adventurer 5M | single |
| `creator3pro` | Creator 3 Pro | dual |
| `generic_single` | Generic Flashforge | single |
| `generic_dual` | Generic Flashforge | dual |

`.gx` layout is shared: 58-byte header + 14454-byte BMP, G-code starting at offset 14512. The profile sets `multi_extruder_type` and dual/single metadata.

### Choosing a profile

Priority:

1. Flag `--printer ID` / `-p ID`
2. Environment variable `GCODE_TO_GX_PRINTER`
3. Auto-detect from G-code (two filament/nozzle values or `T1`) → `generic_dual` / `generic_single`

Examples:

```bash
gcode_to_gx --printer creator3pro /path/to/file.gcode
gcode_to_gx -p adventurer5m /path/to/file.gcode

# Windows (PowerShell)
$env:GCODE_TO_GX_PRINTER = "adventurer4"
gcode_to_gx C:\path\to\file.gcode

# macOS / Linux
export GCODE_TO_GX_PRINTER=adventurer4
gcode_to_gx /path/to/file.gcode
```

Orca passes the temporary file path as the **last** argument — flags must come before the path.

## Install from source

Requires Python 3.10+.

```bash
git clone https://github.com/HellEvro/FF_Gcode_to_GX.git
cd FF_Gcode_to_GX
python -m venv .venv
```

Activate the venv:

| OS | Command |
|----|---------|
| Windows (PowerShell) | `.\.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

```bash
pip install -e .
# or with test/build dependencies:
pip install -e ".[dev]"
```

Run without building a binary:

```bash
python -m gcode_to_gx /path/to/file.gcode
python -m gcode_to_gx --printer creator3pro /path/to/file.gcode
```

## Prebuilt binary (recommended for Orca)

| Platform | CI artifact name | Local build |
|----------|------------------|-------------|
| Windows x64 | `gcode_to_gx-windows-x64.exe` | `dist/gcode_to_gx.exe` |
| macOS arm64 | `gcode_to_gx-macos-arm64` | `dist/gcode_to_gx` |
| Linux x64 | `gcode_to_gx-linux-x64` | `dist/gcode_to_gx` |

Download from [Releases](https://github.com/HellEvro/FF_Gcode_to_GX/releases) (recommended) or from [GitHub Actions](../../actions) (workflow **Build binaries**), or build locally.

### Orca post-processing

In Orca: **Process → Others**:

1. **Filename format** — use the `.gx` extension (e.g. `*.gx`).
2. **Post-processing scripts** — path to the binary (and optionally `--printer`):

**Windows:**

```text
"%USERPROFILE%\Apps\gcode_to_gx\gcode_to_gx.exe"
```

With an explicit profile:

```text
"%USERPROFILE%\Apps\gcode_to_gx\gcode_to_gx.exe" --printer creator3pro
```

**macOS:**

```text
"/path/to/gcode_to_gx" --printer adventurer5m
```

Before the first run: `chmod +x /path/to/gcode_to_gx`. If Gatekeeper blocks it: `xattr -dr com.apple.quarantine /path/to/gcode_to_gx`.

**Linux:**

```text
"/path/to/gcode_to_gx" --printer adventurer3
```

Also: `chmod +x /path/to/gcode_to_gx`.

Quotes are required if the path contains spaces. Orca appends the temporary file path at the end of the line.

3. Slice the model and save/send as usual. A thumbnail should appear on the printer screen.

### Debug via Python (no binary)

**Windows:**

```text
"%USERPROFILE%\Apps\gcode_to_gx\.venv\Scripts\python.exe" "%USERPROFILE%\Apps\gcode_to_gx\src\gcode_to_gx\cli.py" --printer creator3pro
```

**macOS / Linux:**

```text
"/path/to/FF_Gcode_to_GX/.venv/bin/python" "/path/to/FF_Gcode_to_GX/src/gcode_to_gx/cli.py" --printer creator3pro
```

## Build a binary locally

```bash
pip install -e ".[dev]"
python scripts/build_exe.py
```

The script builds a one-file binary via PyInstaller for the **current** OS:

- Windows → `dist/gcode_to_gx.exe` (+ copy `gcode_to_gx-windows-x64.exe`)
- macOS / Linux → `dist/gcode_to_gx` (+ platform-tagged copy)

Cross-compilation from one machine to another is not supported. CI builds binaries for all OSes.

## GitHub Actions (Windows + macOS + Linux)

Workflow `.github/workflows/build-binaries.yml` builds artifacts on `windows-latest`, `macos-latest` (arm64), and `ubuntu-latest`.

```bash
gh workflow run build-binaries.yml
gh run watch
```

Artifacts: `gcode_to_gx-windows-x64.exe`, `gcode_to_gx-macos-arm64`, `gcode_to_gx-linux-x64`.

## Compare with FlashPrint

1. In FlashPrint, save a working `.gx` for your printer.
2. Place it as `tests/fixtures/flashprint_dual.gx` or nearby (reference files are gitignored).
3. Compare:

```bash
python scripts/calibrate_header.py /path/to/our.gx /path/to/flashprint_sample.gx
```

## What’s inside .gx

`58-byte header` + `BMP 80×60 (14454 bytes)` + `G-code` (G-code starts at offset 14512).

The converter does **not** insert T0/T1 — toolchange comes from the Orca profile.

## Optional: Creator 3 Pro machine G-code

Under [`profiles/creator3pro/`](profiles/creator3pro/) there are **optional** Orca machine G-code snippets for Flashforge Creator 3 Pro:

| File | Use in Orca |
|------|-------------|
| [`machine_start.gcode`](profiles/creator3pro/machine_start.gcode) | Machine start |
| [`machine_end.gcode`](profiles/creator3pro/machine_end.gcode) | Machine end (**placeholder** — owner’s end paste matched start; review / replace) |
| [`machine_pause.gcode`](profiles/creator3pro/machine_pause.gcode) | Print pause (`; pause print` + `M2000`) |

- Not official Flashforge; not endorsed by the manufacturer.
- Start and pause come from the printer owner; adapt placeholders if your Orca version differs.
- Machine G-code does **not** replace this converter: you still need the post-processing script for the `.gx` header + thumbnail.

See [`profiles/creator3pro/README.md`](profiles/creator3pro/README.md).

## Tests

```bash
pip install -e ".[dev]"
pytest
```
