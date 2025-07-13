import cardputerlib as card
import os
import time
keep_variables = ['card', 'os', 'time', 'keep_variables', 'spi', 'cs', 'sd','vfs','uos', 'SDCARD_MOUNTED','is_dir','list_files',
                 'get_files','printSC','dir','boxX','textM', 'get_page_items','sels','temps','filese'] # Variables to keep
try:
    import sdcard
    import machine
    import uos

    # Configure SPI and CS pin to match your hardware setup
    spi = machine.SPI(1, baudrate=1000000, sck=machine.Pin(40), mosi=machine.Pin(14), miso=machine.Pin(39))
    cs = machine.Pin(12, machine.Pin.OUT)

    sd = sdcard.SDCard(spi, cs)
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")
    SDCARD_MOUNTED = True
except Exception as e:
    print("SD card mount failed:", e)
def is_dir(path):
    try:
        mode = os.stat(path)[0]
        return mode & 0x4000 == 0x4000  # 0x4000 = stat.S_IFDIR
    except:
        return False
def list_files(directory):
    """Returns a list of files and directories from the given directory."""
    files = []
    for file in os.listdir(directory):
        full_path = directory.rstrip("/") + "/" + file
        if file.endswith(".py") or is_dir(full_path):
            if is_dir(full_path):
                files.append(file + '/')
            else:
                files.append(file)
    return files
card.prinS('LOADING',[80,80], [0,255,0])
dir = '/'
boxX = 80
card.setfont('8x8')
textM = 79 if card.fontty == '8x8' else 85

# List all files in the current directory
def get_files(dir):
    fill = list_files(dir.rstrip("/"))
    files = []
    blacklist = ['keybord_test.py', 'keybord_screen.py', 'boot.py', 'screen_dray.py',
                 'display_test.py', 'caos_shapes.py', 'dpad.py', 'cardrgbtesr.py', 'exampleoled.py',
                 'oled_test.py', 'changefont.py', 'scrooltext.py', 'wav_player.py',
                 'main.py', 'boxlauncher6.py','boxlauncher9.py','launcher.py', 'textlaun.py', 'wiplan.py',
                 'webrepl_cfg.py', 'lib/', 'font/', 'hiya/', 'DOOM/', 'display_test.py',
                 'espkey.py', 'gyrotest.py','is_folder.py','oled_test.py','ryainpy.py',
                 'shellout.py','waitforit.py']
    
    # Loop through the files and add those ending with .py and not in blacklist
    for file in fill:
        if file not in blacklist:
            files.append(file)
    filecc = []
    oubuffer = []
    for file in range(len(files)):
        if list(files[file])[-1] == '/':
            filecc.append(files[file])
        else:
            oubuffer.append(files[file])
    for file in oubuffer:
        filecc.append(file)
    del oubuffer
    del files
    filecc.insert(0,'/')
    return filecc
filese = get_files(dir)
# Print function for the launcher screen
def printSC(items, selected, colorIn=[50,50,50], colorOt=[255,255,255]):
    selC = [255, 0, 0]
    items_to_display = items[:6]  # Show only the first 6 items for the current page
    for i in range(len(items_to_display)):
        card.rect(boxX*i if i < 3 else boxX*(i-3), 8 if i < 3 else 67, 72, 55, colorIn, fill=True)
        card.rect(boxX*i if i < 3 else boxX*(i-3), 8 if i < 3 else 67, 72, 55, colorOt if i != selected else selC, fill=False)
        card.prinS(items_to_display[i], [boxX*i+1 if i < 3 else boxX*(i-3)+1, 10 if i < 3 else 69], [0, 255, 0], outline=colorIn, end=boxX*i+textM if i < 3 else boxX*(i-3)+textM)

# Create a function to get the correct slice of items based on the current page
def get_page_items(page_number):
    start_index = page_number * 6
    end_index = start_index + 6
    return filese[start_index:end_index]

sels = [0, 0]  # sels[0] = selected item, sels[1] = current page number
card.clear()
# Initial screen render
temps = get_page_items(sels[1])  # Make sure temps is defined before the loop
printSC(temps, sels[0])
while True:
    car = card.dpad()

    if car != None:
        # Move selection up (stay within bounds for the current page)
        if car == 'UP' and sels[0] > 2:
            sels[0] -= 3
        # Move selection down (stay within bounds for the current page)
        elif car == 'DOWN' and sels[0] < 3 and len(get_page_items(sels[1])) > 3:
            sels[0] += 3
        # Move selection left
        elif car == 'LEFT' and sels[0] > 0:
            sels[0] -= 1
        # Move selection right
        elif car == 'RIGHT' and sels[0] < 5:
            sels[0] += 1
        # Move to next page
        elif car == 'DOWN' and sels[0] > 2 and len(filese) - 6 * (sels[1] + 1) > 0:
            sels[1] += 1
            sels[0] = sels[0] - 3  # Reset selection to the top of the next page
            card.clear()
        # Move to previous page
        elif car == 'UP' and sels[0] < 3 and sels[1] > 0:
            sels[1] -= 1
            sels[0] = sels[0] + 3  # Reset selection to the top of the previous page
            card.clear()

        # Make sure selection does not go out of bounds
        max_items_on_page = len(get_page_items(sels[1]))  # Items on the current page
        if sels[0] >= max_items_on_page:
            sels[0] = max_items_on_page - 1  # Keep selection within the page's bounds

        # Get the current page's slice of items
        temps = get_page_items(sels[1])
        printSC(temps, sels[0])

    # Check if Enter is pressed to launch the selected file, on every frame
    if card.pressing(['ENT']):
        selected_file = temps[sels[0]]  # Get the selected file name
        if selected_file == '/':
            dir = '/'
            card.clear()
            card.prinS('LOADING',[80,40], [0,255,0])
            filese = get_files(dir)
            card.clear()
            sels = [0, 0]
            temps = get_page_items(sels[1])  # Update `temps` after returning from program execution
            printSC(temps, sels[0])
        elif selected_file.endswith('/'):
            dir += selected_file
            card.clear()
            card.prinS('LOADING',[80,40], [0,255,0])
            filese = get_files(dir)
            card.clear()
            sels = [0, 0]
            temps = get_page_items(sels[1])  # Update `temps` after returning from program execution
            printSC(temps, sels[0])
        else:
            card.clear()
            card.prinS(f"Running {selected_file}...", [0, 10], [0, 255, 0])
            time.sleep(0.1)  # Show a loading message for a moment
    
            try:
                with open(dir + selected_file) as f:
                    card.clear()
                    exec(f.read())  # Execute the file
            except Exception as e:
                card.clear()
                card.prinS(f"Error: {str(e)}", [0, 10], [255, 0, 0])
                time.sleep(2)
                card.clear()
            for name in list(globals()):
                if name not in keep_variables:
                    del globals()[name]
            import gc
            gc.collect()
            card.removebuff()
            # Immediately reload the launcher screen after program execution
            card.setfont('8x8')
            card.clear()
            temps = get_page_items(sels[1])  # Update `temps` after returning from program execution
            printSC(temps, sels[0])  # Re-render the launcher screen

    time.sleep(0.1)
