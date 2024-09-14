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
    pantalla_ancho = 240  # Ancho de la pantalla
    tiempo_fijo = 1  # Tiempo fijo para mostrar el texto sin desplazamiento
    velocidad_scroll = 5  # Velocidad del scroll en píxeles
    
    print("Puntos de acceso disponibles:")
    tft.text(font, "Puntos de acceso disponibles:" ,0, 0, st7789.YELLOW)
    
    for ap in ap_list:
        print("SSID:", ap[1], "RSSI:", ap[2], "MAC:", ap[3], "Canal:", ap[4], 
              "Tipo de escaneo:", ap[5], "Tiempo mínimo de escaneo:", ap[6], 
              "Tiempo máximo de escaneo:", ap[7], "Par de cifrado:", ap[8], 
              "Grupo de cifrado:", ap[9], "Soporte 802.11:", ap[10], "WPS:", ap[11], 
              "Seguridad:", ap[0])
        
        texto = (f"SSID:{ap[1]}, RSSI:{ap[2]}, MAC:{ap[3]}, Canal:{ap[4]}, "
                 f"Tipo de escaneo:{ap[5]}, Tiempo mínimo de escaneo:{ap[6]}, "
                 f"Tiempo máximo de escaneo:{ap[7]}, Par de cifrado:{ap[8]}, "
                 f"Grupo de cifrado:{ap[9]}, Soporte 802.11:{ap[10]}, WPS:{ap[11]}, "
                 f"Seguridad:{ap[0]}")
        
        # Mostrar el texto de forma estática durante 2 segundos
        tft.text(font, texto, 0, y_position, st7789.CYAN)
        time.sleep(tiempo_fijo)
        
        # Obtener el ancho del texto en píxeles (usando fuente 8x16)
        texto_ancho = len(texto) * 8
        
        # Si el texto es más ancho que la pantalla, hacer scroll
        if texto_ancho > pantalla_ancho:
            for desplazamiento in range(0, texto_ancho - pantalla_ancho + 1, velocidad_scroll):
                tft.fill_rect(-1, y_position, pantalla_ancho, 17, st7789.BLACK)  # Borrar la línea anterior
                tft.text(font, texto, -desplazamiento, y_position, st7789.CYAN)  # Dibujar el texto desplazado
                time.sleep(0.05)  # Ajusta la velocidad de desplazamiento
            
            # Volver a la posición inicial y mostrar el texto completo sin desplazamiento por 2 segundos
            tft.fill_rect(0, y_position, pantalla_ancho, 16, st7789.BLACK)  # Borrar la línea
            tft.text(font, texto, 0, y_position, st7789.CYAN)  # Mostrar el texto completo nuevamente

            # Mantener el texto desplazado en su última posición por 2 segundos
            time.sleep(tiempo_fijo)
        
        # Incrementar Y para la próxima red    
        y_position += 17  # Incrementa Y para la próxima red

except Exception as e:
    print("Error al obtener puntos de acceso:", e)
