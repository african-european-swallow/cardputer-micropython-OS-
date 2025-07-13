from machine import I2C, Pin
from sths34pf80 import STHS34PF80
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(2))
sensor = STHS34PF80(i2c)

while True:
    obj, amb, present, intensity, motion = sensor.read_all()
    print("Obj: %.2f°C | Amb: %.2f°C | Present: %s | Heat: %d | Motion: %d" %
          (obj, amb, present, intensity, motion))
    time.sleep(1)

