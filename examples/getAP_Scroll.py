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
    screen_width = 240  # Screen width
    fixed_time = 1  # Fixed time to display the text without scrolling
    scroll_speed = 5  # Scrolling speed in pixels
    
    print("Available access points:")
    tft.text(font, "Available access points:", 0, 0, st7789.YELLOW)
    
    for ap in ap_list:
        print("SSID:", ap[1], "RSSI:", ap[2], "MAC:", ap[3], "Channel:", ap[4], 
              "Scan type:", ap[5], "Min scan time:", ap[6], 
              "Max scan time:", ap[7], "Pairwise cipher:", ap[8], 
              "Group cipher:", ap[9], "802.11 support:", ap[10], "WPS:", ap[11], 
              "Security:", ap[0])
        
        text = (f"SSID:{ap[1]}, RSSI:{ap[2]}, MAC:{ap[3]}, Channel:{ap[4]}, "
                f"Scan type:{ap[5]}, Min scan time:{ap[6]}, "
                f"Max scan time:{ap[7]}, Pairwise cipher:{ap[8]}, "
                f"Group cipher:{ap[9]}, 802.11 support:{ap[10]}, WPS:{ap[11]}, "
                f"Security:{ap[0]}")
        
        # Display the text statically for 2 seconds
        tft.text(font, text, 0, y_position, st7789.CYAN)
        time.sleep(fixed_time)
        
        # Get the width of the text in pixels (using 8x16 font)
        text_width = len(text) * 8
        
        # If the text is wider than the screen, scroll it
        if text_width > screen_width:
            for scroll in range(0, text_width - screen_width + 1, scroll_speed):
                tft.fill_rect(-1, y_position, screen_width, 17, st7789.BLACK)  # Clear the previous line
                tft.text(font, text, -scroll, y_position, st7789.CYAN)  # Draw the scrolled text
                time.sleep(0.05)  # Adjust the scrolling speed
            
            # Return to the initial position and display the complete text without scrolling for 2 seconds
            tft.fill_rect(0, y_position, screen_width, 16, st7789.BLACK)  # Clear the line
            tft.text(font, text, 0, y_position, st7789.CYAN)  # Display the complete text again

            # Keep the scrolled text in its last position for 2 seconds
            time.sleep(fixed_time)
        
        # Increment Y for the next network
        y_position += 17  # Increment Y for the next network

except Exception as e:
    print("Error getting access points:", e)
    tft.text(font, f"Error connecting to Wi-Fi: {e}", 0, 100)
