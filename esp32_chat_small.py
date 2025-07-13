import cardputerlib as card
import network
from machine import Pin, SPI
import espnow
import time


sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Define the MAC address of the receiving ESP32 (ESP32 B)
peer = b'\xf0\xf5\xbd\x01\xfcT'
esp.add_peer(peer)
while True:
    vard = card.imput('Send:',[0,0],[0,255,0])
    card.prinS(f'Sent: {vard}',[0,100],[0,255,0])
    esp.send(peer, f'[esp]: {str(vard)}')
    time.sleep(2)
    card.clear()
                    
                
        
 
