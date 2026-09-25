# Черновики анонсов (вне GitHub)

Reddit из агента недоступен (network security на login). Вставить вручную.

## Reply — r/FlashForge «orca with guider 2»

https://www.reddit.com/r/FlashForge/comments/1r1zjbm/orca_with_guider_2/

```text
Open-source Orca post-processing converter for exactly that: G-code → Flashforge .gx (header + thumbnail BMP).

https://github.com/HellEvro/FF_Gcode_to_GX/releases/tag/v0.1.0

In Orca: set filename to *.gx, put the binary path in Post-processing scripts. Guider 2 should use a single-extruder profile (adventurer* / generic_single) — please report back if the screen thumbnail/ETA look wrong.
```

## Reply — r/OrcaSlicer «Thumbnails on FlashForge Adventurer4»

https://www.reddit.com/r/OrcaSlicer/comments/1qsbm9q/thumbnails_on_flashforge_adventurer4_printer/

```text
Thumbnails on Flashforge need a real .gx (binary header + 80×60 BMP), not PNG comments in plain G-code.

Another Orca post-processing option (Adventurer 4 profile included, Win/macOS/Linux binaries):

https://github.com/HellEvro/FF_Gcode_to_GX/releases/tag/v0.1.0

Process → Others → filename *.gx + path to the exe. Feedback welcome if AD4 still misbehaves after conversion.
```

## Reply — r/FlashForge newbie thread (GX question)

https://www.reddit.com/r/FlashForge/comments/1hntchf/information_for_newbies/

```text
Re: how files become .gx — Orca does not emit Flashforge .gx natively. Use a post-processing converter, e.g.:

https://github.com/HellEvro/FF_Gcode_to_GX

Set output filename to *.gx and point Post-processing scripts at the binary from Releases.
```

## New post — r/FlashForge (optional)

**Title:** Open-source Orca post-processing: G-code → Flashforge .gx (Adventurer / Creator 3 Pro)

```text
I open-sourced a small converter for Orca’s Post-processing scripts field: it wraps sliced G-code as Flashforge .gx (header + 80×60 thumbnail).

Profiles: Adventurer 3/4/5M, Creator 3 Pro (dual), generic single/dual.
Binaries: Windows / macOS arm64 / Linux — https://github.com/HellEvro/FF_Gcode_to_GX/releases/tag/v0.1.0
Docs: https://github.com/HellEvro/FF_Gcode_to_GX

Not a replacement for machine start/end G-code or IDEX toolchange in the Orca profile — only the .gx wrapper. Hardware feedback appreciated.
```
