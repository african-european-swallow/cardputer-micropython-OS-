import time
import seesaw

class SeesawGamepad:
    def __init__(self, joystick_xx=14, joystick_yx=15, joystick_xy=14, joystick_yy=16, button_pins=None):
        self.JOY_XX = joystick_xx
        self.JOY_YX = joystick_yx
        self.JOY_XY = joystick_xy
        self.JOY_YY = joystick_yy
        
        # Default button pins if none specified
        if button_pins is None:
            self.BUTTON_PINS = list(range(12))
        else:
            self.BUTTON_PINS = button_pins
        
    def setup(self):
        try:
            seesaw.init()
            for pin in self.BUTTON_PINS:
                seesaw.pin_config(pin, mode=0, pull=1)
            return True  # setup succeeded
        except OSError as e:
            # Usually no device found raises OSError (e.g. ENODEV)
            print("Seesaw device not found:", e)
            return None

    
    def read_joystick(self):
        # Read analog joystick axes (note: two reads per axis, take second one)
        x = seesaw.analog_read(self.JOY_XX)
        x = seesaw.analog_read(self.JOY_YX)
        y = seesaw.analog_read(self.JOY_XY)
        y = seesaw.analog_read(self.JOY_YY)
        return x, y
    
    def read_buttons(self):
        pressed = []
        val = seesaw._read(0x01, 0x04, 8)  # read all GPIOs at once once per call for efficiency
        for pin in self.BUTTON_PINS:
            byte_index = 3 - (pin // 8)
            if pin >= 32:
                byte_index += 4
                pin_mod = pin - 32
            else:
                pin_mod = pin
            bit = (val[byte_index] >> (pin_mod % 8)) & 1
            if bit == 0:  # active low
                pressed.append(pin)
        return pressed
    
    def loop(self, delay=0.1):
        while True:
            x, y = self.read_joystick()
            buttons = self.read_buttons()
            print(f"Joystick X: {x}, Y: {y}")
            print("Buttons pressed:", buttons)
            time.sleep(delay)
