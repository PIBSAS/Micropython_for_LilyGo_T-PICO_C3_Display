from machine import Pin
import time
from tft_buttons import Buttons  # Importar la clase Buttons

class OneButton:
    def __init__(self, pin):
        self._pin = pin
        self._click_count = 0
        self._debounce_time = 50  # Tiempo de rebote por defecto
        self._last_debounce_time = 0
        self._click_time = 400 # Tiempo para un clic
        self._last_click_time = 0
        self._double_click_time = 200  # Tiempo para considerar un doble clic
        self._long_press_time = 800  # Tiempo para considerar una presión larga
        self._multi_click_time = 600  # Tiempo para considerar múltiples clics
        self._idle_time = 5000  # Tiempo para considerar el botón inactivo
        self._last_state = self._pin.value()
        self._last_action_time = time.ticks_ms()  # Tiempo del último evento de botón
        self._pressed = False
        self._click_detected = False
        self._long_press_detected = False  # Indica si se detectó una presión larga
        self._long_press_started = False  # Indica si se ha iniciado una presión larga
        self._has_been_active = False
        self._idle_func = None  # Función de callback para inactividad
        
    def setDebounceMs(self, time_ms):
        self._debounce_time = time_ms
    
    def setClickMs(self, time_ms):
        self._click_time = time_ms # Establecer el tiempo para un clic

    def setDoubleClickMs(self, time_ms):
        self._double_click_time = time_ms

    def setLongPressMs(self, time_ms):
        self._long_press_time = time_ms
        
    def setMultiClickMs(self, time_ms):
        self._multi_click_time = time_ms
    
    def setIdleMs(self, time_ms):
        self._idle_time = time_ms  # Establecer el tiempo para inactividad
    
    def attachPress(self, callback):
        self._press_func = callback

    def attachClick(self, callback):
        self._click_func = callback
    
    def attachDoubleClick(self, callback):
        self._double_click_func = callback # Agregar el callback para doble click
    
    def attachMultiClick(self, callback):
        self._multi_click_func = callback # Agregar el callback para múltiples clics
    
    def attachLongPressStart(self, callback):
        self._long_press_start_func = callback
    
    def attachLongPressStop(self, callback):
        self._long_press_stop_func = callback
    
    def attachIdle(self, callback):
        self._idle_func = callback  # Asignar la función de callback para inactividad

    def tick(self):
        current_time = time.ticks_ms()
        current_state = self._pin.value()

        # Comprobar cambio de estado
        if current_state != self._last_state:
            self._last_debounce_time = current_time
            self._last_action_time = current_time  # Actualizar el tiempo del último evento

        # Solo considerar el cambio de estado si ha sido estable por el tiempo de rebote
        if (current_time - self._last_debounce_time) > self._debounce_time:
            if current_state == 0 and not self._pressed:  # Botón presionado
                self._pressed = True
                self._click_count += 1
                self._long_press_detected = False  # Reiniciar detección de presión larga
                self._press_start_time = current_time  # Guardar tiempo de inicio de presión
                
                if hasattr(self, '_press_func') and self._press_func is not None:
                    self._press_func()  # Llamar a la función de callback de presión
            
            elif current_state == 1 and self._pressed:  # Botón liberado
                press_duration = current_time - self._press_start_time  # Duración de la presión
                self._pressed = False

                # Verificar si se detectó presión larga
                if press_duration >= self._long_press_time:
                    if not self._long_press_detected:
                        self._long_press_detected = True
                        if hasattr(self, '_long_press_start_func') and self._long_press_start_func is not None:
                            self._long_press_start_func()  # Llamar al inicio de presión larga
                else:
                    if self._long_press_detected:
                        if hasattr(self, '_long_press_stop_func') and self._long_press_stop_func is not None:
                            self._long_press_stop_func()
                        self._long_press_detected = False

                    # Manejar el tiempo de clic
                    if press_duration <= self._click_time:
                        if hasattr(self, '_click_func') and self._click_func is not None:
                            self._click_func()  # Llamar a la función de callback de clic
                
                # Manejar doble clic
                if self._click_count == 1:  # Si hubo más de un clic
                    if current_time - self._last_click_time <= self._double_click_time:
                        if hasattr(self, '_double_click_func') and self._double_click_func is not None:
                            self._double_click_func()  # Llamar a la función de callback de doble clic
                        self._click_count = 0
                    else:
                        self._click_count = 1
                else:
                    self._click_count = 0  # Resetear conteo de clics si hay más de un clic
                
                self._last_click_time = current_time

            # Manejar múltiples clics
            if self._click_count > 2:
                if hasattr(self, '_multi_click_func') and self._multi_click_func is not None:
                    self._multi_click_func(self._click_count)  # Llamar a la función de callback de múltiples clics
                self._click_count = 0

        # Comprobar si el botón ha sido presionado alguna vez
        if self._pressed or self._click_detected or self._long_press_detected:
            self._has_been_active = True

        # Verificar inactividad
        if self._idle_time > 0 and self._has_been_active:
            if (current_time - self._last_action_time) > self._idle_time:
                if hasattr(self, '_idle_func') and self._idle_func is not None:
                    self._idle_func()  # Llamar a la función de callback de inactividad
                # Reiniciar el estado de inactividad para que el botón responda correctamente después
                self._has_been_active = False
                self._last_action_time = current_time  # Restablecer el tiempo de la última acción para evitar inactividad repetida

        self._last_state = current_state
