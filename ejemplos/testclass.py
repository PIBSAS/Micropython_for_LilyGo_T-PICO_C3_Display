# Importar la clase TPicoESPC3
from TPicoESPC3 import ESPC3
import time

# Configuración de las credenciales Wi-Fi
secrets = {
    "ssid": "TELWINET:9E-5E_EXT",
    "password": "68297640"
}

# Inicializar el módulo ESP32C3
esp = ESPC3(uart_id=1, tx_pin=8, rx_pin=9, debug=True)

# Intentar conectar a la red Wi-Fi
try:
    esp.connect(secrets)
    print("Conectado a la red Wi-Fi:", secrets["ssid"])
except Exception as e:
    print("Error al conectar:", e)

# Realizar un ping a un host
try:
    tiempo_ping = esp.ping("google.com")
    print("Tiempo de ping:", tiempo_ping, "ms")
except Exception as e:
    print("Error al hacer ping:", e)

# Obtener la dirección IP local
try:
    ip_local = esp.local_ip
    print("Dirección IP local:", ip_local)
except Exception as e:
    print("Error al obtener la IP local:", e)
