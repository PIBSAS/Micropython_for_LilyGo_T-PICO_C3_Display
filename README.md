# T-Display PICO C3 ESP32 MicroPython



### Install dependencies:

```bash
sudo apt-get update && sudo apt-get install -y gcc-arm-none-eabi libssl-dev python3 python3-pip python3-venv build-essential libffi-dev git pkg-config
```

### Clone the nice work:

```bash
git clone https://github.com/russhughes/st7789_mpy.git
```
### Clone MicroPython:

```bash
git clone --recurse-submodules https://github.com/micropython/micropython.git
```
### Copy ``tft_config.py`` and ``tft_buttons.py`` and fonts:
```bash
cd st7789_mpy
cp "examples/configs/t-picoc3/tft_config.py" $HOME/micropython/ports/rp2/modules/
cp "examples/configs/tdisplay_rp2040/tft_buttons.py" $HOME/micropython/ports/rp2/modules/
cp "examples/chango/*.py" $HOME/micropython/ports/rp2/modules/
cp "fonts/*.py" $HOME/micropython/ports/rp2/modules/
```

Build MicroPython+ST7789:
```bash
cd micropython
make -C mpy-cross
cd ports/rp2
make USER_C_MODULES=../../../st7789_mpy/st7789/micropython.cmake
make submodules
make
```

Note: If make user line fail, change ``../../../`` for the full path, example: ``/home/your_user/st7789_mpy/st7789/micropython.cmake``.

#### The results will be in:
``micropython/ports/rp2/build-RPI_PICO/firmare.uf2``

#### Examples:
Please use the examples located in the [examples folder of the st7789_mpy repository](https://github.com/russhughes/st7789_mpy/tree/master/examples)
