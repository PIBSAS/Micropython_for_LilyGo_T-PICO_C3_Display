import st7789
from time import sleep
from tft_config import config

tft = config(0)
tft.init()

try:
    while True:
        # Apagar pantalla
        tft.on()
        sleep(1)
        # Encender pantalla
        tft.off()
        sleep(1)
except Exception as e:
    print("Enchufa la placa man!", e)