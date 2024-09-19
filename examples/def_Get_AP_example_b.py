# Import the TPicoESPC3 class
from TPicoESPC3 import ESPC3
import time

# Wi-Fi credentials configuration
secrets = {
    "ssid": "SSID",
    "password": "PASSWORD"
}

# Initialize the ESP32C3 module
esp = ESPC3()

# Try to connect to the Wi-Fi network
try:
    esp.connect(secrets)
    print("Connected to Wi-Fi network:", secrets["ssid"])
except Exception as e:
    print("Error connecting:", e)

# Get the list of access points
try:
    ap_list = esp.get_AP()
    print("Available access points:")
    labels = ["Security", "SSID", "RSSI", "MAC", "Channel", 
              "Scan type", "Minimum scan time", 
              "Maximum scan time", "Encryption pair", 
              "Encryption group", "802.11 support", "WPS"]
    
    for ap in ap_list:
        for i, label in enumerate(labels):
            print(f"{label}:\n{ap[i]}\n")
except Exception as e:
    print("Error obtaining access points:", e)
