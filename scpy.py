import cardputerlib as c
import time as t
import random as r
#c.rect(0,10,100,10,
#[255,255,255],fill=True)
t.sleep(1)
while True:
  if c.button():
    c.rect(r.randint(0,240),
    r.randint(0,135),10,10,
    [r.randint(0,255),
    r.randint(0,255),
    r.randint(0,255)])
  if c.pressing(['any']):
    break
  t.sleep(0.01)