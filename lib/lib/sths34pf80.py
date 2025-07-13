import machine
import time

class STHS34PF80:
    WHO_AM_I_REG = 0x0F
    WHO_AM_I_VAL = 0xD3

    CTRL1_REG = 0x20
    ONE_SHOT_REG = 0x21
    STATUS_REG = 0x23
    FUNC_STATUS_REG = 0x25

    TOBJECT_L_REG = 0x26
    TOBJECT_H_REG = 0x27
    TAMBIENT_L_REG = 0x28
    TAMBIENT_H_REG = 0x29
    PRESENCE_REG = 0x2A
    MOTION_REG = 0x2B

    def __init__(self, i2c, address=0x5A):
        self.i2c = i2c
        self.address = address
        self._initialize_sensor()

    def _write_register(self, register, value):
        self.i2c.writeto_mem(self.address, register, bytes([value]))

    def _read_register(self, register, length=1):
        return self.i2c.readfrom_mem(self.address, register, length)

    def _initialize_sensor(self):
        # ODR = 1Hz (0x03), BDU enabled (0x40) = 0x43
        self._write_register(self.CTRL1_REG, 0x43)

        # Enable presence detection mode: FUNC_CFG_ACCESS + FUNC_CFG registers
        self._write_register(0x70, 0x80)     # Enable embedded functions access
        self._write_register(0x71, 0x01)     # Enable presence detection
        self._write_register(0x70, 0x00)     # Lock back
        time.sleep_ms(100)


    def _wait_for_data_ready(self):
        for _ in range(50):  # max 500ms
            if self._read_register(self.STATUS_REG)[0] & 0x01:
                return True
            time.sleep_ms(10)
        return False

    def trigger_measurement(self):
        self._write_register(self.ONE_SHOT_REG, 0x01)

    def get_object_temperature(self):
        if not self._wait_for_data_ready():
            return None
        lo = self._read_register(self.TOBJECT_L_REG)[0]
        hi = self._read_register(self.TOBJECT_H_REG)[0]
        raw = (hi << 8) | lo
        return raw * 0.01

    def get_ambient_temperature(self):
        if not self._wait_for_data_ready():
            return None
        lo = self._read_register(self.TAMBIENT_L_REG)[0]
        hi = self._read_register(self.TAMBIENT_H_REG)[0]
        raw = (hi << 8) | lo
        return raw * 0.01

    def get_presence_status(self):
        flags = self._read_register(self.FUNC_STATUS_REG)[0]
        return bool(flags & 0x01)

    def get_presence_intensity(self):
        return self._read_register(self.PRESENCE_REG)[0]

    def get_motion_intensity(self):
        return self._read_register(self.MOTION_REG)[0]

    def read_all(self):
        self.trigger_measurement()
        if not self._wait_for_data_ready():
            return None, None, None, None, None
        return (
            self.get_object_temperature(),
            self.get_ambient_temperature(),
            self.get_presence_status(),
            self.get_presence_intensity(),
            self.get_motion_intensity()
        )
