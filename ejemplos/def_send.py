# Importar la clase ESPC3
from TPicoESPC3 import ESPC3
import time

# Inicializa el ESPC3
esp = ESPC3(debug=True)

# Intentar obtener la dirección IP usando send
try:
    # Enviar el comando AT para obtener la dirección IP
    ip_response = esp.send("AT+CIFSR")
    
    # Procesar la respuesta
    # La respuesta generalmente será en el formato +CIFSR:STAIP,"<ip_address>"
    for line in ip_response.split(b"\r\n"):
        if line.startswith(b'+CIFSR:STAIP,"'):
            # Extraer y mostrar la dirección IP
            ip_address = str(line[14:-1], "utf-8")
            print("Dirección IP del ESP32C3:", ip_address)
except Exception as e:
    print("Error al obtener la dirección IP:", e)
