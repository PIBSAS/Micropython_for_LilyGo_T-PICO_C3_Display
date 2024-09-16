from machine import Pin
from time import sleep

# Controlar el backlight manualmente
backlight_pin = Pin(4, Pin.OUT)
try:
    while True:
        # Apagar el backlight
        backlight_pin.value(0)
        sleep(1)
        # Encender el backlight
        backlight_pin.value(1)
        sleep(1)
except Exception as e:
    print("Enchufa la placa man!", e)