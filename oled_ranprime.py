from machine import Pin, SoftI2C
import ssd1306, time, random
from oledlib import printS
i2c = SoftI2C(sda=Pin(2), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D)

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_random_prime(start, end):
    """Get a random prime number within a range."""
    primes = [n for n in range(start, end + 1) if is_prime(n)]
    return random.choice(primes) if primes else None

while True:
    display.fill_rect(0,0,128,64, 1)
    display.fill_rect(1,1,126,62, 0)
    display.text(str(get_random_prime(0, 10000)), 5, 32)
    display.show()
    time.sleep(1)
