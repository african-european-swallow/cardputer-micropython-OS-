"""Generic ESP32 with ST7789 240x320 display"""

from machine import Pin, SPI
from lib import st7789py as st7789

TFA = 0
BFA = 0

def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(1, baudrate=31250000, sck=Pin(36), mosi=Pin(35)),
        240,
        135,
        reset=Pin(33, Pin.OUT),
        cs=Pin(37, Pin.OUT),
        dc=Pin(34, Pin.OUT),
        backlight=Pin(38, Pin.OUT),
        rotation=rotation,
        options=options,
        buffer_size=buffer_size)