import time
import cardputerlib as cpl
import random
 
class StopwatchTimer:
    def __init__(self):
        self.running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.mode = "stopwatch"  # Modes: "stopwatch" or "timer"
        self.timer_duration = 30  # Default 30 seconds timer
        self.timer_remaining = self.timer_duration
        self.timer_alarm = False
        self.ran = False
        self.draw_ui()

    def start_stop(self):
        if not self.running:
            self.start_time = time.ticks_ms() - self.elapsed_time
            self.running = True
        else:
            self.elapsed_time = time.ticks_ms() - self.start_time
            self.running = False

    def reset(self):
        self.running = False
        self.elapsed_time = 0
        self.timer_remaining = self.timer_duration
        self.timer_alarm = False
        self.ran = False
        self.draw_ui()

    def switch_mode(self):
        self.mode = "timer" if self.mode == "stopwatch" else "stopwatch"
        self.reset()

    def update(self):
        cpl.clear()
        cpl.prinS(f"Mode: {self.mode}", [10, 10], [255, 255, 255])
        if self.mode == "stopwatch":
            elapsed = (time.ticks_ms() - self.start_time) if self.running else self.elapsed_time
            minutes = elapsed // 60000  # Convert ms to minutes
            seconds = (elapsed // 1000) % 60  # Convert ms to seconds
            time_display = f"{minutes:02}:{seconds:02}"
        else:
            if self.running:
                self.ran = True
                self.timer_remaining = max(0, self.timer_duration - (time.ticks_ms() - self.start_time) // 1000)
                if self.timer_remaining == 0 and not self.timer_alarm:
                    self.timer_alarm = True
                if self.timer_alarm:
                    cpl.fill([random.randint(0,255),random.randint(0,255),random.randint(0,255)])
            elif self.ran == False:
                self.timer_remaining = self.timer_duration
            # Convert timer remaining time to minutes and seconds
            minutes = self.timer_remaining // 60
            seconds = self.timer_remaining % 60
            time_display = f"{minutes:02}:{seconds:02}"  # Format as MM:SS
        if not self.timer_alarm or not self.running:
            cpl.setfont('16x32')
            cpl.prinS(time_display, [40, 50], [0, 255, 0] if self.running else [255, 0, 0])
            cpl.setfont('8x8')

    def draw_ui(self):
        cpl.clear()
        cpl.prinS(f"Mode: {self.mode}", [10, 10], [255, 255, 255])
        cpl.prinS("S: Start/Stop", [10, 30], [255, 255, 255])
        cpl.prinS("R: Reset", [10, 50], [255, 255, 255])
        cpl.prinS("M: Switch Mode", [10, 70], [255, 255, 255])
        time.sleep(0.5)
        cpl.clear()
        if self.mode == 'timer':
            cpl.prinS('Time for Timer:', [0,12],[255,255,255])
            self.moab = cpl.imput('(Min) (Sec): ', [0,20], [255,255,255]).split(' ')
            self.timer_duration = int(self.moab[0])*60 + int(self.moab[1])
        self.update()

    def handle_key(self, key):
        key = key.lower()
        if key == "s":
            self.start_stop()
        elif key == "r":
            self.reset()
        elif key == "m":
            self.switch_mode()
        self.update()

    def check_keys(self):
        if cpl.pressing(["s"]):
            self.handle_key("s")
        if cpl.pressing(["r"]):
            self.handle_key("r")
        if cpl.pressing(["m"]):
            self.handle_key("m")

stopwatch_timer = StopwatchTimer()

while True:
    if cpl.pressing(['`','ESC']):
        break
    stopwatch_timer.check_keys()
    stopwatch_timer.update()
    time.sleep(0.1)
