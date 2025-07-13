from cardputerlib import dpad, prinS, setfont, waitfor, clear, rect, line, checklen
import os
import time

blacklist = ['keybord_test.py', 'keybord_screen.py', 'boot.py', 'screen_dray.py',
             'display_test.py', 'caos_shapes.py', 'dpad.py', 'cardrgbtesr.py', 'exampleoled.py',
             'oled_test.py', 'sdcard_reader.py', 'changefont.py', 'scrooltext.py', 'wav_player.py',
             'shell.py']

# Get list of Python files on internal storage
files = [f for f in os.listdir("/") if f.endswith(".py") and f not in blacklist]
if not files:
    files = ["No scripts"]

selected_index = 0

def draw_screen():
    clear()
    setfont('8x8')
    prinS("Launcher", [5, 5], [0, 255, 0])  # Title
    
    file_name = files[selected_index]
    setfont('16x32')

    # Background for selection box
    rect(10, 35, 220, checklen(file_name, start=20, end=220)*32+18, [255, 255, 255])  # White border
    rect(12, 37, 216, checklen(file_name, start=20, end=220)*32+14, [50, 50, 50], fill=True)  # Dark background

    # Print filename inside the selection box
    prinS(file_name, [20, 45], [0, 255, 0], end=220, outline=[50, 50, 50])

draw_screen()

while True:
    key = dpad()
    if key == "RIGHT":
        selected_index = (selected_index + 1) % len(files)
        draw_screen()
    elif key == "LEFT":
        selected_index = (selected_index - 1) % len(files)
        draw_screen()
    elif key == "DOWN" and files[selected_index] != "No scripts":
        setfont('8x8')
        clear()
        exec(open(f"/{files[selected_index]}").read())  # Run selected script
        draw_screen()
    time.sleep(0.2)

