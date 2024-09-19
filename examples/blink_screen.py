import st7789
from time import sleep
from tft_config import config

tft = config(0)
tft.init()

try:
    while True:
        # Turn off screen
        tft.on()
        sleep(1)
        # Turn on screen
        tft.off()
        sleep(1)
except Exception as e:
    print("Plug in the board, man!", e)
