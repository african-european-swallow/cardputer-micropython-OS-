from machine import Pin, I2C
import mcp23017
import cardputerlib as card
import time

# Setup I2C and MCP23017
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
mcp = mcp23017.MCP23017(i2c, 0x20)

pin_modes = ["I"] * 16  # "I", "O0", or "O1"
for i in range(16):
    mcp[i].input(pull=1)

cursor = 0

def draw_config():
    card.prinS("Config:", [0, 0], [255, 255, 0])
    for i in range(16):
        col = (i % 8) * 28
        row = 10 if i < 8 else 20
        mode = pin_modes[i]
        color = [255, 255, 255]
        if i == cursor:
            color = [0, 255, 255]
        card.prinS(f"[{mode[-1]}]", [col, row], color)

def draw_status():
    card.prinS("Status:", [0, 35], [255, 255, 0])
    for i in range(16):
        col = (i % 8) * 28
        row = 45 if i < 8 else 55
        mode = pin_modes[i]
        if mode == "I":
            val = mcp[i].value()
            color = [0, 255, 0] if val else [255, 0, 0]
        elif mode == "O1":
            val = 1
            color = [0, 200, 255]
        elif mode == "O0":
            val = 0
            color = [0, 0, 255]
        else:
            val = "-"
            color = [128, 128, 128]
        card.prinS(f" {val} ", [col, row], color)

# Initial draw
card.clear()
draw_config()
draw_status()

last_cursor = -1
last_modes = [""] * 16

while True:
    d = card.dpad()
    updated = False

    if d == "LEFT":
        cursor = (cursor - 1) % 16
        updated = True
    elif d == "RIGHT":
        cursor = (cursor + 1) % 16
        updated = True
    elif d == "UP":
        cursor = (cursor - 8) % 16
        updated = True
    elif d == "DOWN":
        cursor = (cursor + 8) % 16
        updated = True
    elif card.pressing(["a"]):
        current = pin_modes[cursor]
        if current == "I":
            pin_modes[cursor] = "O0"
            mcp[cursor].output(0)
        elif current == "O0":
            pin_modes[cursor] = "O1"
            mcp[cursor].output(1)
        elif current == "O1":
            pin_modes[cursor] = "I"
            mcp[cursor].input(pull=1)
        updated = True
        time.sleep(0.2)
    elif card.pressing(["1"]):
        pin_modes[cursor] = "O1"
        mcp[cursor].output(1)
        updated = True
    elif card.pressing(["0"]):
        pin_modes[cursor] = "O0"
        mcp[cursor].output(0)
        updated = True
    elif card.pressing(["r"]):
        pin_modes[cursor] = "I"
        mcp[cursor].input(pull=1)
        updated = True
    elif card.pressing(['ESC','`','BSPC']):
        break
    if updated:
        draw_config()

    draw_status()
    time.sleep(0.05)



'''from machine import Pin, I2C
import mcp23017
import time

i2c = I2C(scl=Pin(1), sda=Pin(2))
mcp = mcp23017.MCP23017(i2c, 0x20)

# Configure pin 0 as output and pin 1 as input with pull-up
mcp[0].output(0)
mcp[1].input(pull=1)

while True:
    val = mcp[1].value()  # read input pin
    print("Pin 1 input:", val)

    mcp[0].value(not val) # toggle output opposite to input

    time.sleep(0.5)
'''