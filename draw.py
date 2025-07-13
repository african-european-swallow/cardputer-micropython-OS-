import cardputerlib as card
import mpu6050
import machine
import time
pin = [0,0,0]
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(2))
mpu = mpu6050.MPU6050(i2c)
card.initbuff()
def get_tilt():
    accel = mpu.get_accel()
    
    x_tilt = accel['y'] / 16384.0  # Left/Right tilt
    y_tilt = accel['x'] / 16384.0  # Up/Down tilt
    z_tilt = accel['z'] / 16384.0

    dx = int(x_tilt * 120)  # Sensitivity
    dy = int(y_tilt * 60)
    dz = int(z_tilt * 127)

    return dx, dy, dz
def get_inverse(liss):
    return [255-liss[0],255-liss[1],255-liss[2]]
card.clear()
color = 'white'
colors = ['black', 'blue', 'gray', 'red', 'green', 'white', 'purple', 'orange', 'yellow', 'pink']
colorsdix = {'black':[0,0,0], 'blue': [0,0,255], 'gray':[128,128,128], 'red':[255,0,0],'green':[0,255,0], 'white':[255,255,255],
          'purple':[76,0,153], 'orange':[255,128,0], 'yellow': [255,255,0], 'pink':[255,102,255]}
dx, dy, dz = get_tilt()
dx = max(-120, min(dx, 238))  # 238 = 240 - 2 to avoid +1 access
dy = max(-70, min(dy, 133))
while True:
    if card.pressing(['ESC']):
        break
    for i, key in enumerate(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']):
        if card.pressing([key]):
            color = colors[i]
            break
    card.prinS(color, [0,0], colorsdix[color])
    oldx = dx
    oldy = dy
    dx, dy, dz = get_tilt()
    dx = max(-118, min(dx, 238))  # 238 = 240 - 2 to avoid +1 access
    dy = max(-60, min(dy, 60))
    if card.pressing(['BSPC']):
        card.fbclear()
    if card.button():
        card.fbrect((120-dx)-5, (60-dy)-5,10,10,colorsdix[color], fill=True)
    else:
        time.sleep(0.01)
    olpin = [p[:] if isinstance(p, list) else [0, 0, 0] for p in pin]
    try:
        card.fbpixel(120-oldx,60-oldy, [olpin[0][0],olpin[0][1],olpin[0][2]])
    except:
        None
    pin = [card.fbfind(120-dx,60-dy)]
    #print(pin)
    print(dx,dy)
    try:
        card.fbpixel(120-dx,60-dy, [255-pin[0][0],255-pin[0][1],255-pin[0][2]])
    except:
        None
    card.fbdraw(0,0)