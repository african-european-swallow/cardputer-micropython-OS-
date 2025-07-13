import seesaw
import time

# The pins used by the gamepad: 0 to 11
BUTTON_PINS = list(range(12))

def setup_gamepad():
    seesaw.init()

    # Set all 12 GPIOs as input with pullup
    for pin in BUTTON_PINS:
        seesaw.pin_config(pin, mode=0, pull=1)  # input, pullup

def read_buttons():
    pressed = []
    for pin in BUTTON_PINS:
        val = seesaw._read(0x01, 0x04, 8)
        byte_index = 3 - (pin // 8)
        if pin >= 32:
            byte_index += 4
            pin -= 32
        bit = (val[byte_index] >> (pin % 8)) & 1
        if bit == 0:  # active LOW
            if pin not in [3, 4, 7, 8, 9]:
                pressed.append(pin)
    return pressed

# --- Main loop ---
setup_gamepad()
print("Starting to read gamepad buttons...")

while True:
    pressed = read_buttons()
    print("Pressed buttons:", pressed)
    time.sleep(0.1)
