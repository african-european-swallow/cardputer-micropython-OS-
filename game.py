import cardputerlib as card
from machine import Pin, SPI
import st7789py as st7789
import time
import random
class Enemy:
    def __init__(self, xe, ye):
        self.xe = xe
        self.ye = ye
    def move(self):
        move2 = random.choice(['UP','DOWN','LEFT','RIGHT'])
        if move2 == 'UP' and self.ye < 110:
            self.ye += 10
        elif move2 == 'DOWN' and self.ye > 0:
            self.ye -= 10
        elif move2 == 'LEFT' and self.xe > 0:
            self.xe -= 10
        elif move2 == 'RIGHT' and self.xe < 220:
            self.xe += 10
tft = st7789.ST7789(
    SPI(2, baudrate=40000000, sck=Pin(36), mosi=Pin(35), miso=None),
    135,
    240,
    reset=Pin(33, Pin.OUT),
    cs=Pin(37, Pin.OUT),
    dc=Pin(34, Pin.OUT),
    backlight=Pin(38, Pin.OUT),
    rotation=0,
    color_order=st7789.BGR
)
card.clear()
x = 0
y = 0
colors = [110, 38, 14]
enemys = []
timer = 0
biblw = ['Commit to the Lord whatever you do, and he will establish your plans. Proverbs 16:3',
         'But Jesus beheld them, and said unto them, With men this is impossible; but with God all things are possible. Matthew 19:26',
         'Now no chastening for the present seemeth to be joyous, but grievous: nevertheless afterward it yieldeth the peaceable fruit of righteousness unto them which are exercised thereby. Hebrews 12:11',
         'Wherefore we receiving a kingdom which cannot be moved, let us have grace, whereby we may serve God acceptably with reverence and godly fear. Hebrews 12:28',
         'And God shall wipe away all tears from their eyes; and there shall be no more death, neither sorrow, nor crying, neither shall there be any more pain: for the former things are passed away. Revelations 21:4',
         'Wherefore I also, after I heard of your faith in the Lord Jesus, and love unto all the saints, Cease not to give thanks for you, making mention of you in my prayers; Ephesians 1:15-16']
card.setfont('16x32')
card.setrotation(1)
card.prinS('BIBLE CHASE!', [0,50] , [255,255,255])
time.sleep(2)
n = 10
wrathy = False
card.setrotation(0)
while True:
    if card.pressing(['ESC']):
        break
    timer += 1
    move = ''
    move = card.customdpad('e','a','s','d')
    if move == 'UP' and y < 110:
        y += 10
    elif move == 'DOWN' and y > 0:
        y -= 10
    elif move == 'LEFT' and x > 0:
        x -= 10
    elif move == 'RIGHT' and x < 220:
        x += 10
        
    tft.fill_rect(y, x, 20, 20, st7789.color565(255, 0, 0))
    time.sleep(0.1)
    if timer >= n:
        timer = 0
        enemys.append(Enemy(random.randint(0,220), random.randint(0,110)))
    tft.fill(st7789.color565(0, 0, 0))
    for i in enemys:
        i.move()
        tft.fill_rect(i.ye, i.xe, 20, 20, st7789.color565(colors[0], colors[1], colors[2]))
        if (i.ye <= y + 20 and i.ye >= y) or (y <= i.ye + 20 and y >= i.ye):
            if (i.xe <= x + 20 and i.xe >= x) or (x <= i.xe + 20 and x >= i.xe):
                tft.fill(st7789.color565(0, 0, 0))
                card.setrotation(1)
                if wrathy:
                    card.setfont('16x32')
                    card.prinS('You got hit by THE WRATH OF GOD', [0,0], [255,255,255])
                    time.sleep(2)
                    tft.fill(st7789.color565(0, 0, 0))
                card.setfont('8x8')
                card.prinS(random.choice(biblw), [0,0], [255,255,255])
                time.sleep(4)
                card.waitfor('any', '', [0,0], [0,0,0])
                card.setrotation(0)
                colors = [110, 38, 14]
                timer = 0
                enemys = []
                n = 10                    
    if random.randint(0,1000) == 1:
        n = 0
        cololrs = [136,8,8]
        wrathy = True
        