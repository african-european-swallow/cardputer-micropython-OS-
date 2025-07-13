from machine import Pin, SoftI2C
import ssd1306

# using default address 0x3C
i2c = SoftI2C(sda=Pin(2), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D)
display.poweroff()     # power off the display, pixels persist in memory
display.poweron()      # power on the display, pixels redrawn
display.contrast(0)    # dim
display.contrast(255)  # bright
display.invert(0)      # display inverted
#display.invert(0)      # display normal
display.text('hi', 10, 10)  # rotate 0 degrees
display.show()         # write the contents of the FrameBuffer to display memory
display.fill(0)
display.fill_rect(0, 0, 32, 32, 1)
display.fill_rect(2, 2, 28, 28, 0)
display.vline(9, 8, 22, 1)
display.vline(16, 2, 22, 1)
display.vline(23, 8, 22, 1)
display.fill_rect(26, 24, 2, 4, 1)
display.text('MicroPython', 40, 0, 1)
display.text('SSD1306', 40, 12, 1)
display.text('OLED 128x64', 40, 24, 1)
display.show()