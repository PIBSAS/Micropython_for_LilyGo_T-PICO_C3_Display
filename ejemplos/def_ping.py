# Importar la clase TPicoESPC3
from TPicoESPC3 import ESPC3
import time

# Definir el SSID y la contraseña de la red Wi-Fi
ssid = "YOUR_WIFI"
password = "YOUR_CREDENTIAL"

# Inicializar el módulo ESP32C3
esp = ESPC3(uart_id=1, tx_pin=8, rx_pin=9, debug=True)

# Intentar conectarse a la red Wi-Fi
try:
    connection_info = esp.join_ap(ssid, password)
    if connection_info:
        print("Conectado a la red Wi-Fi:", connection_info['ssid'])
        print("Detalles de la conexión:")
        for key, value in connection_info.items():
            print(f"{key}: {value}")
        
        # Realizar un ping a un host (por ejemplo, 8.8.8.8)
        host = "8.8.8.8"
        ping_result = esp.ping(host)
        if ping_result:
            print(f"Ping exitoso a {host}, tiempo de respuesta: {ping_result} ms")
        else:
            print(f"No se pudo hacer ping a {host}")
except Exception as e:
    print("Error al conectarse o hacer ping:", e)
