# DEVLOG

Краткий журнал. Новые записи — сверху. Длинные разборы — в ARCHIVE.

## 2026-09-25

- Docs: `README.md` (EN) + `README.ru.md` (RU), language switch; generic paths.
- Опц. шаблоны machine G-code: `gcode/creator3pro/` (start/end/toolchange; community-inspired, не official FF).
- Профили принтеров (`adventurer3/4/5m`, `creator3pro`, `generic_single/dual`); CLI `--printer` / env `GCODE_TO_GX_PRINTER`; auto-detect.
- CI `build-binaries.yml` (win / macos-arm64 / linux); 11 pytest OK; Windows exe локально.

- Private GitHub: https://github.com/HellEvro/FF_Gcode_to_GX (`origin` → push `main` OK).
- `gh repo create` через Cursor `GITHUB_TOKEN` дал 403; репо создан API с git-credential токеном HellEvro.

## 2026-09-23

- v1: dual G-code→GX, CLI, 5 pytest OK, PyInstaller `dist/gcode_to_gx.exe` (smoke OK).
- Калибровка: `scripts/calibrate_header.py`; эталон FlashPrint — от пользователя.
- Orca: путь exe в «Скрипты постобработки», имя файла `*.gx`.
