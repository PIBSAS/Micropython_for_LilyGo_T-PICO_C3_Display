import machine
import time

button1 = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    print("Button1:", button1.value(), "Button2:", button2.value())
    time.sleep(0.1)
