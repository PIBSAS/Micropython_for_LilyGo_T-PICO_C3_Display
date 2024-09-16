# Import necessary modules
from tft_config import config
from machine import ADC, Pin, SPI, PWM
import time
import st7789
from TPicoESPC3 import ESPC3 # Your custom ESP class
import vga1_8x8 as font

# Initialize TFT display
tft = config(3)
tft.init()
tft.fill(st7789.BLACK)

# Initialize ESP Wi-Fi module (set the correct UART pins for your board)
esp = ESPC3(debug=True)

# Initialize ADC for battery voltage reading
adc = ADC(Pin(26))  # Pin 26 is used for battery voltage sensing

# Pin setup for buttons
button_1 = Pin(6, Pin.IN, Pin.PULL_UP)
button_2 = Pin(7, Pin.IN, Pin.PULL_UP)

# Configuración de las credenciales Wi-Fi
secrets = {
    "ssid": "YOUR_WIFI",
    "password": "CREDENTIAL"
}

# Function to display text on the screen
def display_message(messages):
    tft.fill(st7789.BLACK)
    max_chars_per_line = 20  # Ajusta esto según el ancho de la pantalla y el tamaño de la fuente
    y_offset = 5
    
    # Asegúrate de que 'messages' sea una lista
    if isinstance(messages, str):
        messages = [messages]
    
    # Procesa cada mensaje
    for message in messages:
        words = message.split(' ')
        current_line = ""
        
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
            y_offset += 16  # Ajusta el desplazamiento para la próxima línea

# Function to gradually increase screen brightness
def set_brightness():
    #print("Iniciando la configuración del brillo...")  # Mensaje inicial
    backlight = PWM(Pin(4))  # Configura GPIO4 como PWM
    backlight.freq(1000)  # Establece la frecuencia PWM
    #print("Frecuencia PWM establecida a 1000 Hz.")

    for i in range(0,65536,16):  # Del 0 al 65535
        backlight.duty_u16(i)  # Establece el ciclo de trabajo directamente
        time.sleep(0.005)
        #print(f"Brillo actual: {i}")

    backlight.duty_u16(65535)  # Establecer el brillo al máximo
    #print("Brillo establecido al máximo.")

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
   # try:
    # Conectar a la red Wi-Fi
    esp.connect(secrets)
    print("Conectado a la red Wi-Fi:", secrets["ssid"])
    tft.text(font, "Conectando a la red Wi-fi:", 0, 0)
    tft.text(font, f"{secrets['ssid']}", 0, 20)
    # Obtener la dirección IP local
    ip_address = esp.get_ip()
    if ip_address:
        tft.text(font, f"IP Address: {ip_address}", 0, 40)
        print(f"IP Address: {ip_address}")
    else:
        print("No IP Address")
        tft.text(font, "No IP Address", 0, 100)
    # Esperar un momento para asegurar que la conexión sea estable
    time.sleep(2)

        # Enviar solicitud AT+HTTPCGET para acceder a una URL
        #tft.text(font, "Intentando conectarse a:", 0, 40)
        #tft.text(font, "https://www.google.com", 0, 60)
        #response = esp.send('AT+HTTPCGET="https://www.google.com/"')
        #if response is None or len(response) == 0:
        #    print("No se recibió respuesta válida.")
        #    tft.text(font, "Error: No response", 0, 120, st7789.RED)
        #else:
            # Mostrar respuesta en la pantalla
        #    tft.fill(st7789.BLACK)
        #    tft.text(font, response[:20], 0, 0)  # Mostrar las primeras 20 letras de la respuesta

    #except Exception as e:
    #    print(f"Error durante la conexión o la solicitud HTTP: {e}")
    #    tft.text(font, f"Error: {e}", 0, 120, st7789.RED)



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
        # Obtener la dirección IP local
        ip_address = esp.get_ip()
        if ip_address:
            print(f"IP Address: {ip_address}")
        else:
            print("No IP Address")
        # Obtener la dirección MAC (deberás implementar este método en tu clase)
        mac_address = esp.get_mac_address()  # Nuevo método a implementar
        print(f"MAC Address: {mac_address}")
        
        # Mostrar ambos datos en la pantalla como una lista
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
    # Aquí realizamos la prueba Wi-Fi
    wifi_test()
    # Esperar un tiempo para ver la respuesta
    time.sleep(2)  # Esperar 5 segundos para que se vea el resultado
    
    # Mostrar una imagen
    pico = 'RaspberryPi.jpg'
    tft.jpg(pico, 0, 0)  # Imagen inicial
    
    #Configurar el brillo gradual de la pantalla
    set_brightness()
    
    # Bucle principal
    while True:
        blink()  # Parpadeo de LED u otras tareas
        time.sleep(0.1)  # Tiempo de espera para evitar el uso excesivo de CPU

# Llamar a la función principal para iniciar el programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
