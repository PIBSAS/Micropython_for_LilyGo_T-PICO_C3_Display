# Import the ESPC3 class
from TPicoESPC3 import ESPC3
from tft_config import config
import vga1_8x8 as font
import st7789
from time import sleep

tft = config(3)
tft.init()

# Define the Wi-Fi network SSID and password
ssid = "SSID"
password = "PASSWORD"

# Initialize the ESP32C3 module
esp = ESPC3()

# Scroll configuration
screen_width = tft.width()  # Screen width using ST7789
fixed_time = 2  # Fixed time to display text without scrolling
scroll_speed = 5  # Scrolling speed in pixels
y_position = 9  # Initial Y position

# Example usage
try:
    connection_info = esp.join_ap(ssid, password)
    if connection_info:
        tft.text(font, "Connecting to Wi-Fi network:", 0, 0, st7789.WHITE)

        ## Calculate the centered position for the SSID
        ssid_width = len(connection_info['ssid']) * 8  # Width of the SSID (assuming 8x8 font)
        ssid_x_pos = (screen_width - ssid_width) // 2  # X position to center the SSID

        # Display the centered SSID on the next line
        tft.text(font, connection_info['ssid'], ssid_x_pos, 9, st7789.MAGENTA)
        # Increment Y for the next line
        y_position += 9
        print("Connected to Wi-Fi network:", connection_info['ssid'])
        
        tft.text(font, "Connection details", 0, y_position, st7789.YELLOW)
        print("Connection details:")
        y_position += 9

        for key, value in connection_info.items():
            text = f"{key}: {value}"
            print(text)
            text_width = len(text) * 8  # Calculate the width of the text (assuming 8x8 font)

            # Display the text statically for a fixed amount of time
            tft.text(font, text, 0, y_position, st7789.CYAN)
            sleep(fixed_time)

            # If the text is wider than the screen, scroll it
            if text_width > screen_width:
                for scroll in range(0, text_width - screen_width + 1, scroll_speed):
                    tft.fill_rect(0, y_position, screen_width, 8, st7789.BLACK)  # Clear the previous line
                    tft.text(font, text, -scroll, y_position, st7789.CYAN)  # Draw the scrolled text
                    sleep(0.05)  # Adjust the scroll speed

                # Return to the initial position and display the complete text without scrolling for 2 seconds
                tft.fill_rect(0, y_position, screen_width, 8, st7789.BLACK)  # Clear the line
                tft.text(font, text, 0, y_position, st7789.CYAN)  # Display the complete text again
                sleep(fixed_time)

            y_position += 9

except Exception as e:
    print("Error connecting to Wi-Fi network:", e)
    tft.text(font, f"Error connecting to Wi-Fi network: {e}", 0, y_position, st7789.RED)
