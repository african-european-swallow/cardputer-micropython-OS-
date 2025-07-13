from math import pi
from machine import Pin, SPI
import st7789py as st7789
import random
import time

tft = st7789.ST7789(
    SPI(2, baudrate=40000000, sck=Pin(36), mosi=Pin(35), miso=None),
    135,
    240,
    reset=Pin(33, Pin.OUT),
    cs=Pin(37, Pin.OUT),
    dc=Pin(34, Pin.OUT),
    backlight=Pin(38, Pin.OUT),
    rotation=0,
    color_order=st7789.BGR
    )
def r(num):
    if num:
        return random.randint(0,240)
    else:
        return random.randint(0,135)
# Define the points of the polygon (e.g., triangle)
while True:
    tft.fill(st7789.color565(0, 0, 0))
    polygon_points = []
    for i in range(random.randint(3,1000)):
        polygon_points.append((r(False), r(True)))
        print(i)

# Set color in 565 format (e.g., Green)
    color = st7789.color565(random.randint(0,255), random.randint(0,255), random.randint(0,255))

# Position of the polygon (screen offset)
    x_offset = 0
    y_offset=0
    rotation_angle = 0  # 45 degrees in radians

# Draw the polygon with rotation and positioning
    tft.polygon(polygon_points, x_offset, y_offset, color, angle=rotation_angle)

    time.sleep(0.5)