import cardputerlib as card
from random import randint
import sys
if randint(0,1) == 0:
    card.clear()
while True:
    if card.pressing(['BSPC']):
        card.clear()
    elif card.pressing(['any']):
        sys.exit()
    if card.button():
        card.pixel(randint(0,240), randint(0,135), [randint(0,255),randint(0,255),randint(0,255)])