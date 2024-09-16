from machine import UART, Pin
import time

time.sleep(3)  # Espera para asegurarse de que todo esté listo

# Inicializa el UART (bus 1, TX en pin 8, RX en pin 9)
uart = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9), cts=Pin(10), rts=Pin(11))
uart.write('ATE0\r\n')  # Desactiva el eco en el ESP

led = Pin(25, Pin.OUT)  # LED en la placa

# Comandos AT que se enviarán
comandos_at = [
    'AT',             # Comando para verificar la comunicación
    'AT+GMR',        # Obtener la versión del firmware
    'AT+CWMODE?',    # Obtener el modo de operación
    'AT+CWJAP="SSID","PASSWORD"'  # Conectar a Wi-Fi (reemplaza con tus credenciales)
]

while True:
    for cmd in comandos_at:
        try:
            led.toggle()  # Cambia el estado del LED
            uart.write(cmd + '\r\n')  # Envía el comando AT
            print("Enviando:", cmd)

            # Espera la respuesta
            time.sleep(1)  # Espera un momento para permitir que el ESP responda
            while uart.any() == 0:
                time.sleep_ms(100)  # Espera por datos

            response = uart.read()  # Lee la respuesta
            print("Respuesta del ESP:", response)  # Imprime la respuesta

            time.sleep(2)  # Espera un poco antes de enviar el siguiente comando
        except Exception as e:
            print("Error:", e)
    time.sleep(5)  # Espera antes de repetir los comandos
