import st7789
import tft_config
import tft_buttons
import time as sleep
import vga1_8x16 as f

# Configure the TFT display
tft = tft_config.config(0)
tft.init()

# Initialize the buttons
buttons = tft_buttons.Buttons()

# Main loop
while True:
    # Clear the display before drawing new text
    tft.fill(0)  # Clear the display with black color (or whatever color you prefer)

    # Check for left button press
    if not buttons.left.value():  # Button is pressed (active low)
        tft.text(f, "Left", 20, 0)  # Display "Left" at (20, 20)
        print("Left button pressed!")
        sleep.sleep(0.1)  # Delay for debouncing

    # Optional: Check for right button press
    if not buttons.right.value():  # Button is pressed (active low)
        tft.text(f, "Right", 20, 50)  # Display "Right" at (20, 50)
        print("Right button pressed!")
        sleep.sleep(0.1)  # Delay for debouncing

    # Add a small delay in the loop to reduce CPU usage
    sleep.sleep(0.01)
