import cardputerlib as card
from machine import Pin, SPI
import st7789py as st7789
import time
import random


#lookup values for our keyboard
kc_shift = const(61)
kc_fn = const(65)

keymap = {
    67:'`',  63:'1',  57:'2',  53:'3', 47:'4', 43:'5', 37:'6', 33:'7', 27:'8', 23:'9', 17:'0', 13:'_', 7:'=', 3:'B!S!P!C!',
    
    66:'TAB',62:'q',  56:'w',  52:'e', 46:'r', 42:'t', 36:'y', 32:'u', 26:'i', 22:'o', 16:'p', 12:'[', 6:']', 2:'\\',
    
                      55:'a',  51:'s', 45:'d', 41:'f', 35:'g', 31:'h', 25:'j', 21:'k', 15:'l', 11:';', 5:"'", 1:'E!N!T!',
    
    64:'CTL',60:'OPT',54:'ALT',50:'z', 44:'x', 40:'c', 34:'v', 30:'b', 24:'n', 20:'m', 14:',', 10:'.', 4:'/', 0:' ',
    }

keymap_shift = {
    67:'~',  63:'!',  57:'@',  53:'#', 47:'$', 43:'%', 37:'^', 33:'&', 27:'*', 23:'(', 17:')', 13:'-', 7:'+', 3:'B!S!P!C!',
    
    66:'TAB',62:'Q',  56:'W',  52:'E', 46:'R', 42:'T', 36:'Y', 32:'U', 26:'I', 22:'O', 16:'P', 12:'{', 6:'}', 2:'|',
    
                      55:'A',  51:'S', 45:'D', 41:'F', 35:'G', 31:'H', 25:'J', 21:'K', 15:'L', 11:':', 5:'"', 1:'E!N!T!',
    
    64:'CTL',60:'OPT',54:'ALT',50:'Z', 44:'X', 40:'C', 34:'V', 30:'B', 24:'N', 20:'M', 14:'<', 10:'>', 4:'?', 0:' ',
    }

keymap_fn = {
    67:'ESC',63:'F1', 57:'F2', 53:'F3',47:'F4',43:'F5',37:'F6',33:'F7',27:'F8',23:'F9',17:'F10',13:'_',7:'=', 3:'DEL',
    
    66:'TAB',62:'q',  56:'w',  52:'e', 46:'r', 42:'t', 36:'y', 32:'u', 26:'i', 22:'o', 16:'p', 12:'[', 6:']', 2:'\\',
    
                      55:'a',  51:'s', 45:'d', 41:'f', 35:'g', 31:'h', 25:'j', 21:'k', 15:'l', 11:'UP',5:"'", 1:'E!N!T!',
    
    64:'CTL',60:'OPT',54:'ALT',50:'z', 44:'x', 40:'c', 34:'v', 30:'b', 24:'n',20:'m',14:'LEFT',10:'DOWN',4:'RIGHT',0:' ',
    }


class KeyBoard():
    def __init__(self):
        self._key_list_buffer = []
        
        #setup column pins. These are read as inputs.
        c0 = Pin(13, Pin.IN, Pin.PULL_UP)
        c1 = Pin(15, Pin.IN, Pin.PULL_UP)
        c2 = Pin(3, Pin.IN, Pin.PULL_UP)
        c3 = Pin(4, Pin.IN, Pin.PULL_UP)
        c4 = Pin(5, Pin.IN, Pin.PULL_UP)
        c5 = Pin(6, Pin.IN, Pin.PULL_UP)
        c6 = Pin(7, Pin.IN, Pin.PULL_UP)
        
        #setup row pins. These are given to a 74hc138 "demultiplexer", which lets us turn 3 output pins into 8 outputs (8 rows) 
        a0 = Pin(8, Pin.OUT)
        a1 = Pin(9, Pin.OUT)
        a2 = Pin(11, Pin.OUT)
        
        self.pinMap = {
            'C0': c0,
            'C1': c1,
            'C2': c2,
            'C3': c3,
            'C4': c4,
            'C5': c5,
            'C6': c6,
            'A0': a0,
            'A1': a1,
            'A2': a2,
        }
        
        self.key_state = []
        
        
    def scan(self):
        """scan through the matrix to see what keys are pressed."""
        
        self._key_list_buffer = []
        
        #this for loop iterates through the 8 rows of our matrix
        for row in range(0,8):
            self.pinMap['A0'].value(row & 0b001)
            self.pinMap['A1'].value( ( row & 0b010 ) >> 1)
            self.pinMap['A2'].value( ( row & 0b100 ) >> 2)
        
        
            #iterate through each column
            columns = []
            for i, col in enumerate(['C6', 'C5', 'C4', 'C3', 'C2', 'C1', 'C0']):
                val = self.pinMap[col].value()
                
                if not val: # button pressed
                    key_address = (i * 10) + row
                    self._key_list_buffer.append(key_address)
                
        return self._key_list_buffer                
                
                
    def get_pressed_keys(self):
        """Get a readable list of currE!N!T!ly held keys."""
        
        #update our scan results
        self.scan()
        
        self.key_state = []
        
        if not self._key_list_buffer: # if nothing is pressed, we can return an empty list
            return self.key_state
        
        
        
        if kc_fn in self._key_list_buffer:
            
            #remove modifier keys which are already accounted for
            self._key_list_buffer.remove(kc_fn)
            if kc_shift in self._key_list_buffer:
                self._key_list_buffer.remove(kc_shift)
                
            for keycode in self._key_list_buffer:
                self.key_state.append(keymap_fn[keycode])
                
        elif kc_shift in self._key_list_buffer:
            
            #remove modifier keys which are already accounted for
            self._key_list_buffer.remove(kc_shift)
            
            for keycode in self._key_list_buffer:
                self.key_state.append(keymap_shift[keycode])
        
        else:
            for keycode in self._key_list_buffer:
                self.key_state.append(keymap[keycode])
        
        return self.key_state
            
        
        
class Square:
    def __init__(self, xe, ye):
        self.xe = xe
        self.ye = ye
        self.ymove = True
        self.xmove = True
    def move(self):
        global points, boxadd
        move2 = random.choice(['UP','DOWN','LEFT','RIGHT'])
        if move2 == 'UP' and self.ye < 120:
            self.ye += boxmove
        elif move2 == 'DOWN' and self.ye > 0:
            self.ye -= boxmove
        elif move2 == 'LEFT' and self.xe > 0:
            self.xe -= boxmove
        elif move2 == 'RIGHT' and self.xe < 230:
            self.xe += boxmove
            
        if self.xmove:
            self.xe += boxmove
        else:
            self.xe -= boxmove
        if self.xe >= 230:
            points += boxadd
            self.xe = 230
            self.xmove = False
        if self.xe <= 0:
            points += boxadd
            self.xe = 0
            self.xmove = True
        
        if self.ymove:
            self.ye += boxmove
        else:
            self.ye -= boxmove
        if self.ye >= 120:
            points += boxadd
            self.ye = 120
            self.ymove = False
        if self.ye <= 0:
            points += boxadd
            self.ye = 0
            self.ymove = True
        if (self.ye <= 10  or self.ye + 10 >= 110) and (self.xe <= 10 or self.xe + 10 >= 220):
            points += boxadd * 4
ttf = st7789.ST7789(
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
kb = KeyBoard()
card.setrotation(1)
points = 0
boxadd = 1
upclick = 1
squares = []
upsquare = 5
display_squares = True
boxmove = 2
upboxmove = 4
upboxre = 3
addpoints = 1

def settings():
    global display_squares
    while True:
        card.clear()
        card.setfont('8x8')
        card.prinS(f'1: Display Squares: {display_squares}', [0,10], [0,255,0])
        time.sleep(0.25)
        inp = card.imput("(Setting num) (true/false(to change))or'exit':", [0,110], [0,255,0])
        inpu = inp.split(' ')
        if len(inpu) == 2:
            if inpu[0] == '1':
                display_squares = True if inpu[1] == 'true' else False 
        if inp == 'exit':
            game()
            
def shop():
    global points, addpoints, upclick, upsquare, squares, upboxmove, boxadd, upboxre, boxmove
    shopinfo = {'Upgrade Click' : int(1.5*upclick), 'Add Bouncing Square' : int(2*upsquare), 'Upgrade Square Movement' : int(1.5*upboxmove), 'Upgrade Square Reward' : int(2*upboxre)}
    while True:
        card.clear()
        card.setfont('8x8')
        card.prinS('1: Upgrade Click, Price: ' + str(int(1.5*upclick)) + '\\n' + '2: Add Bouncing Square, Price: ' + str(int(2*upsquare)) + '\\n3: Upgrade Square Movement, Price: ' + str(int(1.5*upboxmove)) + '\\n4: Upgrade Square Reward, Price: ' + str(int(2*upboxre)), [0,10], [0,255,0])
        time.sleep(0.25)
        card.prinS('Points: ' + str(points), [0,112], [0,255,0])
        inp = card.imput("Shop num or 'exit':", [0,120], [0,255,0])
        if inp == '1':
            if points >= int(1.5*upclick):
                points -= int(1.5*upclick)
                upclick *= 1.5
                addpoints += 1
                card.clear()
                card.prinS('Bought one "Upgrade Click"', [0,67], [0,255,0])
                time.sleep(0.5)
            else:
                card.clear()
                card.prinS('You do not have enough points!', [0,67], [0,255,0])
                time.sleep(1)
        if inp == '2':
            if points >= int(2*upsquare):
                points -= int(2*upsquare)
                upsquare *= 2
                squares.append(Square(random.randint(0,220), random.randint(0,110)))
                card.clear()
                card.prinS('Bought one "Add Bouncing Square"', [0,67], [0,255,0])
                time.sleep(0.5)
            else:
                card.clear()
                card.prinS('You do not have enough points!', [0,67], [0,255,0])
                time.sleep(1)
        if inp == '3':
            if points >= int(1.5*upboxmove):
                points -= int(1.5*upboxmove)
                upboxmove *= 1.5
                boxmove += 2
                card.clear()
                card.prinS('Bought one "Upgrade Square Movement"', [0,67], [0,255,0])
                time.sleep(0.5)
            else:
                card.clear()
                card.prinS('You do not have enough points!', [0,67], [0,255,0])
                time.sleep(1)
        if inp == '4':
            if points >= int(2*upboxre):
                points -= int(2*upboxre)
                upboxre *= 2
                boxadd += 1
                card.clear()
                card.prinS('Bought one "Upgrade Square Reward"', [0,67], [0,255,0])
                time.sleep(0.5)
            else:
                card.clear()
                card.prinS('You do not have enough points!', [0,67], [0,255,0])
                time.sleep(1)
        if inp == 'exit':
            game()
        
def game():
    global points, addpoints
    card.setfont('16x32')
    card.clear()
    card.prinS(str(points), [0,50], [0,255,0])
    old_keys = []
    usedk = []
    while True:
        card.clear()
        ttf.rotation(0)
        for i in squares:
            i.move()
            if display_squares:
                ttf.rect(i.ye, i.xe, 10, 10, st7789.color565(0, 100, 180))
        ttf.rotation(1)
        card.prinS(str(points), [0,50], [0,255,0])
        keys = kb.get_pressed_keys()
        if keys != old_keys:
            if len(keys) >0:
                for i in keys:
                    if str(i) == 'u' and i not in usedk:
                        usedk.append(str(i))
                        points += addpoints
                        card.clear()
                        card.prinS(str(points), [0,50], [0,255,0])
                    if str(i) == 's':
                        shop()
                    if str(i) == "`":
                        settings()
            usedkc = usedk
            for e in usedkc:
                if e not in keys:
                    usedk.remove(e)
            old_keys = keys
        time.sleep(0.01)
game()