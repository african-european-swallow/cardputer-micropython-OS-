import time
import machine
from machine import Pin
from micropython import const

# Define constants for modifier keys
kc_shift = const(61)
kc_fn = const(65)

# Define keymaps for different modes
keymap = {
    67: '`',  63: '1',  57: '2',  53: '3', 47: '4', 43: '5', 37: '6', 33: '7', 27: '8', 23: '9', 17: '0', 13: '_', 7: '=', 3: 'BSPC',
    66: 'TAB', 62: 'q',  56: 'w',  52: 'e', 46: 'r', 42: 't', 36: 'y', 32: 'u', 26: 'i', 22: 'o', 16: 'p', 12: '[', 6: ']', 2: '\\',
    55: 'a',  51: 's', 45: 'd', 41: 'f', 35: 'g', 31: 'h', 25: 'j', 21: 'k', 15: 'l', 11: ';', 5: "'", 1: 'ENT',
    64: 'CTL', 60: 'OPT', 54: 'ALT', 50: 'z', 44: 'x', 40: 'c', 34: 'v', 30: 'b', 24: 'n', 20: 'm', 14: ',', 10: '.', 4: '/', 0: ' ',
}

keymap_shift = {
    67: '~',  63: '!',  57: '@',  53: '#', 47: '$', 43: '%', 37: '^', 33: '&', 27: '*', 23: '(', 17: ')', 13: '-', 7: '+', 3: 'BSPC',
    66: 'TAB', 62: 'Q',  56: 'W',  52: 'E', 46: 'R', 42: 'T', 36: 'Y', 32: 'U', 26: 'I', 22: 'O', 16: 'P', 12: '{', 6: '}', 2: '|',
    55: 'A',  51: 'S', 45: 'D', 41: 'F', 35: 'G', 31: 'H', 25: 'J', 21: 'K', 15: 'L', 11: ':', 5: '"', 1: 'ENT',
    64: 'CTL', 60: 'OPT', 54: 'ALT', 50: 'Z', 44: 'X', 40: 'C', 34: 'V', 30: 'B', 24: 'N', 20: 'M', 14: '<', 10: '>', 4: '?', 0: ' ',
}

keymap_fn = {
    67: 'ESC', 63: 'F1', 57: 'F2', 53: 'F3', 47: 'F4', 43: 'F5', 37: 'F6', 33: 'F7', 27: 'F8', 23: 'F9', 17: 'F10', 13: '_', 7: '=', 3: 'DEL',
    66: 'TAB', 62: 'q', 56: 'w', 52: 'e', 46: 'r', 42: 't', 36: 'y', 32: 'u', 26: 'i', 22: 'o', 16: 'p', 12: '[', 6: ']', 2: '\\',
    55: 'a', 51: 's', 45: 'd', 41: 'f', 35: 'g', 31: 'h', 25: 'j', 21: 'k', 15: 'l', 11: 'UP', 5: "'", 1: 'ENT',
    64: 'CTL', 60: 'OPT', 54: 'ALT', 50: 'z', 44: 'x', 40: 'c', 34: 'v', 30: 'b', 24: 'n', 20: 'm', 14: 'LEFT', 10: 'DOWN', 4: 'RIGHT', 0: ' ',
}

class KeyBoard:
    def __init__(self):
        self._key_list_buffer = []
        
        # Setup column pins (inputs with pull-up resistors)
        self.pinMap = {
            'C0': Pin(13, Pin.IN, Pin.PULL_UP),
            'C1': Pin(15, Pin.IN, Pin.PULL_UP),
            'C2': Pin(3, Pin.IN, Pin.PULL_UP),
            'C3': Pin(4, Pin.IN, Pin.PULL_UP),
            'C4': Pin(5, Pin.IN, Pin.PULL_UP),
            'C5': Pin(6, Pin.IN, Pin.PULL_UP),
            'C6': Pin(7, Pin.IN, Pin.PULL_UP),
            'A0': Pin(8, Pin.OUT),
            'A1': Pin(9, Pin.OUT),
            'A2': Pin(11, Pin.OUT),
        }
        
        self.key_state = []

    def scan(self):
        """Scan through the matrix to see what keys are pressed."""
        self._key_list_buffer = []
        
        # Loop through the 8 rows
        for row in range(8):
            # Activate the row by setting the appropriate bits for A0, A1, A2
            self.pinMap['A0'].value(row & 0b001)
            self.pinMap['A1'].value((row & 0b010) >> 1)
            self.pinMap['A2'].value((row & 0b100) >> 2)
        
            # Check the columns
            for i, col in enumerate(['C6', 'C5', 'C4', 'C3', 'C2', 'C1', 'C0']):
                val = self.pinMap[col].value()
                
                if not val:  # Key pressed
                    key_address = (i * 10) + row
                    self._key_list_buffer.append(key_address)
                
        return self._key_list_buffer
    
    def get_pressed_keys(self):
        """Get a readable list of currently held keys."""
        self.scan()  # Update the scan results
        self.key_state = []

        if not self._key_list_buffer:
            return self.key_state
        
        if kc_fn in self._key_list_buffer:
            # Remove modifier keys which are already accounted for
            self._key_list_buffer.remove(kc_fn)
            if kc_shift in self._key_list_buffer:
                self._key_list_buffer.remove(kc_shift)
            
            for keycode in self._key_list_buffer:
                self.key_state.append(keymap_fn.get(keycode, ''))
        
        elif kc_shift in self._key_list_buffer:
            # Remove modifier keys which are already accounted for
            self._key_list_buffer.remove(kc_shift)
            
            for keycode in self._key_list_buffer:
                self.key_state.append(keymap_shift.get(keycode, ''))
        
        else:
            for keycode in self._key_list_buffer:
                self.key_state.append(keymap.get(keycode, ''))
        
        return self.key_state
