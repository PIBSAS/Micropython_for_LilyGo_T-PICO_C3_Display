# Import the TPicoESPC3 class
from TPicoESPC3 import ESPC3

# Define the SSID and password for the Wi-Fi network
ssid = "WIFI"
password = "PASSWORD"

# Initialize the ESP32C3 module
esp = ESPC3()

# Example usage
try:
    connection_info = esp.join_ap(ssid, password)
    if connection_info:
        print("Connected to Wi-Fi network:", connection_info['ssid'])
        print("Connection details:")
        for key, value in connection_info.items():
            print(f"{key}: {value}")
except Exception as e:
    print("Error connecting to the Wi-Fi network:", e)
