from tft_config import config
import vga1_8x16 as font
from time import sleep

tft = config(3)
tft.init()

def main():
    try:
        image = f'RaspberryPi.jpg'  # The image must be in the root of the RP2040; otherwise, specify which folder it's in.
        print(f"Loading {image}")
        tft.jpg(image, 0, 0)

    except Exception as e:
        print("Place the image on the T-PicoC3!:", e)
        tft.text(font, f"Load the image on the T-PicoC3!: {e}", 0, 50)

main()
sleep(10)
tft.off()
