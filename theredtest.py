import _thread
import cardputerlib as card
import time

stop = False
running = True
run = True
dir = '/'
counter = 0
selected_file = '_texteditor.py'
try:
    def listen():
        global stop, running
        try:
            while not stop:
                with open(dir + selected_file) as f:
                        card.clear()
                        exec(f.read())
                        running = False
                        stop = True
        except KeyboardInterrupt:
            stop = True
            run = False
            print("Program interrupted by user.")
            
    _thread.start_new_thread(listen, ())

    while run:
        try:
            counter+=1
            if not running:
                card.prinS(str(counter), [0,0],[255,0,0])
            if card.pressing(['a']) and stop:
                stop = False
                running = True
                _thread.start_new_thread(listen, ())
            time.sleep(0.1)
        except KeyboardInterrupt:
            stop = True
            run = False
            print("Program interrupted by user.")
except KeyboardInterrupt:
    stop = True
    run = False
    print("Program interrupted by user.")