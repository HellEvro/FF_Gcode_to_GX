# AGENT_HANDOFF — сжатая память агента

> L0. Читать этот файл (+ верх DEVLOG при нужде). Архив — только по инциденту.
> Код > docs. Секреты не писать.

**Обновлено:** 2026-09-25 · **Repo:** https://github.com/HellEvro/FF_Gcode_to_GX (private)

---

## 0. Протокол

До: L0 → L1 (DEVLOG ≤60 строк) → L2 профиль/код.
После: запись 3–8 строк + merge/prune; handoff ≤150 строк.

---

## 1. Суть проекта

Post-process для Orca: G-code → Flashforge `.gx` (шапка + BMP 80×60). Профили single/dual под Adventurer / Creator 3 Pro. Доставка — бинарник в «Скрипты постобработки».

---

## 2. Сейчас важно

| Статус | Что |
|--------|-----|
| Done | профили `src/gcode_to_gx/printers/`; CLI `--printer` / `GCODE_TO_GX_PRINTER`; auto-detect |
| Done | README EN + `README.ru.md` (language switch); CI `build-binaries.yml` |
| Done | опц. шаблоны `gcode/creator3pro/` (start/end/toolchange; не official FF) |
| Done | local Windows `dist/gcode_to_gx.exe`; Mac/Linux — через CI (`macos-arm64`) |
| Open | проверка на железе; эталон FlashPrint |
| Note | Cursor `GITHUB_TOKEN` без createRepo; push через git-credential |

---

## 3. Жёсткие решения владельца

| Тема | Решение |
|------|---------|
| Интеграция | бинарник в post-processing Orca |
| Принтеры | adventurer3/4/5m, creator3pro, generic_single/dual |
| Layout GX | общий (58 + 14454, offset 14512) |
| Docs | EN primary `README.md`, RU `README.ru.md`; generic paths only |

---

## 4. Карта

| Зона | Где |
|------|-----|
| Ядро | `src/gcode_to_gx/` |
| Профили | `src/gcode_to_gx/printers/` |
| Опц. G-code | `gcode/creator3pro/` |
| Сборка | `scripts/build_exe.py` |
| CI | `.github/workflows/build-binaries.yml` |
| Калибровка | `scripts/calibrate_header.py` |

---

## 5. Ловушки

- BMP ровно 14454 байт (offset G-code 14512).
- Не вставлять T0/T1 в конвертере — профиль Orca.
- Orca путь — последний argv; флаги до пути.
- PyInstaller не кросс-компилирует; Mac/Linux из CI.
- Machine G-code ≠ `.gx` header; шаблоны C3Pro — optional, adapt firmware.

---

## 6. Durable decisions

### GX + профили
- dual: `multi_extruder_type=1`; single: `0`, left filament/nozzle = 0.
- Default без флага/env: auto → `generic_dual` / `generic_single`.
- In-place overwrite пути от Orca.

---

## 7. Не делать

- Не править plan-файл Cursor.
- Не force-push.
- Не писать личные пути в README.
