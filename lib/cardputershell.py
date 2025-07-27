#usages:
#(var = ShellPrinter) to init the things (very disctiptive!)
#var.print(string) to print in the shell
#var.set_color((rval, gval, bval)) to change the shell's font color
#var.set_font('8x8' or '16x16' or '16x32') to set shell's font 8x8 is the basic starting one
#var.input(string) acts as input but for the new shell
#var.clear() to clear the screen + text reserves
from machine import Pin, SPI
import st7789py as st7789
import time
from font import vga2_8x8 as font
fontty = '8x8'
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
class ShellPrinter:
    def __init__(self, width=240, height=135):
        self.width = width
        self.height = height
        self.fontty = '8x8'
        self.line_height = self._get_line_height()
        self.max_lines = self.height // self.line_height
        self.buffer = []
        self.color = (255, 255, 255)
        self.font = self._load_font(self.fontty)
        self.anchor_index = 0  # line index in buffer where input starts

    def _get_line_height(self):
        return 8 if self.fontty == '8x8' else (30 if self.fontty == '16x32' else 14)

    def _load_font(self, font_type):
        if font_type == '8x8':
            from font import vga2_8x8 as font
        elif font_type == '16x32':
            from font import vga2_16x32 as font
        elif font_type == '16x16':
            from font import vga2_16x16 as font
        else:
            raise ValueError("Unknown font type")
        return font

    def _render(self):
        tft.fill(0)
        for i, line in enumerate(self.buffer[-self.max_lines:]):
            tft.text(self.font, line, 0, i * self.line_height, st7789.color565(*self.color))

    def set_color(self, color):
        self.color = color

    def set_font(self, font_type):
        self.fontty = font_type
        self.line_height = self._get_line_height()
        self.max_lines = self.height // self.line_height
        self.font = self._load_font(font_type)

    def clear(self):
        self.buffer = []
        tft.fill(0)

    def checklen(self, string):
        max_chars = 30 if self.fontty == '8x8' else 15
        return (len(string) + max_chars - 1) // max_chars

    def _wrap_text(self, text):
        max_chars = 30 if self.fontty == '8x8' else 15
        return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

    def print(self, text):
        for line in self._wrap_text(text):
            if len(self.buffer) >= self.max_lines:
                self.buffer.pop(0)
            self.buffer.append(line)
        self._render()

    def printin(self, text):
        wrapped = self._wrap_text(text)
        for i, line in enumerate(wrapped):
            idx = self.anchor_index + i
            if idx < len(self.buffer):
                self.buffer[idx] = line
            else:
                self.buffer.append(line)
        self._render()

    def input(self, prompt):
        self.lineused = self.checklen(prompt)
        self.anchor_index = len(self.buffer)
        self.buffer += [''] * self.lineused
        self.printin(prompt)

        kb = KeyBoard()
        input_chars = []
        prev_keys = []
        held_keys = []
        last = ''

        while True:
            keys = kb.get_pressed_keys()
            if keys != prev_keys:
                for key in keys:
                    if key in held_keys:
                        continue
                    if key == 'ENT':
                        result = ''.join(input_chars)
                        self.printin(prompt + result)
                        time.sleep(0.25)
                        return result
                    elif key == 'BSPC' and input_chars:
                        input_chars.pop()
                    elif key == 'TAB':
                        input_chars.extend([' '] * 4)
                    elif key == 'ESC':
                        return ''
                    elif key not in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                        input_chars.append(key)
                    held_keys.append(key)

                for key in held_keys[:]:
                    if key not in keys:
                        held_keys.remove(key)

                full_text = prompt + ''.join(input_chars)

                # If text grew beyond initial space, shift buffer
                while self.checklen(full_text) > self.lineused:
                    self.buffer.append('')
                    self.buffer.pop(0)
                    self.anchor_index -= 1
                    self.lineused += 1

                if full_text != last:
                    self.printin(full_text)
                    last = full_text

                prev_keys = keys


