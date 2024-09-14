# Importar la clase TPicoESPC3
from TPicoESPC3 import ESPC3
import st7789, tft_config, time
import vga1_8x16 as font

tft = tft_config.config(3)
tft.init()
tft.fill(st7789.BLACK)

# Inicializar el módulo ESP32C3
esp = ESPC3() # Se puede activar el debug ingreando el parametro debug=True

# Obtener la lista de puntos de acceso
try:
    ap_list = esp.get_AP()
    y_position = 16  # Posición inicial en Y
    print("Puntos de acceso disponibles:")
    tft.text(font, "Puntos de acceso disponibles:" ,0, 0, st7789.YELLOW)
    for ap in ap_list:
        print("SSID:", ap[1], "RSSI:", ap[2], "MAC:", ap[3], "Canal:", ap[4], 
              "Tipo de escaneo:", ap[5], "Tiempo mínimo de escaneo:", ap[6], 
              "Tiempo máximo de escaneo:", ap[7], "Par de cifrado:", ap[8], 
              "Grupo de cifrado:", ap[9], "Soporte 802.11:", ap[10], "WPS:", ap[11], 
              "Seguridad:", ap[0])
    
        tft.text(font, f"SSID:{ap[1]}, RSSI:{ap[2]}, MAC:{ap[3]}, Canal:{ap[4]}, "
                       f"Tipo de escaneo:{ap[5]}, Tiempo mínimo de escaneo:{ap[6]}, "
                       f"Tiempo máximo de escaneo:{ap[7]}, Par de cifrado:{ap[8]}, "
                       f"Grupo de cifrado:{ap[9]}, Soporte 802.11:{ap[10]}, WPS:{ap[11]}, "
                       f"Seguridad:{ap[0]}", 
                       0, y_position, st7789.CYAN)
        
        y_position += 17  # Incrementa Y para la próxima red

except Exception as e:
    print("Error al obtener puntos de acceso:", e)