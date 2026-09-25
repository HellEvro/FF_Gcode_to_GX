# DEVLOG

Краткий журнал. Новые записи — сверху. Длинные разборы — в ARCHIVE.

## 2026-09-25

- Discussions: **#3** share C3Pro machine G-code; **#4** request best Orca presets; **#5** request filament presets (PETG Reddit: `/tnqzom`).
- Update comment на OrcaSlicer #9577 со ссылками на #3–#5.
- `docs/ANNOUNCE_DRAFTS.md` — Reddit replies/new posts (C3Pro + GX); Cursor-browser всё ещё blocked.

- **Public** https://github.com/HellEvro/FF_Gcode_to_GX + topics; Release **v0.1.0** (win/mac/linux binaries).
- Анонсы: OrcaSlicer [#9577](https://github.com/OrcaSlicer/OrcaSlicer/issues/9577#issuecomment-5838692298), [#2612](https://github.com/OrcaSlicer/OrcaSlicer/issues/2612#issuecomment-5838692555); Discussions #1/#2.
- Reddit (r/FlashForge Guider2, r/OrcaSlicer AD4 thumbnails, newbie GX Q) — login blocked; черновики `docs/ANNOUNCE_DRAFTS.md`.
- README: ссылка на Releases.

- Docs: `README.md` (EN) + `README.ru.md` (RU), language switch; generic paths.
- Опц. Orca G-code владельца: `profiles/creator3pro/` (start, pause `M2000`, end-заглушка; удалён выдуманный `gcode/`).
- Профили принтеров (`adventurer3/4/5m`, `creator3pro`, `generic_single/dual`); CLI `--printer` / env `GCODE_TO_GX_PRINTER`; auto-detect.
- CI `build-binaries.yml` (win / macos-arm64 / linux); 11 pytest OK; Windows exe локально.
- Git: `origin` HellEvro/FF_Gcode_to_GX; `gh` через Cursor env-PAT ограничен — API через git-credential.

## 2026-09-23

- v1: dual G-code→GX, CLI, 5 pytest OK, PyInstaller `dist/gcode_to_gx.exe` (smoke OK).
- Калибровка: `scripts/calibrate_header.py`; эталон FlashPrint — от пользователя.
- Orca: путь exe в «Скрипты постобработки», имя файла `*.gx`.
