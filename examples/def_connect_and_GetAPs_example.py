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
    print("Connected to the Wi-Fi network:", secrets["ssid"])
except Exception as e:
    print("Error connecting:", e)

# Get the list of access points
try:
    ap_list = esp.get_AP()
    print("Available access points:")
    for ap in ap_list:
        print("SSID:", ap[1], "RSSI:", ap[2], "MAC:", ap[3], "Channel:", ap[4], 
              "Scan type:", ap[5], "Minimum scan time:", ap[6], 
              "Maximum scan time:", ap[7], "Encryption pair:", ap[8], 
              "Encryption group:", ap[9], "802.11 support:", ap[10], "WPS:", ap[11], 
              "Security:", ap[0])
except Exception as e:
    print("Error obtaining access points:", e)
