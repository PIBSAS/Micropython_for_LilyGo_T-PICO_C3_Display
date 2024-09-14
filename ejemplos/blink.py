from machine import Pin
import time

# Definir el pin del LED integrado
LED_BUILTIN = 25
led = Pin(LED_BUILTIN, Pin.OUT)

# Configuración inicial (setup)
def setup():
    led.value(0)  # Inicializa el LED apagado

# Bucle principal (loop)
def loop():
    while True:
        led.value(1)  # Enciende el LED
        time.sleep(1)  # Espera 1 segundo
        led.value(0)  # Apaga el LED
        time.sleep(1)  # Espera 1 segundo

# Ejecución
setup()
loop()
