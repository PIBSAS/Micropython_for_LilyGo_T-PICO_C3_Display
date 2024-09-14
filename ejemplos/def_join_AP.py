# Importar la clase TPicoESPC3
from TPicoESPC3 import ESPC3
import time

# Definir el SSID y la contraseña de la red Wi-Fi
ssid = "YOUR_WIFI"
password = "YOUR_CREDENTIAL"

# Inicializar el módulo ESP32C3
esp = ESPC3(debug=True)

# Ejemplo de uso
try:
    connection_info = esp.join_ap(ssid, password)
    if connection_info:
        print("Conectado a la red Wi-Fi:", connection_info['ssid'])
        print("Detalles de la conexión:")
        for key, value in connection_info.items():
            print(f"{key}: {value}")
except Exception as e:
    print("Error al conectarse a la red Wi-Fi:", e)
