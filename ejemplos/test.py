from machine import UART, Pin
import time

time.sleep(3)  # Espera para asegurarse de que todo esté listo

# Inicializa el UART (bus 1, TX en pin 8, RX en pin 9)
uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9), cts=Pin(10), rts=Pin(11))
uart.write('ATE0\r\n')  # Desactiva el eco en el ESP

led = Pin(25, Pin.OUT)  # LED en la placa

while True:
    try:
        led.toggle()  # Cambia el estado del LED
        uart.write('TEST\r\n')  # Envía un mensaje de prueba
        print("uart OK")
    except Exception as e:
        print("Error:", e)
    time.sleep(1)
