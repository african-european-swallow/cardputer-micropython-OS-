#Features!
#prinS (string, cord(in []), color(in []), end=(wher you want to end), outline=(a color other than black!))
#imput (string to print, cord(in []), color(in []), end=(wher you want to end), outline=(a color other than black!))
#setrotation (rotation from 0 to 3) 1 is normal.
#waitfor (what to wait for(any kebord button on the cardputer) (or 'any'), string, cord(in []), color (in []), outline=(a color other than black!))
#clear just clears! ()
#fill ([r,g,b]) fills screen with color
#dot (or pixel) ([x,y], rgb=[r,g,b]) stes a dot at set positon to set color
#line (the line thigns) IDK 
#rect (the rect things!) IDK
#setfont (8x8(for 8x8 font) or 16x32(for 16x32 font) or 16x16(for 16x16 font)) starts with 8x8 font if not used
#dpad, () returns 'UP', 'DOWN', 'LEFT', or 'RIGHT' depending on if any key is pressed
#customdpad, ('key(for up)','key(for left)', 'key(for down)', 'key(for right')) returns 'UP', 'DOWN', 'LEFT', or 'RIGHT' depending on if any key is pressed
#scroll_text, (string, color(in []), speed=(NUM), direction=(left or right))
#pressing (['names of keys' or 'any']) returns True if at least one of the keys in the list are pressed if none returns False
#sleep (True(on) or False(off)) backlight is still on tho
#set_backlight (True(on) or False(off))
#button () returns True if top button is pressed else False
from machine import Pin, SPI
import st7789py as st7789
import time
from font import vga2_8x8 as font
import framebuf
from array import array
fontty = '8x8'
ppin = Pin(0, Pin.IN, Pin.PULL_DOWN)
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


tft.rotation(1)
rotot = 1
#lookup values for our keyboard
kc_shift = const(61)
kc_fn = const(65)

keymap = {
    67:'`',  63:'1',  57:'2',  53:'3', 47:'4', 43:'5', 37:'6', 33:'7', 27:'8', 23:'9', 17:'0', 13:'_', 7:'=', 3:'BSPC',
    
    66:'TAB',62:'q',  56:'w',  52:'e', 46:'r', 42:'t', 36:'y', 32:'u', 26:'i', 22:'o', 16:'p', 12:'[', 6:']', 2:'\\',
    
                      55:'a',  51:'s', 45:'d', 41:'f', 35:'g', 31:'h', 25:'j', 21:'k', 15:'l', 11:';', 5:"'", 1:'ENT',
    
    64:'CTL',60:'OPT',54:'ALT',50:'z', 44:'x', 40:'c', 34:'v', 30:'b', 24:'n', 20:'m', 14:',', 10:'.', 4:'/', 0:' ',
    }

keymap_shift = {
    67:'~',  63:'!',  57:'@',  53:'#', 47:'$', 43:'%', 37:'^', 33:'&', 27:'*', 23:'(', 17:')', 13:'-', 7:'+', 3:'BSPC',
    
    66:'TAB',62:'Q',  56:'W',  52:'E', 46:'R', 42:'T', 36:'Y', 32:'U', 26:'I', 22:'O', 16:'P', 12:'{', 6:'}', 2:'|',
    
                      55:'A',  51:'S', 45:'D', 41:'F', 35:'G', 31:'H', 25:'J', 21:'K', 15:'L', 11:':', 5:'"', 1:'ENT',
    
    64:'CTL',60:'OPT',54:'ALT',50:'Z', 44:'X', 40:'C', 34:'V', 30:'B', 24:'N', 20:'M', 14:'<', 10:'>', 4:'?', 0:' ',
    }

keymap_fn = {
    67:'ESC',63:'F1', 57:'F2', 53:'F3',47:'F4',43:'F5',37:'F6',33:'F7',27:'F8',23:'F9',17:'F10',13:'_',7:'=', 3:'DEL',
    
    66:'TAB',62:'q',  56:'w',  52:'e', 46:'r', 42:'t', 36:'y', 32:'u', 26:'i', 22:'o', 16:'p', 12:'[', 6:']', 2:'\\',
    
                      55:'a',  51:'s', 45:'d', 41:'f', 35:'g', 31:'h', 25:'j', 21:'k', 15:'l', 11:'UP',5:"'", 1:'ENT',
    
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
        """Get a readable list of currENTly held keys."""
        
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

def setrotation(rotation):
    global rotot
    tft.rotation(rotation)
    rotot = rotation

def prinS(string, cord, color, end='normal', outline=[]):
    global rotot, fontty
    loopstr = list(str(string))  # Convert string to a list of characters
    whole = []
    
    # Determine screen width limit for wrapping
    if not isinstance(end, int):
        num1 = 240 if rotot % 2 != 0 else 135
    else:
        num1 = end
    
    # Choose font width and vertical spacing
    if fontty == '3x4':
        font_width = 3
        shiftam = 5
    elif fontty == '8x8':
        font_width = 8
        shiftam = 10
    elif fontty == '16x32':
        font_width = 16
        shiftam = 30
    elif fontty == '16x16':
        font_width = 16
        shiftam = 15
    else:
        font_width = 8
        shiftam = 10

    # Break string into lines
    while len(loopstr) > 0:
        counter = 0
        partal = []
        while counter < int(((num1 - cord[0]) / font_width) - 1) and len(loopstr) > 0:
            if len(loopstr) >= 2 and loopstr[0] == '\\' and loopstr[1] == 'n':
                loopstr.pop(0)
                loopstr.pop(0)
                break
            partal.append(loopstr.pop(0))
            counter += 1
        whole.append(''.join(partal))

    # Display each line
    if len(outline) != 3:
        outline = [0, 0, 0]

    fg = st7789.color565(color[0], color[1], color[2])
    bg = st7789.color565(outline[0], outline[1], outline[2])
    shifter = 0
    for e in whole:
        tft.text(font, e, cord[0], cord[1] + shifter, fg, bg)
        shifter += shiftam

def setfont(num):
    global fontty, font
    if str(num) == '8x8':
        fontty = '8x8'
        from font import vga2_8x8 as font
    elif str(num) == '16x32':
        from font import vga2_16x32 as font
        fontty = '16x32'
    elif str(num) == '16x16':
        from font import vga2_16x16 as font
        fontty = '16x16'
    elif str(num) == '3x4':
        from font import vga2_3x4 as font
        fontty = '3x4'
    else:
        print('font size not recognized!')
        fontty = '8x8'
        from font import vga2_8x8 as font
def imput(say, cord, color, end='normal', outline=[]):
    kb = KeyBoard()
    prinS(str(say), cord, color, end=end, outline=outline)
    old_keys = []
    inputkb = []
    usedk = []
    enter = False
    while True:
        keys = kb.get_pressed_keys()
        if keys != old_keys:
            if len(keys) >0:
                for i in keys:
                    if str(i) == 'ENT':
                        enter = True
                    elif str(i) == 'BSPC':
                        if len(inputkb) > 0:
                            prinS(' '*int(len(inputkb)) + ' '* int(len(list(say))), cord, color, end=end, outline=outline)
                            inputkb.pop(-1)
                    elif str(i) == 'TAB':
                        for i in range(4):
                            inputkb.append(' ')
                        usedk.append(str(i))
                    elif str(i) == 'ESC':
                        return ' '
                    elif str(i) == 'DOWN' or str(i) == 'UP' or str(i) == 'LEFT' or str(i) == 'RIGHT':
                        None
                    elif i != '' and i not in usedk:
                        inputkb.append(str(i))
                        usedk.append(str(i))
            usedkc = usedk
            for e in usedkc:
                if e not in keys:
                    usedk.remove(e)
            if enter:
                time.sleep(0.25)
                return str(''.join(inputkb)) 
            else:
                prinS(str(str(say) + ''.join(inputkb)), cord, color, end=end, outline=outline)
            old_keys = keys
def waitfor(what, say, cord, color, end='normal', outline=[]):
    kb = KeyBoard()
    old_keys = []
    prinS(str(say), cord, color, end=end, outline=outline)
    while True:
        keys = kb.get_pressed_keys()
        if keys != old_keys:
            for i in keys:
                if what == 'any':
                    time.sleep(0.25)
                    return i
                elif i == what:
                    time.sleep(0.25)
                    return i
        old_keys = keys
        
def clear():
    tft.fill(0)
def fill(color):
    tft.fill(st7789.color565(color[0], color[1], color[2]))
def dot(pos, rgb=[255,255,255]):
    tft.pixel(pos[0], pos[1], st7789.color565(rgb[0], rgb[1], rgb[2]))
def dpad():
    kb = KeyBoard()
    old_keys = []
    xx = 0
    while True: 
        keys = kb.get_pressed_keys()
        if keys != old_keys:
            for i in keys:
                if i == ';':
                    return "UP"
                elif i == ',':
                    return 'LEFT'
                elif i == '.':
                    return 'DOWN'
                elif i == '/':
                    return "RIGHT"
        if xx>= 10:
            return None
        xx+=1
        old_keys = keys
def customdpad(up,left,down,right):
    kb = KeyBoard()
    old_keys = []
    xx = 0
    while True:
        keys = kb.get_pressed_keys()
        if keys != old_keys:
            for i in keys:
                if i == up:
                    return "UP"
                elif i == left:
                    return 'LEFT'
                elif i == down:
                    return 'DOWN'
                elif i == right:
                    return "RIGHT"
        if xx>= 10:
            return None
        xx+=1
        old_keys = keys


def scroll_text(text, color, speed=50, direction="left"):
    """Scroll text horizontally across the display."""
    global tft, font, fontty
    
    display_width = 240
    text_width = (len(text) * 8) if fontty == '8x8' else (len(text) * 16) # Assuming 8 pixels per character for the font
    start_x = display_width if direction == "left" else -text_width
    
    x = start_x
    
    while True:
        tft.fill(0)  # Clear the screen
        tft.text(font, text, x, 50, st7789.color565(color[0], color[1], color[2]))
        if direction == "left":
            x -= 2
            if x + text_width < 0:  # Wrap text back to the start
                x = display_width
        else:
            x += 2
            if x > display_width:  # Wrap text back to the opposite side
                x = -text_width

        time.sleep_ms(speed)
def rect(a,b,c,d,color, fill=False):
    if fill:
        tft.fill_rect(a,b,c,d,st7789.color565(color[0], color[1], color[2]))
    else:
        tft.rect(a,b,c,d,st7789.color565(color[0], color[1], color[2]))
def line(a,b,c,d,color):
    tft.line(a,b,c,d,st7789.color565(color[0], color[1], color[2]))
def pixel(a,b,color):
    tft.pixel(a,b,st7789.color565(color[0], color[1], color[2]))
def checklen(string, start='normal', end='normal'):
    #int(((num1 - cord[0]) / num2) - 1)
    num1 = end if isinstance(end, int) else 240
    num2 = start if isinstance(start, int) else 0
    loopstr = list(str(string))  # Convert string to a list of characters
    whole = []
        
    # Break string into parts
    while len(loopstr) > 0:
        counter = 0
        partal = []
        max_chars_per_line = int(((num1 - num2) / 8) - 1) if fontty == '8x8' else (int(((num1 - num2) / 16) - 1) if fontty == '16x32' else int(((num1 - num2) / 16) - 1))
        while counter < int((max_chars_per_line)) and len(loopstr) > 0:
            partal.append(loopstr.pop(0))  # Append the first character and remove it from loopstr
            counter += 1
        whole.append(''.join(partal))
    return len(whole)


def pressing(list):
    kb = KeyBoard()
    keys = kb.get_pressed_keys()
    if len(keys) > 0 and list[0] == 'any':
        return True
    for iui in list:
        if iui in keys:
            return True
    return False
def pressed():
    kb = KeyBoard()
    return kb.get_pressed_keys()
def sleep(bol):
    tft.sleep_mode(bol)
def set_backlight(state: bool):
    tft.backlight(1 if state else 0)
def button():
    if ppin.value() == 1:
        return False
    return True
def removebuff():
    global buffer, fbuf
    import gc
    gc.collect()
    del gc
    try:
        del buffer
    except:
        None
    try:
        del fbuf
    except:
        None
def initbuff():
    global buffer, fbuf
    removebuff()
    width = 240
    height = 135
    
    # Create a buffer for the frame
    buffer = bytearray(width * height * 2)  # 2 bytes per pixel for RGB565
    fbuf = framebuf.FrameBuffer(buffer, width, height, framebuf.RGB565)

def fbline(x0, y0, x1, y1, color):
    fbuf.line(x0, y0, x1, y1, st7789.color565(color[2], color[0], color[1]))
def fbpixel(x,y,color):
    fbuf.pixel(x,y,st7789.color565(color[2], color[0], color[1]))
def fbdraw(x,y):
    global buffer
    tft.blit_buffer(buffer, x, y, 240, 135)
def fbfill(color):
    fbuf.fill(st7789.color565(color[2], color[0], color[1]))
def fbfind(x, y):
    color = fbuf.pixel(x, y)
    
    if color is None:
        print(f"Error: Invalid pixel at ({x}, {y})")
        return 'BAD'  # Return black if pixel is invalid
    
    # Extract RGB components from RGB565 format
    r = (color >> 11) & 0x1F  # Red is the highest 5 bits
    g = (color >> 5) & 0x3F   # Green is the next 6 bits
    b = color & 0x1F          # Blue is the lowest 5 bits

    # Scale the components to 8-bit values (0-255)
    r = int((r / 31) * 255)
    g = int((g / 63) * 255)
    b = int((b / 31) * 255)

    return [g, b, r]
def fbclear():
    fbuf.fill(0)
def fbrect(a,b,c,d,color, fill=False):
    if fill:
        fbuf.fill_rect(a,b,c,d,st7789.color565(color[2], color[0], color[1]))
    else:
        fbuf.rect(a,b,c,d,st7789.color565(color[2], color[0], color[1]))
def fbpoly(x, y, coords, color, fill=False):
    # Flatten the coords list into a flat list of integers [x0, y0, x1, y1, ..., xn, yn]
    flat_coords = [coord for point in coords for coord in point]
    
    # Convert the list of coordinates into an array of type 'h' (signed short)
    coord_array = array('h', flat_coords)
    
    # Call the framebuffer's poly method to draw the polygon
    fbuf.poly(x, y, coord_array, st7789.color565(color[2], color[0], color[1]), fill)
def fbcircle(x0, y0, radius, color):
    try:
        col = st7789.color565(color[2], color[0], color[1])  # RGB → RGB565
        x = radius
        y = 0
        decision_over2 = 1 - x

        while y <= x:
            for dx, dy in [
                (x, y), (-x, y), (x, -y), (-x, -y),
                (y, x), (-y, x), (y, -x), (-y, -x)
            ]:
                fbuf.pixel(x0 + dx, y0 + dy, col)
            y += 1
            if decision_over2 <= 0:
                decision_over2 += 2 * y + 1
            else:
                x -= 1
                decision_over2 += 2 * (y - x) + 1
    except:
        None
def fbtext(string, cord, color, end='normal'):
    global rotot
    loopstr = list(str(string))  # Convert string to a list of characters
    whole = []
    
    # Break string into parts
    while len(loopstr) > 0:
        counter = 0
        partal = []
        if not isinstance(end, int):
            if rotot % 2 != 0:
                num1 = 240
            else:
                num1 = 135
        else:
            num1 = end
        num2 = 8
        while counter < int(((num1 - cord[0]) / num2) - 1) and len(loopstr) > 0:
            if len(loopstr) >= 2:
                if loopstr[0] == '\\' and loopstr[1] == 'n':
                    loopstr.pop(0)
                    loopstr.pop(0)
                    break
            partal.append(loopstr.pop(0))  # Append the first character and remove it from loopstr
            counter += 1
        whole.append(''.join(partal))  # Join the partal list into a string and add to whole
    
    # Set shift amount based on font size
    shifter = 0
    shiftam = 10

    # Display the text line by line using framebuffer's text method
    for e in whole:
        fbuf.text(
            e,
            cord[0],
            cord[1] + shifter,
            st7789.color565(color[2], color[0], color[1])  # Text color
        )
        shifter += shiftam  # Increase the y-position to avoid overlapping text