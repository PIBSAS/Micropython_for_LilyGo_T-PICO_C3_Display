from machine import PWM, Pin
import time

def set_brightness():
    print("Iniciando la configuración del brillo...")  # Mensaje inicial
    backlight = PWM(Pin(4))  # Configura GPIO4 como PWM
    backlight.freq(1000)  # Establece la frecuencia PWM
    print("Frecuencia PWM establecida a 1000 Hz.")

    for i in range(0,65536,16):  # Del 0 al 65535
        backlight.duty_u16(i)  # Establece el ciclo de trabajo directamente
        time.sleep(0.005)
        print(f"Brillo actual: {i}")

    backlight.duty_u16(65535)  # Establecer el brillo al máximo
    print("Brillo establecido al máximo.")


def main():
    set_brightness()
    # Aquí puedes agregar otros comandos o ciclos

# Llamar a la función principal para iniciar el programa
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")