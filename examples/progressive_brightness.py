from machine import PWM, Pin
import time

def progressive_brightness():
    print("Starting progressive brightness configuration...")  # Initial message
    backlight = PWM(Pin(4))  # Set GPIO4 as PWM
    backlight.freq(1000)  # Set the PWM frequency
    print("PWM frequency set to 1000 Hz.")

    for i in range(0,65536,16):  # From 0 to 65535
        backlight.duty_u16(i)  # Set the duty cycle directly
        time.sleep(0.005)
        print(f"Bright: {i}")

    backlight.duty_u16(65535)  # Set brightness to maximum
    print("Max Brightness.")
    
    # Decrease brightness(optional):
    #for i in range(65536,0,-16):  # Counting down from 65535 to 0
    #    backlight.duty_u16(i)  # Set the duty cycle directly
    #    time.sleep(0.005)
    #    print(f"Bright: {i}")

def main():
    progressive_brightness()
    # You can add other commands or loops here

# Call the main function to start the program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program stopped by the user.")