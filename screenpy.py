import cardputerlib as c
import time as t
li = True
po = False
c.prinS('1, 2, 3', [0,0],
[255,0,0])
while True:
 if c.pressing(['1']):
  c.set_backlight(not li)
  li = not li
 if c.pressing(['2']):
  c.sleep(not po)
  po = not po
 if c.pressing(['3']):
  c.set_backlight(True)
  c.sleep(False)
  break
 t.sleep(0.2)