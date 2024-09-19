# Import the TPicoESPC3 class
from TPicoESPC3 import ESPC3
import time

# Define the SSID and password for the Wi-Fi network
ssid = "SSID"
password = "PASSWORD"

# Initialize the ESP32C3 module
esp = ESPC3(uart_id=1, tx_pin=8, rx_pin=9, debug=True)

# Try to connect to the Wi-Fi network
try:
    connection_info = esp.join_ap(ssid, password)
    if connection_info:
        print("Connected to Wi-Fi network:", connection_info['ssid'])
        print("Connection details:")
        for key, value in connection_info.items():
            print(f"{key}: {value}")
        
        # Ping a host (for example, 8.8.8.8)
        host = "8.8.8.8"
        ping_result = esp.ping(host)
        if ping_result:
            print(f"Successful ping to {host}, response time: {ping_result} ms")
        else:
            print(f"Could not ping {host}")
except Exception as e:
    print("Error connecting or pinging:", e)
