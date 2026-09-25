; =============================================================================
; OPTIONAL template — Flashforge Creator 3 Pro END
; NOT official Flashforge. Adapt before use. See gcode/creator3pro/README.md
; =============================================================================

M104 S0 T1 ; cool left
M104 S0 T0 ; cool right
M140 S0    ; bed off (some firmwares want M140 S0 T0)

; Park / lower bed. G162 is Flashforge-style; use G28 / G1 Zmax if needed.
G162 Z
M652 ; chassis fan off (Flashforge-specific; remove if unsupported)

G92 E0
G1 F1600 Y-125 Z200 ; park — tune Y/Z for your machine
M18                 ; disable steppers (or M84)
