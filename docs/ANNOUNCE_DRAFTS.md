# Черновики анонсов (вне GitHub)

Reddit из Cursor-браузера часто блокирует network security — логин вручную (Google), затем вставить.

## Уже опубликовано на GitHub

| Тема | URL |
|------|-----|
| GX Release / Show | https://github.com/HellEvro/FF_Gcode_to_GX/discussions/1 |
| Public release | https://github.com/HellEvro/FF_Gcode_to_GX/discussions/2 |
| **C3Pro machine G-code** | https://github.com/HellEvro/FF_Gcode_to_GX/discussions/3 |
| **Request: best Orca settings** | https://github.com/HellEvro/FF_Gcode_to_GX/discussions/4 |
| **Request: filament presets** | https://github.com/HellEvro/FF_Gcode_to_GX/discussions/5 |
| OrcaSlicer #9577 (GX + profiles) | https://github.com/OrcaSlicer/OrcaSlicer/issues/9577 |
| OrcaSlicer #2612 (thumbnails) | https://github.com/OrcaSlicer/OrcaSlicer/issues/2612 |

Существующая Reddit-тема про PETG (не создавать дубль):  
https://www.reddit.com/r/FlashForge/comments/tnqzom/creator_3_pro_petgproblems/

---

## Reply — r/FlashForge «Orca profile for creator 3 pro»

https://www.reddit.com/r/FlashForge/comments/1l60q6h/orca_profile_for_creator_3_pro/

```text
Sharing what we have so far for Creator 3 Pro + vanilla Orca:

1) Optional machine G-code (start / pause M2000 / end placeholder):
https://github.com/HellEvro/FF_Gcode_to_GX/tree/main/profiles/creator3pro

2) G-code → .gx post-processing converter (thumbnails on the printer UI), dual profile `creator3pro`:
https://github.com/HellEvro/FF_Gcode_to_GX/releases/tag/v0.1.0

Full tuned Orca printer/process presets are still incomplete — if you have a working export, please drop it here or in:
https://github.com/HellEvro/FF_Gcode_to_GX/discussions/4
```

## Reply — r/FlashForge «Creator 3 Pro and Orca-FlashForge»

https://www.reddit.com/r/FlashForge/comments/1q64k0a/creator_3_pro_and_orcaflashforge/

```text
Same boat — no stock Creator 3 Pro in Orca/FF-Orca. Starter machine G-code + .gx converter here:

https://github.com/HellEvro/FF_Gcode_to_GX/tree/main/profiles/creator3pro
https://github.com/HellEvro/FF_Gcode_to_GX/releases/tag/v0.1.0

Collecting better IDEX/process presets: https://github.com/HellEvro/FF_Gcode_to_GX/discussions/4
```

## New post — r/FlashForge (share settings)

**Title:** Creator 3 Pro + Orca: machine G-code snippets + .gx converter (looking for better presets)

```text
Flashforge Creator 3 Pro still has no stock profile in Orca. Sharing what we open-sourced:

• Machine start / pause (M2000) / end-placeholder G-code:
  https://github.com/HellEvro/FF_Gcode_to_GX/tree/main/profiles/creator3pro

• Orca post-processing → Flashforge .gx (header + thumbnail), dual profile included:
  https://github.com/HellEvro/FF_Gcode_to_GX/releases/tag/v0.1.0

Known gap: full printer/process/IDEX presets and a real end G-code. If you run C3/C3 Pro (or close IDEX cousin) on Orca successfully, please share exports or numbers here / in:
https://github.com/HellEvro/FF_Gcode_to_GX/discussions/4

Filament presets request (PLA/PETG/ABS/TPU/supports):
https://github.com/HellEvro/FF_Gcode_to_GX/discussions/5

(Related older PETG thread: https://www.reddit.com/r/FlashForge/comments/tnqzom/creator_3_pro_petgproblems/)
```

## New post — r/FlashForge (filament request) — optional if the share post already covers it

**Title:** Creator 3 Pro filament settings for Orca? (PLA / PETG / ABS / TPU / soluble)

```text
Looking for working filament + process numbers on Creator 3 Pro with Orca (any brand).

Especially: PLA/PLA+, PETG, ABS/ASA, TPU, and dual-extruder support materials (PVA/HIPS/…).

Please include nozzle size, layer height, temps, speed, fan, retraction, and whether you use Orca or FlashPrint.

We’re collecting replies into:
https://github.com/HellEvro/FF_Gcode_to_GX/discussions/5

Existing PETG discussion (FlashPrint-era, still useful):
https://www.reddit.com/r/FlashForge/comments/tnqzom/creator_3_pro_petgproblems/
```

---

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

## New post — r/FlashForge (converter only)

**Title:** Open-source Orca post-processing: G-code → Flashforge .gx (Adventurer / Creator 3 Pro)

```text
I open-sourced a small converter for Orca’s Post-processing scripts field: it wraps sliced G-code as Flashforge .gx (header + 80×60 thumbnail).

Profiles: Adventurer 3/4/5M, Creator 3 Pro (dual), generic single/dual.
Binaries: Windows / macOS arm64 / Linux — https://github.com/HellEvro/FF_Gcode_to_GX/releases/tag/v0.1.0
Docs: https://github.com/HellEvro/FF_Gcode_to_GX

Not a replacement for machine start/end G-code or IDEX toolchange in the Orca profile — only the .gx wrapper. Hardware feedback appreciated.
```
