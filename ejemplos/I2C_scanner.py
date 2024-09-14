from machine import I2C, Pin
import time

# Definir los pines SDA y SCL
I2C_SDA = 12
I2C_SCL = 13

# Crear el objeto I2C
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)

# Función de configuración inicial
def setup():
    print("\n\nI2C scanner. Scanning... SDA", I2C_SDA, "SCL", I2C_SCL)
    time.sleep(0.5)

# Función principal para escanear dispositivos I2C
def loop():
    while True:
        devices = i2c.scan()
        count = len(devices)

        if count == 0:
            print("No I2C devices found")
        else:
            print("Found", count, "device(s):")
            for device in devices:
                print("Device found at address:", hex(device))

        time.sleep(4)

# Ejecución
setup()
loop()
