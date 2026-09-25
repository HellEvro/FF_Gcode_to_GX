; =============================================================================
; OPTIONAL template — Flashforge Creator 3 Pro TOOL CHANGE (dual)
; NOT official Flashforge. Adapt before use. See gcode/creator3pro/README.md
;
; Paste into Orca "Change filament" / tool-change custom G-code (wording varies
; by version). Creator 3 Pro community profiles often use M108 Tx rather than
; only a bare T command — keep whichever your firmware accepts.
;
; Orca placeholders (verify names for your version):
;   {previous_extruder}  {next_extruder}
;   {nozzle_temperature[next_extruder]}  etc.
; =============================================================================

; Retract on current tool (relative E — ensure M83 if your profile uses relative)
; G1 E-1 F1800

; Cool / idle previous tool (optional — reduces oozing; may slow dual prints)
; M104 S{standby_temperature_delta} T{previous_extruder}

; Heat next tool — order must be S then T on many Flashforge firmwares
; M104 S{nozzle_temperature[next_extruder]} T{next_extruder}
; M6 T{next_extruder}

; Flashforge-style tool select (preferred in community Creator 3 Pro Cura profiles)
M108 T{next_extruder}

; Fallback if M108 is ignored on your firmware:
; T{next_extruder}

G92 E0

; Optional wipe / purge tower is normally handled by the slicer — do not duplicate
; large prime moves here unless you know your wipe tower is disabled.
