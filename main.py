import cardputerlib as card
import os
import time

keep_variables = ['card', 'os', 'time', 'keep_variables', 'spi', 'cs', 'sd','vfs','uos', 'SDCARD_MOUNTED','is_dir','list_files',
                 'get_files','printSC','dir','boxX','textM', 'get_page_items','sels','temps','filese', 'ITEMS_PER_PAGE','ROWS_PER_PAGE',
                  'ITEMS_PER_ROW','ROWS_PER_PAGE' ,'ITEMS_PER_ROW', 'boxY','selected_file']

try:
    import sdcard
    import machine
    import uos

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
        return mode & 0x4000 == 0x4000
    except:
        return False

def list_files(directory):
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
card.setfont('8x8')



ITEMS_PER_ROW = 3
ROWS_PER_PAGE = 3
ITEMS_PER_PAGE = ITEMS_PER_ROW * ROWS_PER_PAGE
textM = int(240/ITEMS_PER_ROW)-1 if card.fontty == '8x8' else 85
boxX = int(240/ITEMS_PER_ROW) #80
boxY = int(126/ROWS_PER_PAGE)  # new height of each box #42

def get_files(dir):
    fill = list_files(dir.rstrip("/"))
    files = []
    blacklist = ['keybord_test.py', 'keybord_screen.py', 'boot.py', 'screen_dray.py',
                 'display_test.py', 'caos_shapes.py', 'dpad.py', 'cardrgbtesr.py', 'exampleoled.py',
                 'oled_test.py', 'changefont.py', 'scrooltext.py', 'wav_player.py',
                 'main.py', 'boxlauncher6.py','boxlauncher9.py','launcher.py', 'textlaun.py', 'wiplan.py',
                 'webrepl_cfg.py', 'lib/', 'font/', 'hiya/', 'DOOM/', 'display_test.py',
                 'espkey.py', 'gyrotest.py','is_folder.py','oled_test.py','ryainpy.py',
                 'shellout.py','waitforit.py','hello.py','scrolltext.py','sdcard_reader.py',
                 ]
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

def printSC(items, selected, colorIn=[70,70,70], colorOt=[255,255,255]):
    selC = [255, 0, 0]
    for i in range(len(items)):
        row = i // ITEMS_PER_ROW
        col = i % ITEMS_PER_ROW
        x = boxX * col
        y = 8 + row * boxY
        card.rect(x, y, boxX-8, boxY-4, colorIn, fill=True)
        card.rect(x, y, boxX-8, boxY-4, selC if i == selected else colorOt, fill=False)
        card.prinS(items[i], [x + 1, y + 2], [0, 255, 0], outline=colorIn, end=x + textM)

def get_page_items(page_number):
    start_index = page_number * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    return filese[start_index:end_index]

sels = [0, 0]
card.clear()
temps = get_page_items(sels[1])
printSC(temps, sels[0])

while True:
    car = card.dpad()

    if car is not None:
        max_items = len(get_page_items(sels[1]))
        row = sels[0] // ITEMS_PER_ROW
        col = sels[0] % ITEMS_PER_ROW

        # Move up within page
        if car == 'UP' and row > 0:
            sels[0] -= ITEMS_PER_ROW

        # Move down within page
        elif car == 'DOWN' and row < ROWS_PER_PAGE - 1 and (sels[0] + ITEMS_PER_ROW) < max_items:
            sels[0] += ITEMS_PER_ROW

        # Move left
        elif car == 'LEFT' and col > 0:
            sels[0] -= 1

        # Move right
        elif car == 'RIGHT' and col < ITEMS_PER_ROW - 1 and (sels[0] + 1) < max_items:
            sels[0] += 1

        # Page down from bottom row → top row next page, same column
        elif car == 'DOWN' and row == ROWS_PER_PAGE - 1 and (sels[1] + 1) * ITEMS_PER_PAGE < len(filese):
            sels[1] += 1
            # move selection to top row (row 0) same column
            new_index = 0 * ITEMS_PER_ROW + col
            max_new_items = len(get_page_items(sels[1]))
            sels[0] = min(new_index, max_new_items - 1)
            card.clear()

        # Page up from top row → bottom row previous page, same column
        elif car == 'UP' and row == 0 and sels[1] > 0:
            sels[1] -= 1
            # move selection to bottom row (last row) same column
            max_new_items = len(get_page_items(sels[1]))
            last_row = (max_new_items - 1) // ITEMS_PER_ROW  # zero-indexed last row
            new_index = last_row * ITEMS_PER_ROW + col
            # clamp index to max items
            sels[0] = min(new_index, max_new_items - 1)
            card.clear()

        # Clamp if needed
        max_items = len(get_page_items(sels[1]))
        if sels[0] >= max_items:
            sels[0] = max_items - 1

        temps = get_page_items(sels[1])
        printSC(temps, sels[0])

    if card.pressing(['BSPC']):
        for name in list(globals()):
            if name not in keep_variables:
                del globals()[name]
        card.removebuff()
        import gc
        gc.collect()
        card.setfont('8x8')
        card.clear()
        temps = get_page_items(sels[1])
        printSC(temps, sels[0])
    if card.pressing(['ENT']):
        selected_file = temps[sels[0]]
        if selected_file == '/':
            dir = '/'
            card.clear()
            card.prinS('LOADING',[80,40], [0,255,0])
            filese = get_files(dir)
            card.clear()
            sels = [0, 0]
            temps = get_page_items(sels[1])
            printSC(temps, sels[0])
        elif selected_file.endswith('/'):
            dir += selected_file
            card.clear()
            card.prinS('LOADING',[80,40], [0,255,0])
            filese = get_files(dir)
            card.clear()
            sels = [0, 0]
            temps = get_page_items(sels[1])
            printSC(temps, sels[0])
        else:
            card.clear()
            card.prinS(f"Running {selected_file}...", [0, 10], [0, 255, 0])
            time.sleep(0.1)
            for name in list(globals()):
                if name not in keep_variables:
                    del globals()[name]
            card.removebuff()
            import gc
            gc.collect()
            try:
                with open(dir + selected_file) as f:
                    card.clear()
                    exec(f.read(), {})
            except Exception as e:
                card.clear()
                card.prinS(f"Error: {str(e)}", [0, 10], [255, 0, 0])
                time.sleep(2)
                card.clear()
            for name in list(globals()):
                if name not in keep_variables:
                    del globals()[name]
            card.removebuff()
            import gc
            gc.collect()
            card.setfont('8x8')
            card.clear()
            temps = get_page_items(sels[1])
            printSC(temps, sels[0])

    time.sleep(0.05)



