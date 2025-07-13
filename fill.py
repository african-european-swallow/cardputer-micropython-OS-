from cardputerlib import prinS, imput, waitfor, setfont
setfont('3x4')
prinS(imput('fill:', [50, 20], [0,255,0])*int(imput('How many? ', [50,30], [0,255,0])), [0,0], [0,255,0])
waitfor('any','',[0,0],[0,0,0])