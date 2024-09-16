# Importar la clase TPicoESPC3
from TPicoESPC3 import ESPC3
from tft_config import config
import vga1_8x8 as font
import st7789
from time import sleep

tft = config(3)
tft.init()

# Definir el SSID y la contraseña de la red Wi-Fi
ssid = "TELWINET:9E-5E_EXT"
password = "68297640"

# Inicializar el módulo ESP32C3
esp = ESPC3()

# Configuración para el scroll
pantalla_ancho = tft.width()  # Ancho de la pantalla usando St7789
tiempo_fijo = 2  # Tiempo fijo para mostrar el texto sin desplazamiento
velocidad_scroll = 5  # Velocidad del scroll en píxeles
y_position = 9  # Posición inicial en Y

# Ejemplo de uso
try:
    connection_info = esp.join_ap(ssid, password)
    if connection_info:
        # Mostrar mensaje "Conectando a la red Wi-Fi:"
        tft.text(font, "Conectando a la red Wi-Fi:", 0, 0, st7789.WHITE)

        # Calcular la posición centrada para el SSID
        ssid_ancho = len(connection_info['ssid']) * 8  # Ancho del SSID (asumiendo fuente 8x8)
        ssid_x_pos = (pantalla_ancho - ssid_ancho) // 2  # Posición X para centrar el SSID

        # Mostrar el SSID centrado en la línea siguiente
        tft.text(font, connection_info['ssid'], ssid_x_pos, 9, st7789.MAGENTA)
        y_position += 9
        print("Conectado a la red Wi-Fi:", connection_info['ssid'])
        
        tft.text(font, "Detalles de la conexión", 0, y_position, st7789.YELLOW)
        print("Detalles de la conexión:")
        y_position += 9

        for key, value in connection_info.items():
            texto = f"{key}: {value}"
            print(texto)
            texto_ancho = len(texto) * 8  # Calcular el ancho del texto (asumiendo fuente 8x8)

            # Mostrar el texto de forma estática durante un tiempo fijo
            tft.text(font, texto, 0, y_position, st7789.CYAN)
            sleep(tiempo_fijo)

            # Si el texto es más ancho que la pantalla, hacer scroll
            if texto_ancho > pantalla_ancho:
                for desplazamiento in range(0, texto_ancho - pantalla_ancho + 1, velocidad_scroll):
                    tft.fill_rect(0, y_position, pantalla_ancho, 8, st7789.BLACK)  # Borrar la línea anterior
                    tft.text(font, texto, -desplazamiento, y_position, st7789.CYAN)  # Dibujar el texto desplazado
                    sleep(0.05)  # Ajusta la velocidad de desplazamiento

                # Volver a la posición inicial y mostrar el texto completo sin desplazamiento por 2 segundos
                tft.fill_rect(0, y_position, pantalla_ancho, 8, st7789.BLACK)  # Borrar la línea
                tft.text(font, texto, 0, y_position, st7789.CYAN)  # Mostrar el texto completo nuevamente
                sleep(tiempo_fijo)

            # Incrementar Y para la próxima línea
            y_position += 9  # Incrementa Y para la próxima línea
except Exception as e:
    print("Error al conectarse a la red Wi-Fi:", e)
    tft.text(font, f"Error al conectarse a la red Wi-Fi: {e}", 0, y_position, st7789.RED)
