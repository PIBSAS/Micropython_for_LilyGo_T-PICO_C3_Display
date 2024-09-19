# Import the ESPC3 class
from TPicoESPC3 import ESPC3
from tft_config import config
from machine import ADC, Pin, SPI, PWM
import time
import st7789
import vga1_8x8 as font

# Initialize TFT display
tft = config(3)
tft.init()
tft.fill(st7789.BLACK)

# Initialize ESP Wi-Fi module
esp = ESPC3(debug=True)

# Initialize ADC for battery voltage reading
adc = ADC(Pin(26))  # Pin 26 is used for battery voltage sensing

# Pin setup for buttons
button_1 = Pin(6, Pin.IN, Pin.PULL_UP)
button_2 = Pin(7, Pin.IN, Pin.PULL_UP)

# Wi-Fi credentials configuration
secrets = {
    "ssid": "YOUR_WIFI",
    "password": "YOU_PASSWORD"
}

# Function to display text on the screen
def display_message(messages):
    tft.fill(st7789.BLACK)
    max_chars_per_line = 20  # Adjust this according to the screen width and font size
    y_offset = 5
    
    # Ensure 'messages' is a list
    if isinstance(messages, str):
        messages = [messages]
    
    # Process each message
    for message in messages:
        words = message.split(' ')
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars_per_line:
                current_line += word + " "
            else:
                tft.text(font, current_line.strip(), 5, y_offset, st7789.YELLOW)
                y_offset += 16  # Adjust line spacing
                current_line = word + " "
        
        # Print the last remaining line
        if current_line:
            tft.text(font, current_line.strip(), 5, y_offset, st7789.YELLOW)
            y_offset += 16  # Adjust spacing for the next line

# Function to gradually increase screen brightness
def set_brightness():
    backlight = PWM(Pin(4))  # Set GPIO4 as PWM
    backlight.freq(1000)  # Set the PWM frequency

    for i in range(0, 65536, 16):  # From 0 to 65535
        backlight.duty_u16(i)  # Set duty cycle directly
        time.sleep(0.005)

    backlight.duty_u16(65535)  # Set brightness to maximum

# Function to read the battery voltage
def read_battery_voltage():
    raw_value = adc.read_u16()
    voltage = (raw_value / 65535.0) * 3.3 * 2 + 0.05  # Adjust calculation based on your setup
    return voltage

# Function to display battery voltage on the TFT
def display_battery_voltage():
    voltage = read_battery_voltage()
    display_message(f"Battery: {voltage:.2f} V")

def wifi_test():
    # Connect to the Wi-Fi network
    esp.connect(secrets)
    print("Connected to the Wi-Fi network:", secrets["ssid"])
    tft.text(font, "Connecting to the Wi-Fi network:", 0, 0)
    tft.text(font, f"{secrets['ssid']}", 0, 20)
    # Get the local IP address
    ip_address = esp.get_ip()
    if ip_address:
        tft.text(font, f"IP Address: {ip_address}", 0, 40)
        print(f"IP Address: {ip_address}")
    else:
        print("No IP Address")
        tft.text(font, "No IP Address", 0, 100)
    # Wait a moment to ensure a stable connection
    time.sleep(2)

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

def display_wifi_data():
    try:
        # Get the local IP address
        ip_address = esp.get_ip()
        if ip_address:
            print(f"IP Address: {ip_address}")
        else:
            print("No IP Address")
        # Get the MAC address (you need to implement this method in your class)
        mac_address = esp.get_mac_address()  # New method to implement
        print(f"MAC Address: {mac_address}")
        
        # Display both data on the screen as a list
        display_message([f"IP Address: {ip_address}", f"MAC Address: {mac_address}"])

    except Exception as e:
        display_message("Error fetching Wi-Fi data")
        print(f"Error fetching Wi-Fi data: {e}")

def blink():
    led = Pin("LED", Pin.OUT)
    led.off()
    time.sleep(2)
    led.on()
    time.sleep(2)

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

def main():
    # Here we perform the Wi-Fi test
    wifi_test()
    # Wait some time to see the response
    time.sleep(2)  # Wait 5 seconds to see the result
    
    # Show the image need to upload to T-PicoC3, if you put the image in root, delete images/
    pico = 'images/RaspberryPi.jpg'
    tft.jpg(pico, 0, 0)  # Initial image
    
    # Configure gradual screen brightness
    set_brightness()
    
    # Main loop
    while True:
        blink()  # LED blinking or other tasks
        time.sleep(0.1)  # Wait time to avoid excessive CPU usage

# Call the main function to start the program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program stopped by the user.")
