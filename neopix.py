import neopixel, time, random
from machine import Pin
ledPin = Pin(21)
led = neopixel.NeoPixel(ledPin, 1, bpp=3)
def slide(x,y,z,ox,oy,oz):
    while True:
        if ox > x:
            ox -= 1
        elif ox < x:
            ox += 1
        if oy > y:
            oy -= 1
        elif oy < y:
            oy += 1
        if oz > z:
            oz -= 1
        elif oz < z:
            oz += 1
        led.fill((
        ox,
        oy,
        oz))
    
        led.write()
        time.sleep(0.01)
        if ox == x and oy == y and oz == z:
            return x, y, z
x,y,z = 0,0,0
while True:
    x, y, z = slide(random.randint(0,255),random.randint(0,255),random.randint(0,255),x,y,z)
    time.sleep(0.5)

    