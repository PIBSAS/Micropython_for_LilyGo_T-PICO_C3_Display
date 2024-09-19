# Import the ESPC3 class
from TPicoESPC3 import ESPC3
import st7789, tft_config, time
import vga1_8x16 as font

tft = tft_config.config(3)
tft.init()
tft.fill(st7789.BLACK)

# Initialize the ESP32C3 module
esp = ESPC3()  # Debug can be enabled by passing the parameter debug=True

# Get the list of access points
try:
    ap_list = esp.get_AP()
    y_position = 16  # Initial Y position
    print("Available access points:")
    tft.text(font, "Available access points:" ,0, 0, st7789.YELLOW)
    for ap in ap_list:
        print("SSID:", ap[1], "RSSI:", ap[2], "MAC:", ap[3], "Channel:", ap[4], 
              "Scan type:", ap[5], "Min scan time:", ap[6], 
              "Max scan time:", ap[7], "Pairwise cipher:", ap[8], 
              "Group cipher:", ap[9], "802.11 support:", ap[10], "WPS:", ap[11], 
              "Security:", ap[0])
    
        tft.text(font, f"SSID:{ap[1]}, RSSI:{ap[2]}, MAC:{ap[3]}, Channel:{ap[4]}, "
                       f"Scan type:{ap[5]}, Min scan time:{ap[6]}, "
                       f"Max scan time:{ap[7]}, Pairwise cipher:{ap[8]}, "
                       f"Group cipher:{ap[9]}, 802.11 support:{ap[10]}, WPS:{ap[11]}, "
                       f"Security:{ap[0]}", 
                       0, y_position, st7789.CYAN)
        
        y_position += 17  # Increment Y for the next network

except Exception as e:
    print("Error getting access points:", e)