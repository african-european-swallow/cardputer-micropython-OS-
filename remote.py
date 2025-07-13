import network
import espnow
import time
import cardputerlib as card
import sys
# Enable Wi-Fi station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Replace with the receiver's MAC address
peer_mac = b'`U\xf9\xda\xbb\xf2'  # Use actual MAC address from Step 3
e.add_peer(peer_mac)

# Send a message
card.clear()
card.prinS('Remote for Esp-Car!', [0,0],[0,255,0])
card.prinS('Arrows to move the car, and esc to exit to home menu.', [0,10], [0,255,0])
while True:
    if card.pressing(['`','~','ESC']):
        e.active(False)
        wlan.active(False)
        sys.exit()
    msg = card.dpad()
    if msg == None:
        msg = 'none'
    e.send(peer_mac, msg)
    time.sleep(0.1)