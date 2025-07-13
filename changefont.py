import cardputerlib
cardputerlib.setfont('8x8')
cardputerlib.prinS('Hello', [0,0], [0,255,0])
cardputerlib.setfont('16x16')
cardputerlib.prinS('Hello', [0,40], [0,255,0])
cardputerlib.setfont('16x32')
cardputerlib.prinS('Hello', [0,80], [0,255,0])
cardputerlib.waitfor('any', '',[0,0],[0,0,0])
