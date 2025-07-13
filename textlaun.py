from cardputerlib import prinS, imput, clear, setfont
import os, time
# List all files in the current directory

files = os.listdir()

filese = []
blacklist = ['keybord_test.py', 'keybord_screen.py', 'boot.py', 'screen_dray.py',
             'display_test.py','caos_shapes.py', 'dpad.py', 'cardrgbtesr.py', 'exampleoled.py',
             'oled_test.py', 'sdcard_reader.py', 'changefont.py', 'scrooltext.py', 'wav_player.py']
# Loop through the files and print those ending with .py
for file in files:
    if file.endswith(".py") and file not in blacklist:
        filese.append(file)


# Ask user to input file to execute and ensure file exists


# Ensure the file exists
while True:
    clear()
    setfont('8x8')
    prinS('exe: ', [0,120], [0,0,255])
    prinS(', '.join(filese), [0,10], [0,0,255])
    file_to_exec = imput('exe: ', [0,120], [0,0,255])
    if file_to_exec in files:
        with open(file_to_exec) as f:
            clear()
            exec(f.read())
    else:
        clear()
        prinS("File not found!", [0,10], [255,0,0])
        time.sleep(2)
        clear()
