from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
SLAVE_ADDR = 0x42

def write_number_16bit(value):
    low = value & 0xFF
    high = (value >> 8) & 0xFF
    i2c.writeto(SLAVE_ADDR, bytes([low, high]))

def read_number_16bit():
    data = i2c.readfrom(SLAVE_ADDR, 2)
    if len(data) == 2:
        return data[0] | (data[1] << 8)
    return None

def write_string(text):
    b = text.encode('utf-8')
    # Send in chunks if needed (max ~32 bytes per I2C message)
    i2c.writeto(SLAVE_ADDR, b)

counter = 0
while True:
    # Send 16-bit number
    write_number_16bit(counter)
    time.sleep_ms(20)
    
    # Read 16-bit number back from slave
    val = read_number_16bit()
    if val is not None:
        print("Read number from slave:", val)
    
    # Every 10 counts send a string
    if counter % 10 == 0:
        s = "Hello this is a test of wits and endurance where you will fail HAHAHAHAHAHAHHA {}".format(counter)
        print("Sending string:", s)
        write_string(s)
    
    counter = (counter + 1) % 65536
    time.sleep(0.1)
