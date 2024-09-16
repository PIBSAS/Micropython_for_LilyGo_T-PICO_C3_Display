# Importar la clase TPicoESPC3
from TPicoESPC3 import ESPC3
from tft_config import config
import st7789
import vga1_8x16 as font
import time

tft = config(3)
tft.init()
# Inicializar el módulo ESP32C3
esp = ESPC3()

# Configuración de las credenciales Wi-Fi
secrets = {
    "ssid": "TELWINET:9E-5E_EXT",
    "password": "68297640"
}

# Intentar conectar a la red Wi-Fi
try:
    esp.connect(secrets)
    print("Conectado a la red Wi-Fi:", secrets["ssid"])
    tft.text(font, "Conectado a la red Wi-fi:", 0, 0)
    tft.text(font, f"{secrets["ssid"]}", 0, 20)
    ip_address = esp.get_ip()
    if ip_address:
        tft.text(font, f"IP Address: {ip_address}", 0, 40)
        print(f"IP Address: {ip_address}")
    else:
        print("No IP Address")
        tft.text(font, "No IP Address", 0, 100)
except Exception as e:
    print("Error al conectar:", e)
    tft.text(font, f"Error al conectarse a la red Wi-Fi: {e}", 0, 120, st7789.RED)