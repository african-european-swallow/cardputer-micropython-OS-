import cardputerlib as card
import mpu6050
import machine
import time
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(2))
mpu = mpu6050.MPU6050(i2c)
def get_tilt():
    accel = mpu.get_accel()
    
    x_tilt = accel['y'] / 16384.0  # Left/Right tilt
    y_tilt = accel['x'] / 16384.0  # Up/Down tilt
    z_tilt = accel['z'] / 16384.0

    dx = int(x_tilt * 120)  # Sensitivity
    dy = int(y_tilt * 60)
    dz = int(z_tilt * 127)

    return dx, dy, dz

while True:
    dx, dy, dz = get_tilt()
    if card.button():
        card.clear()
    card.rect((120-dx)-5, (67-dy)-5,10,10,[dz,dz,dz], fill=True)
    time.sleep(0.1)