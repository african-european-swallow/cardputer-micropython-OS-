from machine import I2C, Pin
import cardputerlib as card
import time

# I2C setup
i2c = I2C(0, scl=Pin(1), sda=Pin(2))

def scan_i2c():
    try:
        return i2c.scan()
    except:
        return []

def draw_grid(found):
    card.clear()
    card.prinS(" I2C Device Grid Scan ", [5, 0], [0, 255, 0])  # Centered title

    # Column headers (8 columns)
    col_header = "    " + " ".join(f"{x:X}" for x in range(8))
    card.prinS(col_header, [0, 1], [200, 200, 200])

    # Grid rows
    row_y = 2
    for row in range(16):
        base = row * 8
        if base > 0x77:
            break  # Don't draw rows starting above 0x77

        line = f"{base:02X}  "
        for offset in range(8):
            addr = base + offset
            if addr > 0x77:
                break  # Skip addresses past 0x77
            if addr in found:
                line += f"{addr:02X} "
            else:
                line += "-- "
        card.prinS(line, [0, row_y], [255, 255, 255])
        row_y += 8

def i2c_grid_main():
    while True:
        found = scan_i2c()
        draw_grid(found)
        card.prinS("R = Rescan     Q = Quit", [0, 127], [128, 128, 128])

        while True:
            if card.pressing(['r']):
                break
            elif card.pressing(['q']):
                return

i2c_grid_main()
