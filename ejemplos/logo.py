from tft_config import config
from time import sleep

tft = config(3)
tft.init()
def main():

    try:
        image = f'RaspberryPi.jpg' # La imagen debe estar en el root del RP2040, caso contrario indicar en cual carpeta esta.
        print(f"Loading {image}")
        tft.jpg(image, 0, 0)

    except Exception as e:
        print("Conecta la pantalla man!:", e)

main()
sleep(10)
tft.off()