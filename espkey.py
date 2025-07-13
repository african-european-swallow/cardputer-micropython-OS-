import network
import espnow
import cardkey as kb
import time

# Set up Wi-Fi in station mode
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()  # For ESP8266 compatibility, disconnect if not already

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Set the ATOM U MAC address (replace with the actual MAC address of your ATOM U)
ATOM_U_MAC = b'\x48\xca\x43\x3a\x33\x28'
  # Example: Replace with your ATOM U MAC address

# Add the ATOM U as a peer
esp.add_peer(ATOM_U_MAC)

# Initialize the Cardputer keyboard object
key = kb.KeyBoard()

while True:
    # Get pressed keys from Cardputer
    pressed_keys = key.get_pressed_keys()

    # Iterate through each pressed key
    for es in pressed_keys:
        try:
            # Send each keypress as a byte message over ESP-NOW
            esp.send(ATOM_U_MAC, es.encode('utf-8'))
            print(f"Sent key: {es}")
        except Exception as e:
            print(f"Error sending data: {e}")

    # Short delay before sending again
    time.sleep(0.5)
