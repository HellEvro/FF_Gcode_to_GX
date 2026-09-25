; =============================================================================
; PLACEHOLDER — machine end G-code for Creator 3 Pro
; The owner’s paste for “end” matched start; real end G-code still needed.
; Replace this file with your working FlashPrint/Orca end snippet when available.
; =============================================================================
M104 S0 ; nozzle off
M140 S0 ; bed off
G91
G1 Z10 F600 ; raise a bit (relative)
G90
G28 X Y ; home X/Y (present / park — tune for your firmware)
M84 ; disable steppers
