import cardputerlib as card
import random
import time
def run():
    num = random.randint(0,100)
    card.clear()
    while True:
        gus = card.imput('0-100: ',[0,0],[255,255,255])
        if gus == 'exit':
            break
        try:
            if int(gus) > num:
                card.clear()
                card.prinS('Too high',[0,60],[255,255,255])
                num -= 1
            elif int(gus) < num:
                card.clear()
                card.prinS('Too low ',[0,60],[255,255,255])
                num += 1
            if num > 100 or num < 0:
                card.clear()
                card.prinS('YOU LOOSE!',[0,0],[255,255,255])
                time.sleep(2)
                run()
            if int(gus) == num:
                card.clear()
                card.prinS('YOU WON!',[0,0],[255,255,255])
                time.sleep(2)
                run()
                break
            if gus == '':
                break
        except:
            None
run()