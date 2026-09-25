; =============================================================================
; OPTIONAL template — Flashforge Creator 3 Pro (dual / IDEX-oriented) START
; NOT official Flashforge. Adapt before use. See gcode/creator3pro/README.md
; Community-inspired (Cura Creator 3 Pro profiles). Placeholders are Orca-style.
; =============================================================================

; Build envelope + dual tools (T0 T1). Adjust X/Y/Z to your printable volume.
M118 X120 Y120 Z200 T0 T1

M107 ; part fans off during heat-up
G90  ; absolute positioning

; Raise Z slightly before waiting on heaters (safe clearance — tune as needed)
G1 Z0.5 F840

; Wait for bed / nozzles. Flashforge often uses M7 (bed) and M6 (hotend) + T index.
; If your firmware ignores these, use M190 / M109 with S… T… order instead.
M7 T0
M6 T0
M6 T1

; --- Temperatures (set before wait if your firmware needs explicit M104/M140) ---
; Prefer S then T: M104 S{temp} T{tool}
; Uncomment and adjust placeholders for your Orca version:
; M140 S{bed_temperature_initial_layer[0]}
; M104 S{nozzle_temperature_initial_layer[0]} T0
; M104 S{nozzle_temperature_initial_layer[1]} T1

; Select right tool (T0), prime line on +X side
M108 T0
G92 E0
G1 X145 Y120 Z0.2 F1200
G1 X145 Y-120 E7.982
G1 X144 Y-120 E8.016
G1 X144 Y120 E15.998
G1 X144 Y123 E5.998 F2000
G1 Z0.5
G92 E0

; Select left tool (T1), prime line on -X side
M108 T1
G92 E0
G1 X-145 Y120 Z0.2 F1200
G1 X-145 Y-120 E7.982
G1 X-144 Y-120 E8.016
G1 X-144 Y120 E15.998
G1 X-144 Y123 E5.998 F2000
G1 Z0.5
G92 E0

; Chassis fan (Flashforge-specific; remove if unsupported)
M651

; Optional part-cooling — set per tool if needed:
; M106 S{fan_percentage} T0
; M106 S{fan_percentage} T1

; Leave active tool as required by the first extruder in the sliced object:
; M108 T{initial_extruder}
