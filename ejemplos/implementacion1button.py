import time
import machine
from MP_OneButton import OneButton

# Callback functions
def on_button1_click():
    print("Button 1 clicked!")

def on_button1_double_click():
    print("Button 1 double-clicked!")

def on_button1_long_press():
    print("Button 1 long pressed!")

def on_button2_click():
    print("Button 2 clicked!")

def on_button2_double_click():
    print("Button 2 double-clicked!")

def on_button2_long_press():
    print("Button 2 long pressed!")

# Initialize buttons
button1 = OneButton(6, active_low=True, pullup_active=True)  # Button on GPIO6
button2 = OneButton(7, active_low=True, pullup_active=True)  # Button on GPIO7

# Attach events to button 1
button1.attachClick(on_button1_click)
button1.attachDoubleClick(on_button1_double_click)
button1.attachLongPressStop(on_button1_long_press)

# Attach events to button 2
button2.attachClick(on_button2_click)
button2.attachDoubleClick(on_button2_double_click)
button2.attachLongPressStop(on_button2_long_press)

# Main loop
while True:
    button1.tick()  # Check button 1 status
    button2.tick()  # Check button 2 status
    time.sleep(0.005)  # Small delay to avoid overloading the CPU
