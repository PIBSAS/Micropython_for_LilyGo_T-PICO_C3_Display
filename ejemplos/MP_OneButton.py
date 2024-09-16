import machine
import time

class OneButton:
    def __init__(self, pin, active_low=True, pullup_active=True):
        self._pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP if pullup_active else machine.Pin.PULL_DOWN)
        self._active_low = active_low
        self._debounce_ms = 50
        self._click_ms = 400
        self._press_ms = 800
        self._multi_click_ms = 600  # Time window for multi-clicks
        self._state = "INIT"
        self._last_debounce_time = 0
        self._last_press_time = 0
        self._click_count = 0
        self._long_press_detected = False
        self._last_click_time = 0
        
        self._press_func = None
        self._click_func = None
        self._double_click_func = None
        self._multi_click_func = None
        self._long_press_start_func = None
        self._long_press_stop_func = None

    # Setters for timing parameters
    def setDebounceMs(self, ms):
        self._debounce_ms = ms

    def setClickMs(self, ms):
        self._click_ms = ms

    def setPressMs(self, ms):
        self._press_ms = ms

    def setMultiClickMs(self, ms):
        self._multi_click_ms = ms

    # Attach event functions
    def attachPress(self, callback):
        self._press_func = callback

    def attachClick(self, callback):
        self._click_func = callback

    def attachDoubleClick(self, callback):
        self._double_click_func = callback

    def attachMultiClick(self, callback):
        self._multi_click_func = callback

    def attachLongPressStart(self, callback):
        self._long_press_start_func = callback

    def attachLongPressStop(self, callback):
        self._long_press_stop_func = callback

    # Main function to detect button events
    def tick(self):
        current_time = time.ticks_ms()
        reading = self._pin.value()
        if self._active_low:
            reading = not reading

        #print(f"Pin {self._pin} state: {reading}")

        # Handle debounce
        if reading != self._last_press_time:
            self._last_debounce_time = current_time

        if (current_time - self._last_debounce_time) > self._debounce_ms:
            # Button is pressed
            if reading == 1 and self._state == "INIT":
                self._state = "PRESS"
                self._last_press_time = current_time
                if self._press_func:
                    print("Button pressed.")  # Debug message
                    self._press_func()
            
            # Button is released
            elif reading == 0 and self._state == "PRESS":
                press_duration = current_time - self._last_press_time
                if press_duration > self._press_ms:
                    # Long press detected
                    if self._long_press_stop_func:
                        print("Long press detected.")  # Debug message
                        self._long_press_stop_func()
                elif press_duration > self._click_ms:
                    # Single click detected
                    self._click_count += 1
                    self._last_click_time = current_time
                    self._state = "CLICK"  # Enter click state to check for double/multi-click
                    print("Single click detected.")  # Debug message
                else:
                    self._state = "INIT"

            # Check for multi-clicks
            if self._state == "CLICK":
                if (current_time - self._last_click_time) > self._multi_click_ms:
                    # Determine the number of clicks
                    if self._click_count == 1:
                        if self._click_func:
                            print("Calling click function.")  # Debug message
                            self._click_func()
                    elif self._click_count == 2:
                        if self._double_click_func:
                            print("Calling double click function.")  # Debug message
                            self._double_click_func()
                    elif self._click_count > 2:
                        if self._multi_click_func:
                            print("Calling multi click function.")  # Debug message
                            self._multi_click_func()

                    # Reset state
                    self._click_count = 0
                    self._state = "INIT"
