# This file is executed on every boot (including wake-boot from deepsleep)
from cardputerlib import fill, rect, prinS, setfont
import time

def cardos_splash():
    bg = [150, 150, 150]
    fill([0,0,0])

    orange = [255, 140, 0]
    yellow = [255, 255, 0]
    dark_gray = [50, 50, 50]

    rect(5, 5, 230, 125, orange)

    setfont('16x32')
    prinS("Card", [60, 30], bg)
    prinS("OS", [124,30], [255,255,255])

    setfont('8x8')
    prinS('LOADING',[80,80], [0,255,0])
    for i in range(0, 200, 10):
        rect(20 + i, 100, 10, 10, [0, 255, 0], fill=True)
        time.sleep(0.01)

if __name__ == "__main__":
    cardos_splash()


'''import esp
esp.osdebug(None)
import webrepl
webrepl.start()'''
'''import network
import time
import webrepl

# Replace these with your Wi-Fi credentials
SSID = "bunnyzilla"
PASSWORD = "babylon5"

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Connecting to Wi-Fi...")
    wlan.connect(SSID, PASSWORD)
    timeout = 10  # seconds
    for _ in range(timeout * 10):
        if wlan.isconnected():
            break
        time.sleep(0.1)

if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print("Connected. IP:", ip)
else:
    print("Failed to connect to Wi-Fi")

# Start WebREPL
webrepl.start()
'''