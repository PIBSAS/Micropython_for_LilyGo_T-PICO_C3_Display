# Import the TPicoESPC3 class
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
    initial_y_position = 16  # Initial Y position
    screen_width = 240  # Width of the screen
    fixed_time = 1  # Fixed time to display the text without scrolling
    scroll_speed = 5  # Scrolling speed in pixels
    
    print("Available access points:")
    tft.text(font, "Available access points:", 0, 0, st7789.YELLOW)
    
    y_positions = []  # List to store the Y positions of each line
    texts = []  # List to store each line of text
    
    # Display all networks statically first
    y_position = initial_y_position
    
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
        
        # Store text and position for later
        texts.append(text)
        y_positions.append(y_position)

        # Display the text statically
        tft.text(font, text, 0, y_position, st7789.CYAN)
        y_position += 16  # Increment Y for the next network

    # Keep the results fixed for 2 seconds
    time.sleep(fixed_time)
        
    # Now scroll all lines at the same time
    for scroll in range(0, max(len(text) * 8 for text in texts) - screen_width + 1, scroll_speed):
        for i, text in enumerate(texts):
            tft.fill_rect(0, y_positions[i], screen_width, 17, st7789.BLACK)  # Clear the previous line
            tft.text(font, text, -scroll, y_positions[i], st7789.CYAN)  # Draw the scrolled text
        time.sleep(0.05)  # Adjust the scrolling speed
    
    # After scrolling, display the lines again statically for 2 seconds
    tft.fill(st7789.BLACK)  # Clear the screen
    for i, text in enumerate(texts):
        tft.text(font, "Available access points:", 0, 0, st7789.YELLOW)
        tft.text(font, text, 0, y_positions[i], st7789.CYAN)
    
    time.sleep(fixed_time)
    
except Exception as e:
    print("Error getting access points:", e)
    tft.text(font, f"Error connecting to Wi-Fi: {e}", 0, 100)
