import cardputerlib as card
import time
card.clear()
def calculate_pi(iterations):
    card.clear()
    pi = 0
    for i in range(iterations):
        pi += ((-1)**i) / (2*i + 1)
        card.prinS(str(pi*4), [0,0], [255,255,255])
    return 4 * pi
card.prinS(f'The final verdict is: {str(calculate_pi(int(card.imput('How many? ', [0,0], [255,255,255]))))}', [0,0], [255,255,255])
time.sleep(2)