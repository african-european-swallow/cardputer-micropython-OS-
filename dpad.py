from cardputerlib import dpad, customdpad
import time
while True:
    print(dpad())
    # dpad returns UP DOWN LEFT or RIGHT
    print(customdpad('e','a','s','d'))
    time.sleep(0.1)