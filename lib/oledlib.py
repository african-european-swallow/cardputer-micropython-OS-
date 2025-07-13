from machine import SoftI2C, Pin
import ssd1306
# Initialize I2C with correct SDA and SCL pins
i2c = SoftI2C(scl=Pin(1), sda=Pin(2), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D)  # Change from 0x3C to 0x3D
def printS(string, cord):
    loopstr = list(str(string))  # Convert string to a list of characters
    whole = []
    
    # Break string into parts
    while len(loopstr) > 0:
        counter = 0
        partal = []
        num1 = 128
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
    
    # Display the text line by line
    
    shifter = 0
    shiftam = 10
    for e in whole:
        oled.text(e, cord[0], cord[1] + shifter)
        shifter += shiftam  # Increase the y-position to avoid overlapping text
    oled.show()
def clear(allway):
    oled.fill(0)
    if allway:
        oled.show()
def show():
    oled.show()
def invert(num):
    oled.invert(num)