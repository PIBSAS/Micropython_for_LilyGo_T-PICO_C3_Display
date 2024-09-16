# main.py
from machine import Pin
import time
from tft_buttons import Buttons
from OneButton import OneButton  # Importar la clase OneButton

# Crear instancia de Buttons
buttons = Buttons()

# Crear instancias de OneButton para cada botón
button1 = OneButton(buttons.left)  # Botón izquierdo
button2 = OneButton(buttons.right)  # Botón derecho

# Establecer tiempo de inactividad
#button1.setIdleMs(5000)  # Establece 1 segundo de inactividad

# Funciones callback

def on_click():
    print("Callback: Button clicked")
    button1._last_action_time = time.ticks_ms()  # Actualiza tiempo de la última acción

def on_double_click():
    print("Callback: Button double clicked")
    button1._last_action_time = time.ticks_ms()  # Actualiza tiempo de la última acción

def on_multiple_click(click_count):
    print(f"Callback: Button multiple clicked {click_count} times")
    button1._last_action_time = time.ticks_ms()  # Actualiza tiempo de la última acción

def on_long_press_start():
    print("Callback: Long press started")
    button1._last_action_time = time.ticks_ms()  # Actualiza tiempo de la última acción

def on_long_press_stop():
    print("Callback: Long press stopped")
    button1._last_action_time = time.ticks_ms()  # Actualiza tiempo de la última acción

def on_idle():
    print("Callback: Button is idle")

# Asignar funciones callback
#button1.attachPress(on_press)
button1.attachClick(on_click)
button1.attachDoubleClick(on_double_click)
button1.attachMultiClick(on_multiple_click)
button1.attachLongPressStart(on_long_press_start)
button1.attachLongPressStop(on_long_press_stop)
#button1.attachIdle(on_idle)  # Asigna la función de inactividad

# Bucle principal
while True:
    button1.tick()  # Verificar el estado del botón
    button2.tick()  # Verificar el estado del botón
    time.sleep_ms(1)  # Pausa breve para no sobrecargar el CPU