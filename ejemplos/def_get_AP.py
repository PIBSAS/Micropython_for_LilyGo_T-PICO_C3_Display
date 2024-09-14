# Importar la clase TPicoESPC3
from TPicoESPC3 import ESPC3
import time

# Configuración de las credenciales Wi-Fi
secrets = {
    "ssid": "YOUR_WIFI",
    "password": "YOUR_CREDENTIAL"
}

# Inicializar el módulo ESP32C3
esp = ESPC3() # Se puede activar el debug ingreando el parametro debug=True

# Intentar conectar a la red Wi-Fi
try:
    esp.connect(secrets)
    print("Conectado a la red Wi-Fi:", secrets["ssid"])
except Exception as e:
    print("Error al conectar:", e)

# Obtener la lista de puntos de acceso
try:
    ap_list = esp.get_AP()
    print("Puntos de acceso disponibles:")
    for ap in ap_list:
        print("SSID:", ap[1], "RSSI:", ap[2], "MAC:", ap[3], "Canal:", ap[4], 
              "Tipo de escaneo:", ap[5], "Tiempo mínimo de escaneo:", ap[6], 
              "Tiempo máximo de escaneo:", ap[7], "Par de cifrado:", ap[8], 
              "Grupo de cifrado:", ap[9], "Soporte 802.11:", ap[10], "WPS:", ap[11], 
              "Seguridad:", ap[0])
except Exception as e:
    print("Error al obtener puntos de acceso:", e)
