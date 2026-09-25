M118 X150 Y125 Z200 T[initial_extruder] ; Границы печати Flashforge
M140 S[bed_temperature_initial_layer_single] ; Нагрев стола

G90 ; Абсолютные координаты осей
M82 ; Абсолютные координаты экструдера

G28 ; Автохоуминг
G1 Z15 F1200 ; Опускаем стол

M190 S[bed_temperature_initial_layer_single] ; Ожидание нагрева стола

T[initial_extruder]
M104 S[nozzle_temperature_initial_layer] T[initial_extruder]
M109 S[nozzle_temperature_initial_layer] T[initial_extruder]

G92 E0 ; Сброс экструдера
