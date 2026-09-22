# G-code → GX для Orca Slicer (Flashforge Creator 3 Pro)

Конвертер для поля **«Скрипты постобработки»** в Orca: берёт временный файл после нарезки, вшивает dual-шапку Flashforge и эскиз 80×60, перезаписывает файл как `.gx`. Дальше сохранение/отправка — **штатными кнопками Orca**.

## Быстрый старт (готовый .exe)

1. Соберите exe (нужен Python один раз у того, кто собирает):

```powershell
cd E:\Drive\Projects\Gcode_to_Gx
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python scripts/build_exe.py
```

2. В Orca: **Процесс → Прочее**:
   - **Формат имени файла** — с расширением `.gx` (у вас уже так).
   - **Скрипты постобработки** — одна строка:

```text
"E:\Drive\Projects\Gcode_to_Gx\dist\gcode_to_gx.exe"
```

Кавычки обязательны, если в пути есть пробелы.

3. Нарежьте модель с **двумя филаментами** и сохраните/отправьте как обычно.

На экране Creator 3 Pro должен появиться эскиз.

## Без сборки exe (для отладки)

```powershell
pip install -e .
python -m gcode_to_gx "C:\path\to\file.gcode"
```

В постобработку Orca можно временно вписать:

```text
"C:\Path\To\python.exe" "E:\Drive\Projects\Gcode_to_Gx\src\gcode_to_gx\cli.py"
```

## Сверка с FlashPrint

1. В FlashPrint сохраните рабочий двухголовый `.gx` для Creator 3 Pro.
2. Положите его в `tests/fixtures/flashprint_dual.gx`.
3. Сконвертируйте тестовый/свой файл и сравните:

```powershell
python scripts/calibrate_header.py путь\к\наш.gx tests/fixtures/flashprint_dual.gx
```

## Профиль принтера

Конвертер **не** настраивает IDEX/toolchange. Нужен dual-профиль Orca под Creator 3 Pro (community: [OrcaSlicer#9577](https://github.com/OrcaSlicer/OrcaSlicer/issues/9577)).

## Что внутри .gx

`шапка 58 байт` + `BMP 80×60 (14454 байт)` + `G-code` (старт G-code с offset 14512).

## Тесты

```powershell
pip install -e ".[dev]"
pytest
```
