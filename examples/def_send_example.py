# Import the TPicoESPC3 class
from TPicoESPC3 import ESPC3

# Initialize the ESPC3
esp = ESPC3()

# Try to obtain the IP address using send
try:
    # Send the AT command to get the IP address
    ip_response = esp.send("AT+CIFSR")
    
    # Process the response
    # The response will typically be in the format +CIFSR:STAIP,"<ip_address>"
    for line in ip_response.split(b"\r\n"):
        if line.startswith(b'+CIFSR:STAIP,"'):
            # Extract and display the IP address
            ip_address = str(line[14:-1], "utf-8")
            print("ESP32C3 IP Address:", ip_address)
except Exception as e:
    print("Error obtaining the IP address:", e)
