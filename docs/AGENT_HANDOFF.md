# AGENT_HANDOFF — сжатая память агента

> L0. Читать этот файл (+ верх DEVLOG при нужде). Архив — только по инциденту.
> Код > docs. Секреты не писать.

**Обновлено:** 2026-09-23 · **Repo:** Gcode_to_Gx · **Local:** E:\Drive\Projects\Gcode_to_Gx

---

## 0. Протокол

До: L0 → L1 (DEVLOG ≤60 строк) → L2 профиль/код.
После: запись 3–8 строк + merge/prune; handoff ≤150 строк.

---

## 1. Суть проекта

Post-process для Orca: G-code → Flashforge `.gx` (dual header + BMP 80×60) для Creator 3 Pro. Доставка — `dist/gcode_to_gx.exe` в «Скрипты постобработки».

---

## 2. Сейчас важно

| Статус | Что |
|--------|-----|
| Done | dual-конвертер, CLI, pytest, `dist/gcode_to_gx.exe`, calibrate script |
| Open | пользователь кладёт эталон FlashPrint; проверка на Creator 3 Pro |
| Next | вписать exe в Orca post-process; сверить с FlashPrint `.gx` |

---

## 3. Жёсткие решения владельца

| Тема | Решение |
|------|---------|
| Интеграция | .exe в post-processing Orca, не native plugin |
| Режим | две головы (dual), не Copy/Mirror |
| Принтер | Flashforge Creator 3 Pro |

---

## 4. Карта

| Зона | Где |
|------|-----|
| Ядро | `src/gcode_to_gx/` |
| Сборка exe | `scripts/build_exe.py` |
| Калибровка | `scripts/calibrate_header.py` |
| Инструкция Orca | `README.md` |

---

## 5. Ловушки

- BMP должен быть ровно 14454 байт (offset G-code 14512).
- Не вставлять T0/T1 в конвертере — это профиль Orca.
- Эталон FlashPrint пользователь кладёт сам (gitignore).

---

## 6. Durable decisions

### GX dual
- multi_extruder_type=1; filament/nozzle right+left из комментариев Orca.
- In-place overwrite пути от Orca.

---

## 7. Не делать

- Не править plan-файл Cursor.
- Не force-push.
