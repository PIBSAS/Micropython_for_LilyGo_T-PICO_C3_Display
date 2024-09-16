# Importar la clase TPicoESPC3
from TPicoESPC3 import ESPC3
import time

# Inicializar el módulo ESP32C3
esp = ESPC3(debug=True)

# Conectar a Wi-Fi
esp.send('AT+CWJAP="TELWINET:9E-5E_EXT","68297640"')

# Configurar el ESP32-C3 como servidor
esp.send('AT+CIPMUX=1')  # Habilitar múltiples conexiones
esp.send('AT+CIPSERVER=1,80')  # Iniciar servidor en el puerto 80

while True:
    # Chequear el estado de las conexiones
    response = esp.send('AT+CIPSTATUS', 0.5)
    print(response)

    # Verificar si hay una conexión entrante
    if '+IPD,' in response:  # Detecta la entrada de datos de una conexión
        print('Conexión entrante detectada.')

        # Contenido HTML
        html_content = '<html><body><h1>Hello from Pico!</h1></body></html>'
        content_length = len(html_content)

        # Preparar encabezados HTTP
        headers = (
            'HTTP/1.1 200 OK\r\n'
            'Content-Type: text/html\r\n'
            'Content-Length: ' + str(content_length) + '\r\n'
            'Connection: close\r\n'
            '\r\n'  # Asegúrate de que este salto de línea esté al final
        )

        total_length = len(headers) + content_length

        # Enviar longitud precisa (encabezados + contenido)
        esp.send(f'AT+CIPSEND=0,{total_length}')  # Longitud total exacta

        # Enviar encabezados HTTP
        response = esp.send(headers)
        print('Enviando encabezados:', headers)
        if b'OK' in response:
            # Ahora enviar el contenido HTML solo si los encabezados fueron enviados con éxito
            response = esp.send(html_content)
            print('Enviando contenido HTML:', html_content)
            if b'ERROR' in response:
                print('Error al enviar contenido HTML:', response)
        else:
            print('Error al enviar encabezados:', response)

        # Cerrar la conexión
        esp.send('AT+CIPCLOSE=0')

    # Esperar un momento antes de verificar nuevamente
    time.sleep(1)
