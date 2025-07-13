'''

Writes "Hello!" in random colors at random locations on the Display.
https://www.youtube.com/watch?v=atBa0BYPAAc

.. note:: This example requires the following modules:

  .. hlist::
    :columns: 3

    - `st7789py`
    - `tft_config`
    - `vga2_bold_16x32`

'''
from machine import Pin, SPI
import random
import st7789py as st7789
from font import vga2_3x4 as font


def main():
    """
    The big show!
    """
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

    if True:
        for rotation in range(4):
            tft.rotation(rotation)
            tft.fill(0)
            col_max = tft.width - font.WIDTH * 5
            row_max = tft.height - font.HEIGHT
            if col_max < 0 or row_max < 0:
                raise RuntimeError(
                    "This font is too big to display on this screen."
                )

            for _ in range(100):
                tft.text(
                    font,
                    "Hello",
                    random.randint(0, col_max),
                    random.randint(0, row_max),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8),
                    ),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8),
                    ),
                )
            tft.text(
                    font,
                    "a b c d e f g h i j k l m n o p q r s t u v w x y z",
                    random.randint(0, col_max),
                    random.randint(0, row_max),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8),
                    ),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8),
                    ),
                )


main()