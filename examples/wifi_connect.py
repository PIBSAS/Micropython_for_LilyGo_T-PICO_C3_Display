# Import the ESPC3 class
from TPicoESPC3 import ESPC3
from tft_config import config
import st7789
import vga1_8x16 as font
import time

tft = config(3)
tft.init()
# Wi-Fi credentials configuration
esp = ESPC3()

# Wi-Fi credentials configuration
secrets = {
    "ssid": "YOUR_WIFI",
    "password": "YOUR_PASSWORD"
}

# Try to connect to the Wi-Fi network
try:
    esp.connect(secrets)
    print("Connected to Wi-Fi network:", secrets["ssid"])
    tft.text(font, "Connected to Wi-Fi network:", 0, 0)
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
    tft.text(font, f"Error connecting to Wi-Fi: {e}", 0, 120, st7789.RED)