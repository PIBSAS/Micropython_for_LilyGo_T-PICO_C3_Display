# Import necessary modules
import tft_config
from machine import ADC, Pin, SPI
import time
import st7789
from TPicoESPC3 import ESPC3 # Your custom ESP class
import vga1_8x8 as font

# Initialize TFT display
tft = tft_config.config(rotation=1)
tft.init()
tft.fill(st7789.BLACK)

# Initialize ESP Wi-Fi module (set the correct UART pins for your board)
esp = ESPC3(debug=True)

# Initialize ADC for battery voltage reading
adc = ADC(Pin(26))  # Pin 26 is used for battery voltage sensing

# Pin setup for buttons
button_1 = Pin(6, Pin.IN, Pin.PULL_UP)
button_2 = Pin(7, Pin.IN, Pin.PULL_UP)

# Function to display text on the screen
def display_message(message):
    tft.fill(st7789.BLACK)
    max_chars_per_line = 20  # Ajusta esto según el ancho de la pantalla y el tamaño de la fuente
    words = message.split(' ')
    current_line = ""
    y_offset = 5
    
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += word + " "
        else:
            tft.text(font, current_line.strip(), 5, y_offset, st7789.YELLOW)
            y_offset += 16  # Ajusta la distancia entre líneas
            current_line = word + " "
    
    # Imprime la última línea restante
    if current_line:
        tft.text(font, current_line.strip(), 5, y_offset, st7789.YELLOW)

# Function to gradually increase screen brightness
def set_brightness():
    backlight = Pin(4, Pin.OUT)
    for i in range(256):
        backlight.duty_u16(i * i)  # simulate smooth fade-in
        time.sleep(0.005)

# Function to read the battery voltage
def read_battery_voltage():
    raw_value = adc.read_u16()
    voltage = (raw_value / 65535.0) * 3.3 * 2 + 0.05  # Adjust calculation based on your setup
    return voltage

# Function to display battery voltage on the TFT
def display_battery_voltage():
    voltage = read_battery_voltage()
    display_message(f"Battery: {voltage:.2f} V")

# Function to scan and display Wi-Fi networks on the TFT
def scan_wifi_networks():
    try:
        networks = esp.get_AP()
        tft.fill(st7789.BLACK)
        y_offset = 0
        for network in networks:
            ssid = network[1]
            rssi = network[2]
            tft.text(font, f"SSID:{ssid}", 0, y_offset, st7789.WHITE)
            y_offset += 16  # Adjust line height for each network entry
            tft.text(font, f"RSSI:{rssi}dBm", 0, y_offset, st7789.RED)
            y_offset += 16
            if y_offset > tft.height():  # Stop if we go beyond the screen size
                break
    except Exception as e:
        display_message("Wi-Fi Scan Error")
        print(f"Error scanning Wi-Fi: {e}")

# Button 1 handler: Scan Wi-Fi networks
def button_1_handler(pin):
    display_message("Button 1 Pressed: Scanning networks...")
    scan_wifi_networks()

# Button 2 handler: Display battery voltage
def button_2_handler(pin):
    display_battery_voltage()

# Set up interrupts for the buttons
button_1.irq(trigger=Pin.IRQ_FALLING, handler=button_1_handler)
button_2.irq(trigger=Pin.IRQ_FALLING, handler=button_2_handler)

# Main loop can be empty, as button presses handle events
while True:
    time.sleep(1)  # Just keeping the main loop alive
