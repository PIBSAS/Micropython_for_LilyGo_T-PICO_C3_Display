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

## How to Flash the Firmware
### Windows, Linux:
          1. Download the .uf2 file from the release.
          2. Press and hold the BOOT button on the RP2040 and press RESET button or connect it to your computer via USB.
          3. Release the button. The RP2040  will appear as a removable drive.
          4. Drag and drop the .uf2 file onto the drive..
          5. The RP2040 will reboot and run MicroPython..

## Examples Usage
Please use the examples located in the [examples folder of the st7789_mpy repository](https://github.com/russhughes/st7789_mpy/tree/master/examples).

#### The results will be in:
``micropython/ports/rp2/build-RPI_PICO/firmare.uf2``

#### Examples:
Please use the examples located in the [examples folder of the st7789_mpy repository](https://github.com/russhughes/st7789_mpy/tree/master/examples)

## Examples in this repo:

1. **Simulating Arduino Firmware Vendor's Code behaviour**:
   - Like the one in ``T-PicoC3\example\factory\pico\firmware\firmware.ino``.
   - Show Connecting message, the IP Address, show Raspberry Pi Logo gradually brightness, then press a button to Scan networks or the other to show Battery Status. Plus blink led and test wifi connection.
2. **I2C_scanner**:
   - Like the one in ``T-PicoC3\example\arduino\I2C_scanner\I2C_Scanner.ino``.
3. **Blink**:
   - Like the one in ``T-PicoC3\example\arduino\blink\blink.ino`` but using the display too.
4. **Blink Screen**:
   - Blink the screen not the LED Built-in.
5. **Button Test**:
   - Only a hardware test with serial output.
6. **Colors**:
   Run all the Constants colors available in ST7789 Driver.
7. **Progressive Brightness**:
   - Turn on the screen slowly till max bright.
8. **Write Screen**:
   - Shows the three ways of present Text on the Screen using ST7789 Driver.
9. **Image**:
    - Push an image in the screen.
10. **Wifi Connect**:
    - Connect to a Wifi given the data, show the IP.
11. **Join AP**:
    - Connect to an AP similar to the previous but using different function.
    - Showing:
      - RSSI:
      - Reconn-interval.
      - BSSID.
      - Channel.
      - Scan mode.
      - Listen interval.
      - PMF.
      - PCI_EN.
      - And finally SSID, all this one line at time.
12. **Get APs**:
    - Scan networks around showing all details given by AT+CWLAP:
      - RSSI: Signal strength.
      - MAC: String parameter showing MAC address of the AP.
      - Channel: Channel.
      - Scan Type: Wi-Fi scan type. Default: 0.
        - 0: active scan.
        - 1: passive scan
      - Min Scan time: The minimum active scan time per channel. Unit: millisecond. Range [0,1500]. If the scan type is passive, this parameter is invalid.
      - Max Scan time: The maximum active scan time per channel. Unit: millisecond. Range [0,1500]. If this parameter is 0, the firmware will use the default time: 120 ms for active scan; 360 ms for passive scan.
      - Pairwise Cipher: Pairwise cipher type.
        - 0: None
        - 1: WEP40
        - 2: WEP104
        - 3: TKIP
        - 4: CCMP
        - 5: TKIP and CCMP
        - 6: AES-CMAC-128
        - 7: Unknown
      - Group Cipher: Group cipher type, same enumerated value to <pairwise_cipher>
      - 802.11 bands: If the corresponding bit is 1, the corresponding mode is enabled; if the corresponding bit is 0, the corresponding mode is disabled.
        - bit 0: bit to identify if 802.11b mode is enabled or not.
        - bit 1: bit to identify if 802.11g mode is enabled or not.
        - bit 2: bit to identify if 802.11n mode is enabled or not
      - WPS: Wps flag.
        - 0: WPS disabled.
        - 1: WPS enabled
      - Security: encryption method.
        - 0: OPEN.
        - 1: WEP.
        - 2: WPA_PSK.
        - 3: WPA2_PSK.
        - 4: WPA_WPA2_PSK.
        - 5: WPA2_ENTERPRISE.
        - 6: WPA3_PSK.
        - 7: WPA2_WPA3_PSK.
        - 8: WAPI_PSK.
        - 9: OWE.
      - Like all details doesn't fit in screen, there is another code with scroll.
13. **Get APs Scroll:**
    - Scan networks around showing all details given by ``AT+CWLAP`` and scroll the data one SSID at time.
14. **Get APs Multiscroll:**
    - Scan networks around showing all details given by ``AT+CWLAP`` and scroll the data all together.

## Docs:
## Get Latest Raspberry Pi Pico-Series C/C++ SDK:
  [![C SDK](/doc/cover/rp2_C_SDK.png)](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-c-sdk.pdf)

## Get Latest Raspberry Pi Pico-Series Python SDK:
  [![Python SDK](/doc/cover/rp2_Python_SDK.png)](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf)

## Get Latest ESP32 C3 Technical Reference Manual CN:
  [![Reference Manual CN](/doc/cover/esp32-c3_technical_reference_manual_cn.png)](https://www.espressif.com/sites/default/files/documentation/esp32-c3_technical_reference_manual_cn.pdf)

## Get Latest ESP32 C3 Technical Reference Manual EN:
  [![Technical Reference Manual EN](/doc/cover/esp32-c3_technical_reference_manual_en.png)](https://www.espressif.com/sites/default/files/documentation/esp32-c3_technical_reference_manual_en.pdf)
  
## ESP32 C3 Wireless Adventure
  [![ESP32 C3 Wireless Adventure](/doc/cover/ESP32_C3_Wireless_Adventure.png)](https://www.espressif.com/sites/default/files/documentation/ESP32-C3%20Wireless%20Adventure.pdf)

## Get Started with Micropython:
  [![Get Started with Micropython](/doc/cover/Started_Guide.png)](https://hackspace.raspberrypi.com/books/micropython-pico)

## MicroPython Documentation:
  [![MicroPython RP2 Doc](/doc/cover/MicroPython_RP2.png)](https://docs.micropython.org/en/latest/rp2/quickref.html)
  [![MicroPython ESP32 Doc](doc/cover/MicroPython_ESP32.png)](https://docs.micropython.org/en/latest/esp32/quickref.html)

## ESP32 C3 AT Doc:
  [![ESP32 C3 AT Doc](/doc/cover/AT.png)](https://docs.espressif.com/projects/esp-at/en/latest/esp32c3/)
