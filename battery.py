from machine import ADC, Pin
import cardputerlib as card
import time
card.setfont('16x32')
VBAT_PIN = 10  # Battery voltage detection pin
adc = ADC(Pin(VBAT_PIN))  
adc.atten(ADC.ATTN_11DB)  # Allow reading up to ~3.6V

# Adjust this factor if the voltage is too high/low
SCALE_FACTOR = 1.8

def read_battery_voltage():
    raw_value = adc.read()
    voltage = (raw_value / 4095) * 3.6  # Convert ADC value to voltage
    actual_voltage = voltage * SCALE_FACTOR  # Adjusted scaling
    return actual_voltage

def battery_percentage(voltage):
    percent = (voltage - 3.0) / (4.2 - 3.0) * 100
    return max(0, min(100, round(percent)))

while True:
    voltage = read_battery_voltage()
    percent = battery_percentage(voltage)
    card.clear()
    card.prinS(f"Battery:\\n{voltage:.2f}V ({percent}%)", [0,0],[0,255,0])
    card.setfont('8x8')
    card.prinS('"e" to exit', [0,80], [255,255,199])
    card.setfont('16x32')
    time.sleep(1)
    if card.pressing(['e']):
        card.clear()
        break
