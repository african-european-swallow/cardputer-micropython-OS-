import machine
import uos
import sdcard
from machine import Pin
from wavplayer import WavPlayer  # Import WavPlayer for simplified playback
import time
# === SD Card Configuration ===
try:
    spi = machine.SPI(1, baudrate=1000000, sck=machine.Pin(40), muosi=machine.Pin(14), miso=machine.Pin(39))
    cs = machine.Pin(12, machine.Pin.OUT)
    
    sd = sdcard.SDCard(spi, cs)
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")
except:
    print("AUFHHFUH")

# === I2S Pins Configuration ===
SCK_PIN = 41  # Clock Pin
WS_PIN = 43   # Word Select Pin
SD_PIN = 42   # Serial Data Pin
I2S_ID = 1
BUFFER_LENGTH = 8192

# === WavPlayer Setup ===
wp = WavPlayer(
    id=I2S_ID,
    sck_pin=Pin(SCK_PIN),
    ws_pin=Pin(WS_PIN),
    sd_pin=Pin(SD_PIN),
    ibuf=BUFFER_LENGTH,
)

# === Play WAV File ===
try:
    '''wp.play("BabyElephantWalk60.wav", loop=False)
    while wp.isplaying():  # Wait until playback is complete
        pass'''
    wp.play("BabyElephantWalk60.wav", loop=False)
    time.sleep(10)  # play for 10 seconds
    time.sleep(5)  # pause playback for 5 seconds
except Exception as e:
    print("Error:", e)

uos.umount("/sd")
print("Playback complete!")
