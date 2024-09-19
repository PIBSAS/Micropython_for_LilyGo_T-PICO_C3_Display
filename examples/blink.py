from machine import Pin
import time
import st7789, tft_config
import chango_16 as font

tft = tft_config.config(0)
tft.init()
# Define the built-in LED pin
LED_BUILTIN = 25
led = Pin(LED_BUILTIN, Pin.OUT)

# Initial setup
def setup():
    led.value(0)  # Initialize the LED off

# Main loop
def loop():
    try:
        while True:
            led.value(1)  # Turn on the LED
            tft.fill(st7789.BLACK)
            tft.write(font, "ON", 50, 50)
            time.sleep(1)  # Wait for 1 second
            led.value(0)  # Turn off the LED
            tft.fill(st7789.BLACK)
            tft.write(font, "OFF", 50, 50)
            time.sleep(1)  # Wait for 1 second
    except KeyboardInterrupt:
        led.value(0)  # Turn off the LED on exit
        tft.fill(st7789.BLACK)  # Clear the display
        print("Program stopped by the user.")

# Execution
setup()
loop()
