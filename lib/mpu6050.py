import machine
import struct
import time

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')  # Wake up sensor
        time.sleep(0.1)

    def read_raw(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        value = struct.unpack('>h', data)[0]
        return value
    
    def get_accel(self):
        return {
            'x': self.read_raw(0x3B),
            'y': self.read_raw(0x3D),
            'z': self.read_raw(0x3F)
        }
    
    def get_gyro(self):
        return {
            'x': self.read_raw(0x43),
            'y': self.read_raw(0x45),
            'z': self.read_raw(0x47)
        }
