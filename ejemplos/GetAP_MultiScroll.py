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
    y_position_inicial = 16  # Posición inicial en Y
    pantalla_ancho = 240  # Ancho de la pantalla
    tiempo_fijo = 1  # Tiempo fijo para mostrar el texto sin desplazamiento
    velocidad_scroll = 5  # Velocidad del scroll en píxeles
    
    print("Puntos de acceso disponibles:")
    tft.text(font, "Puntos de acceso disponibles:" ,0, 0, st7789.YELLOW)
    
    y_positions = []  # Lista para almacenar las posiciones Y de cada línea
    textos = []  # Lista para almacenar cada línea de texto
    
    # Mostrar todas las redes de forma estática primero
    y_position = y_position_inicial
    
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
        
        # Guardar texto y posición para después
        textos.append(texto)
        y_positions.append(y_position)

        # Mostrar el texto de forma estática
        tft.text(font, texto, 0, y_position, st7789.CYAN)
        y_position += 16  # Incrementar Y para la próxima red

    # Mantener los resultados fijos durante 2 segundos
    time.sleep(tiempo_fijo)
        
     # Ahora hacer scroll para todas las líneas al mismo tiempo
    for desplazamiento in range(0, max(len(texto) * 8 for texto in textos) - pantalla_ancho + 1, velocidad_scroll):
        for i, texto in enumerate(textos):
            tft.fill_rect(0, y_positions[i], pantalla_ancho, 17, st7789.BLACK)  # Borrar la línea anterior
            tft.text(font, texto, -desplazamiento, y_positions[i], st7789.CYAN)  # Dibujar el texto desplazado
        time.sleep(0.05)  # Ajusta la velocidad del scroll
    
    # Después del scroll, mostrar nuevamente las líneas fijas por 2 segundos
    tft.fill(st7789.BLACK)  # Borrar la pantalla
    for i, texto in enumerate(textos):
        tft.text(font, "Puntos de acceso disponibles:" ,0, 0, st7789.YELLOW)
        tft.text(font, texto, 0, y_positions[i], st7789.CYAN)
    
    time.sleep(tiempo_fijo)
    
except Exception as e:
    print("Error al obtener puntos de acceso:", e)

