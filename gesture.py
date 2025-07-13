import machine, time, paju2
import cardputerlib as card
# Declaration I2C pour la communication avec le capteur PAJ7620
# GPIO21 --> SDA, GPIO22 --> SCL
i2c = machine.SoftI2C(scl=machine.Pin(1), sda=machine.Pin(2))
time.sleep(0.1)
g = paju2.PAJ7620(i2c = i2c)
while True:
    geste = g.gesture()
    # geste peut contenir les valeurs suivantes
    # 0 : nothing
    # 1 : Forward
    # 2 : Backward
    # 3 : Right
    # 4 : Left
    # 5 : Up
    # 6 : Down
    # 7 : Clockwise
    # 8 : anti-clockwise
    # 9 : wave
    if geste != 0:
        card.clear()
    if geste == 1: 
        card.prinS("Down", [100,70], [0,255,0])
    elif geste == 2:
        card.prinS("Up", [100,70], [0,255,0])
    elif geste == 3:
        card.prinS("Left", [100,70], [0,255,0])
    elif geste == 4:
        card.prinS("Right", [100,70], [0,255,0])
    elif geste == 5:
        card.prinS("Back", [100,70], [0,255,0])
    elif geste == 6:
        card.prinS("Front", [100,70], [0,255,0])
    elif geste == 7:
        card.prinS("Clockwize", [100,70], [0,255,0])
    elif geste == 8:
        card.prinS("Counter Colckwize", [100,70], [0,255,0])
    elif geste == 9:
        card.prinS("Wave", [100,70], [0,255,0])
    time.sleep(.5)