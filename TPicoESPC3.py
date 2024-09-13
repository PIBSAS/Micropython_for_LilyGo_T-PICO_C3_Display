from machine import UART, Pin
import time

class ESPC3:
    STATUS_APCONNECTED = 2
    STATUS_SOCKETOPEN = 3
    STATUS_SOCKETCLOSED = 4
    STATUS_NOTCONNECTED = 5

    MODE_STATION = 1
    MODE_SOFTAP = 2
    MODE_SOFTAPSTATION = 3

    def __init__(self,
                 uart_id=1,  # Cambia a UART1, que se usa en el ejemplo anterior
                 tx_pin=8,
                 rx_pin=9,
                 baud_rate=115200,
                 tx_buffer=1024,
                 rx_buffer=2048,
                 debug=False):
        """ Inicializa el UART para el módulo ESP32C3 """
        self._debug = debug
        
        try:
            self._uart = UART(uart_id,
                              baudrate=baud_rate,
                              tx=Pin(tx_pin),
                              rx=Pin(rx_pin),
                              txbuf=tx_buffer,
                              rxbuf=rx_buffer)
            if self._debug:
                print("UART inicializado correctamente.")
        except Exception as e:
            print("Error al inicializar UART:", e)
            self._uart = None
            
    def send(self, at, timeout=20, retries=3):
        """ Envía un comando AT, verifica que obtuvimos una respuesta OK,
            y luego devuelve el texto de la respuesta.
        """
        for _ in range(retries):
            if self._debug:
                print("tx ---> ", at)
            
            self._uart.write(bytes(at, "utf-8"))
            self._uart.write(b"\x0d\x0a")  # Enviar CR+LF
            stamp = time.time()
            response = b""
            
            while (time.time() - stamp) < timeout:
                if self._uart.any():
                    response += self._uart.read(1)
                    if response[-4:] == b"OK\r\n":
                        break
                    if response[-7:] == b"ERROR\r\n":
                        break
            
            if self._debug:
                print("<--- rx ", response)

            if response[-4:] == b"OK\r\n":
                return response[:-4]  # Retorna la respuesta sin 'OK'
            
            time.sleep(1)  # Espera antes de reintentar
        raise Exception("No OK response to " + at)
    
    def enable_ipv6(self):
        """ Habilita el uso de IPv6 en el módulo ESP32C3. """
        self.send("AT+CIPV6=1", timeout=3)
        print("IPv6 habilitado.")
    
    def ping(self, host):
        """ Pinga el IP o nombre de host dado, devuelve el tiempo en ms o None en caso de fallo
        """
        # Asegúrate de habilitar IPv6 si es necesario
        self.enable_ipv6()  # Llama a la función para habilitar IPv6
        
        reply = self.send('AT+PING="%s"' % host.strip('"'), timeout=5)
        for line in reply.split(b"\r\n"):
            if line and line.startswith(b"+"):
                try:
                    if line[1:5] == b"PING":
                        return int(line[6:])
                    return int(line[1:])
                except ValueError:
                    return None
        raise RuntimeError("Couldn't ping")

    def connect(self, secrets):
        """ Intenta conectarse a un punto de acceso con los detalles en
            el diccionario 'secrets' pasado.
        """
        retries = 3
        while retries > 0:
            try:
                if not self.is_connected:
                    self.join_ap(secrets["ssid"], secrets["password"])
                return True
            except RuntimeError as exp:
                print("Failed to connect, retrying\n", exp)
                retries -= 1
                time.sleep(2)  # Espera antes de reintentar

    def parse_cwjap_response(self, reply):
        """Parsea la respuesta del comando +CWJAP? para extraer todos los valores."""
        # La respuesta viene en la forma +CWJAP:<ssid>,<bssid>,<channel>,<rssi>,<pci_en>,<reconn_interval>,<listen_interval>,<scan_mode>,<pmf>
        replies = reply.split(b"\r\n")
        
        for line in replies:
            if line.startswith(b"+CWJAP:"):
                # Elimina el prefijo "+CWJAP:" y divide los valores
                line = line[7:].split(b",")
                
                # Procesar y almacenar cada campo
                parsed_values = {
                    "ssid": str(line[0], "utf-8").strip('"'),          # SSID
                    "bssid": str(line[1], "utf-8").strip('"'),         # BSSID
                    "channel": int(line[2]),                           # Canal
                    "rssi": int(line[3]),                              # RSSI
                    "pci_en": int(line[4]),                            # PCI habilitado
                    "reconn_interval": int(line[5]),                   # Intervalo de reconexión
                    "listen_interval": int(line[6]),                   # Intervalo de escucha
                    "scan_mode": int(line[7]),                         # Modo de escaneo
                    "pmf": int(line[8])                                # PMF (Frame Management Protection)
                }
                return parsed_values
        return None
    
    def join_ap(self, ssid, password):
        """ Intenta unirse a un punto de acceso por nombre y contraseña. """
        if self.mode != self.MODE_STATION:
            self.mode = self.MODE_STATION
        
        # Si ya está conectado a la red especificada, devolver la información directamente
        cwjap_reply = self.send("AT+CWJAP?", timeout=10)
        parsed_cwjap = self.parse_cwjap_response(cwjap_reply)
        
        if parsed_cwjap and parsed_cwjap['ssid'] == ssid:
            return parsed_cwjap  # Ya estamos conectados, devolver la información
    
        # Intentar conectar al AP
        for _ in range(3):
            reply = self.send(
                f'AT+CWJAP="{ssid}","{password}"', timeout=15, retries=3
            )
            
            # Comprobar si la conexión fue exitosa
            if b"WIFI CONNECTED" in reply and b"WIFI GOT IP" in reply:
                # Obtener detalles de la conexión
                cwjap_reply = self.send("AT+CWJAP?", timeout=10)
                parsed_cwjap = self.parse_cwjap_response(cwjap_reply)
                if parsed_cwjap:
                    return parsed_cwjap
        # Si falla después de 3 intentos, lanzar una excepción
        raise Exception("No se pudo conectar a la red.")

    @property
    def is_connected(self):
        """ Verifica si estamos conectados a un punto de acceso.
        """
        state = self.status
        return state in (self.STATUS_APCONNECTED, self.STATUS_SOCKETOPEN, self.STATUS_SOCKETCLOSED)

    @property
    def status(self):
        """ El estado de la conexión IP.
        """
        replies = self.send("AT+CIPSTATUS", timeout=5).split(b"\r\n")
        for reply in replies:
            if reply.startswith(b"STATUS:"):
                return int(reply[7:8])
        return None

    @property
    def remote_AP(self):
        """ El nombre del punto de acceso al que estamos conectados, como una cadena.
        """
        if self.status != self.STATUS_APCONNECTED:
            return [None] * 4

        replies = self.send("AT+CWJAP?", timeout=10).split(b"\r\n")
        for reply in replies:
            if reply.startswith(b"+CWJAP:"):
                reply = reply[7:].split(b",")
                print("Respuesta de +CWJAP:", reply)  # Agregar depuración aquí
                try:
                    # Convertir cada valor al tipo correspondiente
                    ssid = str(reply[0], "utf-8").strip('"')  # SSID como string
                    bssid = str(reply[1], "utf-8")  # BSSID como string
                    channel = int(reply[2])  # Canal como entero
                    rssi = int(reply[3])  # RSSI como entero
                    # Agrega más campos si es necesario según el formato
                    return [ssid, bssid, channel, rssi]
                except (ValueError, IndexError) as e:
                    print("Error al analizar la respuesta de +CWJAP:", e)
                    return [None] * 4  # Devolver valores por defecto en caso de error
                
        return [None] * 4

    @property
    def mode(self):
        replies = self.send("AT+CWMODE?", timeout=5).split(b"\r\n")
        for reply in replies:
            if reply.startswith(b"+CWMODE:"):
                return int(reply[8:])
        raise RuntimeError("Bad response to CWMODE?")

    @mode.setter
    def mode(self, mode):
        """ Selección del modo: puede ser MODE_STATION, MODE_SOFTAP o MODE_SOFTAPSTATION.
        """
        if mode not in (1, 2, 3):
            raise RuntimeError("Invalid Mode")
        self.send("AT+CWMODE=%d" % mode, timeout=3)

    @property
    def local_ip(self):
        """ Nuestra dirección IP local como una cadena de puntos.
        """
        reply = self.send("AT+CIFSR").strip(b"\r\n")
        for line in reply.split(b"\r\n"):
            if line.startswith(b'+CIFSR:STAIP,"'):
                return str(line[14:-1], "utf-8")
        raise RuntimeError("Couldn't find IP address")
    
    """
    def print_APs(self, ap_data):
        # Imprime los puntos de acceso de forma más legible.
        print("\nPuntos de acceso disponibles:")
        print("=" * 60)  # Línea de separación
        for ap in ap_data:
            ssid = ap[1].decode('utf-8')  # Decodificar el SSID
            rssi = ap[2]
            mac = ap[3].decode('utf-8')  # Decodificar la dirección MAC
            channel = ap[4]
            scan_type = ap[5]
            min_scan_time = ap[6]
            max_scan_time = ap[7]
            encrypt = ap[8]
            group_encrypt = ap[9]
            supports_802_11 = ap[10]
            wps = ap[11]
            security = "Desconocido"
        
            # Determinar el tipo de seguridad
            if encrypt == 0:
                security = "Ninguna"
            elif encrypt == 1:
                security = "WEP"
            elif encrypt in [2, 3]:
                security = "WPA/WPA2-PSK"
            elif encrypt == 4:
                security = "WPA2-PSK"

            # Imprimir información del punto de acceso
            print(f"SSID: {ssid}")
            print(f"  RSSI: {rssi} dBm")
            print(f"  MAC: {mac}")
            print(f"  Canal: {channel}")
            print(f"  Tipo de escaneo: {scan_type}")
            print(f"  Tiempo mínimo de escaneo: {min_scan_time}")
            print(f"  Tiempo máximo de escaneo: {max_scan_time}")
            print(f"  Par de cifrado: {encrypt}")
            print(f"  Grupo de cifrado: {group_encrypt}")
            print(f"  Soporte 802.11: {supports_802_11}")
            print(f"  WPS: {wps}")
            print(f"  Seguridad: {security}")
            print("-" * 60)  # Línea de separación entre APs
        print("=" * 60)  # Línea de cierre
    """    
    def get_AP(self, retries=3):
        for _ in range(retries):
            try:
                if self.mode != self.MODE_STATION:
                    self.mode = self.MODE_STATION
                # Enviar comando AT para escanear puntos de acceso
                scan = self.send("AT+CWLAP", timeout=5).split(b"\r\n")
            except RuntimeError:
                continue
            
            routers = []
            
            for line in scan:
                if line.startswith(b"+CWLAP:("):
                    # Analizar la línea de respuesta
                    line = line[8:-1].split(b",")
                    router = ["Desconocido"] * 12 # Inicializa con valores por defecto
                    
                    for i, val in enumerate(line):  # Ignorar el primer valor
                        # Convertir el valor a string y manejarlo adecuadamente
                        try:
                            if i == 0:  # Método de cifrado
                                encryption_method = int(val)
                                encryption_mapping = {
                                    0: "Ninguna", 1: "WEP", 2: "WPA-PSK",
                                    3: "WPA2-PSK", 4: "WPA/WPA2-PSK", 5: "WPA2 Enterprise",
                                    6: "WPA3-PSK", 7: "WPA2/WPA3-PSK", 8: "WAPI-PSK", 9: "OWE"
                                }
                                router[0] = encryption_mapping.get(encryption_method, "Desconocido")
                            elif i == 1:  # SSID
                                router[1] = str(val, "utf-8").strip('"') # SSID como string
                            elif i == 2:  # RSSI
                                router[2] = int(val)  # RSSI como entero
                            elif i == 3:  # MAC
                                router[3] = str(val, "utf-8")  # MAC como string
                            elif i == 4:  # Canal
                                router[4] = int(val)  # Canal como entero
                            elif i == 5:  # Tipo de escaneo (se puede ignorar)
                                router[5] = int(val)  # Se puede almacenar si es necesario
                            elif i == 6:  # Tiempo mínimo de escaneo
                                router[6] = int(val)  # Se puede almacenar si es necesario
                            elif i == 7:  # Tiempo máximo de escaneo
                                router[7] = int(val)
                            elif i == 8:  # Cifrado par
                                router[8] = int(val)  # Se puede almacenar si es necesario
                            elif i == 9:  # Cifrado grupo
                                router[9] = int(val)  # Se puede almacenar si es necesario
                            elif i == 10:  # Bandas (b/g/n)
                                router[10] = int(val)  # Se puede almacenar si es necesario
                            elif i == 11:  # WPS
                                router[11] = int(val)  # Se puede almacenar si es necesario    
                        except ValueError:
                            # Si no se puede convertir, almacenar como string
                            router[i] =str(val, "utf-8").strip('"')
                    routers.append(router)
            return routers
        return []
