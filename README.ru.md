# G-code → GX для Orca Slicer (Flashforge)

[English](README.md)

Конвертер для поля **«Скрипты постобработки»** в Orca: берёт временный файл после нарезки, вшивает шапку Flashforge и эскиз 80×60, перезаписывает файл как `.gx`. Дальше сохранение/отправка — штатными кнопками Orca.

Поддерживаются одно- и двухголовые Flashforge (см. профили ниже). Конвертер **не** настраивает IDEX/toolchange — нужен подходящий профиль Orca (community dual: [OrcaSlicer#9577](https://github.com/SoftFever/OrcaSlicer/issues/9577)).

## Профили принтеров

| ID | Принтер | Режим |
|----|---------|--------|
| `adventurer3` | Adventurer 3 | single |
| `adventurer4` | Adventurer 4 | single |
| `adventurer5m` | Adventurer 5M | single |
| `creator3pro` | Creator 3 Pro | dual |
| `generic_single` | Generic Flashforge | single |
| `generic_dual` | Generic Flashforge | dual |

Разметка `.gx` общая: шапка 58 байт + BMP 14454 байт, G-code с offset 14512. Профиль задаёт `multi_extruder_type` и dual/single metadata.

### Выбор профиля

Приоритет:

1. Флаг `--printer ID` / `-p ID`
2. Переменная окружения `GCODE_TO_GX_PRINTER`
3. Auto-detect по G-code (два значения filament/nozzle или `T1`) → `generic_dual` / `generic_single`

Примеры:

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

Orca передаёт путь к временному файлу **последним** аргументом — флаги должны стоять до пути.

## Установка из исходников

Нужен Python 3.10+.

```bash
git clone https://github.com/HellEvro/FF_Gcode_to_GX.git
cd FF_Gcode_to_GX
python -m venv .venv
```

Активация venv:

| ОС | Команда |
|----|---------|
| Windows (PowerShell) | `.\.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

```bash
pip install -e .
# или с тестовыми/сборочными зависимостями:
pip install -e ".[dev]"
```

Запуск без сборки бинарника:

```bash
python -m gcode_to_gx /path/to/file.gcode
python -m gcode_to_gx --printer creator3pro /path/to/file.gcode
```

## Готовый бинарник (рекомендуется для Orca)

| Платформа | Имя артефакта (CI) | Локальная сборка |
|-----------|--------------------|------------------|
| Windows x64 | `gcode_to_gx-windows-x64.exe` | `dist/gcode_to_gx.exe` |
| macOS arm64 | `gcode_to_gx-macos-arm64` | `dist/gcode_to_gx` |
| Linux x64 | `gcode_to_gx-linux-x64` | `dist/gcode_to_gx` |

Скачайте с [Releases](https://github.com/HellEvro/FF_Gcode_to_GX/releases) (предпочтительно) или из [GitHub Actions](../../actions) (workflow **Build binaries**), либо соберите локально.

### Orca: постобработка

В Orca: **Процесс → Прочее**:

1. **Формат имени файла** — с расширением `.gx` (например `*.gx`).
2. **Скрипты постобработки** — путь к бинарнику (и опционально `--printer`):

**Windows:**

```text
"%USERPROFILE%\Apps\gcode_to_gx\gcode_to_gx.exe"
```

С явным профилем:

```text
"%USERPROFILE%\Apps\gcode_to_gx\gcode_to_gx.exe" --printer creator3pro
```

**macOS:**

```text
"/path/to/gcode_to_gx" --printer adventurer5m
```

Перед первым запуском: `chmod +x /path/to/gcode_to_gx`. Если Gatekeeper блокирует: `xattr -dr com.apple.quarantine /path/to/gcode_to_gx`.

**Linux:**

```text
"/path/to/gcode_to_gx" --printer adventurer3
```

Также: `chmod +x /path/to/gcode_to_gx`.

Кавычки обязательны, если в пути есть пробелы. Orca допишет путь к временному файлу в конец строки.

3. Нарежьте модель и сохраните/отправьте как обычно. На экране принтера должен появиться эскиз.

### Отладка через Python (без бинарника)

**Windows:**

```text
"%USERPROFILE%\Apps\gcode_to_gx\.venv\Scripts\python.exe" "%USERPROFILE%\Apps\gcode_to_gx\src\gcode_to_gx\cli.py" --printer creator3pro
```

**macOS / Linux:**

```text
"/path/to/FF_Gcode_to_GX/.venv/bin/python" "/path/to/FF_Gcode_to_GX/src/gcode_to_gx/cli.py" --printer creator3pro
```

## Сборка бинарника локально

```bash
pip install -e ".[dev]"
python scripts/build_exe.py
```

Скрипт собирает one-file через PyInstaller для **текущей** ОС:

- Windows → `dist/gcode_to_gx.exe` (+ копия `gcode_to_gx-windows-x64.exe`)
- macOS / Linux → `dist/gcode_to_gx` (+ копия с тегом платформы)

Кросс-сборка с одной машины на другую не поддерживается. Бинарники для всех ОС собирает CI.

## GitHub Actions (Windows + macOS + Linux)

Workflow `.github/workflows/build-binaries.yml` собирает артефакты на `windows-latest`, `macos-latest` (arm64), `ubuntu-latest`.

```bash
gh workflow run build-binaries.yml
gh run watch
```

Артефакты: `gcode_to_gx-windows-x64.exe`, `gcode_to_gx-macos-arm64`, `gcode_to_gx-linux-x64`.

## Сверка с FlashPrint

1. В FlashPrint сохраните рабочий `.gx` для вашего принтера.
2. Положите его как `tests/fixtures/flashprint_dual.gx` или рядом (эталон в gitignore).
3. Сравните:

```bash
python scripts/calibrate_header.py /path/to/our.gx /path/to/flashprint_sample.gx
```

## Что внутри .gx

`шапка 58 байт` + `BMP 80×60 (14454 байт)` + `G-code` (старт G-code с offset 14512).

Конвертер **не** вставляет T0/T1 — toolchange задаётся профилем Orca.

## Опционально: machine G-code для Creator 3 Pro

В [`profiles/creator3pro/`](profiles/creator3pro/) — **опциональные** сниппеты machine G-code Orca для Flashforge Creator 3 Pro:

| Файл | Поле в Orca |
|------|-------------|
| [`machine_start.gcode`](profiles/creator3pro/machine_start.gcode) | Стартовый G-код |
| [`machine_end.gcode`](profiles/creator3pro/machine_end.gcode) | Завершающий G-код (**заглушка** — вставка «end» совпала со start; проверьте / замените) |
| [`machine_pause.gcode`](profiles/creator3pro/machine_pause.gcode) | G-код паузы печати (`; pause print` + `M2000`) |

- Не официальные материалы Flashforge; без endorsement производителя.
- Start и pause — от владельца принтера; при другой версии Orca проверьте плейсхолдеры.
- Machine G-code **не** заменяет конвертер: post-processing script для шапки `.gx` + эскиза всё равно нужен.

См. [`profiles/creator3pro/README.md`](profiles/creator3pro/README.md).

## Тесты

```bash
pip install -e ".[dev]"
pytest
```
