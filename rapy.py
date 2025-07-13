import cardputerlib as c
import random as r
import time as t
c.clear()
rs = r.randint(0,1000)
for i in range(0,rs):
 c.rect(r.randint(0,240),
 r.randint(0,135),
 r.randint(0,30),
 r.randint(0,30),
 [r.randint(0,255),
 r.randint(0,255),
 r.randint(0,255)],
 fill=True)
t.sleep(2)