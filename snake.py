import cardputerlib as card
import time
import random
import os
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
# === Config ===
width, height = 26, 14
score = 0
hiscore_file = "/sd/snake_score.txt"
foodnum = 5

# === Setup ===
card.initbuff()

class Tail:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Fruitt:
    def __init__(self,cords):
        self.x, self.y = cords

def draw_grid():
    card.fbfill([0, 0, 0])
    for i in range(width):
        for j in range(height):
            card.fbrect(i*9, j*9, 10, 10, [40, 40, 40])

def plbox(x, y, color):
    card.fbrect(x*9+1, y*9+1, 8, 8, color, fill=True)

def rand_pos():
    cucu = 0
    while True:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if not any(seg.x == x and seg.y == y for seg in snake) and not any(seg.x == x and seg.y == y for seg in fruit):
            return (x, y)
        if cucu > 300:
            return (x,y)
        cucu += 1


def load_hiscore():
    try:
        with open(hiscore_file, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_hiscore(new_score):
    try:
        with open(hiscore_file, "w") as f:
            f.write(str(new_score))
    except Exception as e:
        print("Error saving high score:", e)
while True:
   # === Game Setup ===
    snake = [Tail(width//2, height//2)]
    direction = None
    fruit = []
    for i in range(foodnum):
        fruit.append(Fruitt(rand_pos()))
    alive = True
    off = 0
    score = 0
    hiscore = load_hiscore()

    draw_grid()
    for seg in snake:
        plbox(seg.x, seg.y, [255, 0, 0])
    for fr in fruit:
        plbox(fr.x, fr.y, [0, 255, 0])
    card.fbdraw(0, 0)

    # === Wait for initial direction ===
    card.prinS("Press arrow to start", [30, 110], [100, 100, 255])
    card.fbdraw(0, 0)
    while direction is None:
        key = card.dpad()
        if key == 'UP': direction = [0, -1]
        elif key == 'DOWN': direction = [0, 1]
        elif key == 'LEFT': direction = [-1, 0]
        elif key == 'RIGHT': direction = [1, 0]
        time.sleep(0.05)

    last_move = time.ticks_ms()
    # === Game Loop ===
    while alive:
        now = time.ticks_ms()

        key = card.dpad()
        if key == 'UP' and direction != [0, 1]: direction = [0, -1]
        elif key == 'DOWN' and direction != [0, -1]: direction = [0, 1]
        elif key == 'LEFT' and direction != [1, 0]: direction = [-1, 0]
        elif key == 'RIGHT' and direction != [-1, 0]: direction = [1, 0]

        if time.ticks_diff(now, last_move) >= 200:
            last_move = now

            head = snake[0]
            new_x = head.x + direction[0]
            new_y = head.y + direction[1]

            # Game Over check
            if (new_x < 0 or new_x >= width or
                new_y < 0 or new_y >= height or
                any(seg.x == new_x and seg.y == new_y for seg in snake)):
                alive = False
                break
            for s in range(len(fruit)):
                if (new_x, new_y) == (fruit[s].x,fruit[s].y):
                    save = s
                    break
                else:
                    save = None
            # Move or Grow
            if save != None:
                snake.insert(0, Tail(new_x, new_y))
                fruit[save].x,fruit[save].y = (40,40)
                score += 1
                off += 1
            else:
                snake.insert(0, Tail(new_x, new_y))
                snake.pop()
            if off >= len(fruit):
                for i in range(len(fruit)):
                    fruit[i].x,fruit[i].y = rand_pos()
                off = 0
            # Draw
            draw_grid()
            for seg in snake:
                plbox(seg.x, seg.y, [255, 0, 0])
            for fr in fruit:
                plbox(fr.x, fr.y, [0, 255, 0])
            card.fbdraw(0, 0)

        time.sleep(0.01)

    # === Death Screen ===
    if score > hiscore:
        save_hiscore(score)
        new_record = True
    else:
        new_record = False

    card.fbfill([0, 0, 0])
    card.clear()
    card.prinS("Game Over", [30, 20], [255, 0, 0])
    card.prinS(f"Score: {score}", [30, 60], [255, 255, 255])
    card.prinS(f"High: {max(score, hiscore)}", [30, 80], [255, 255, 0])
    if new_record:
        card.prinS("NEW RECORD!", [10, 110], [0, 255, 0])
    time.sleep(0.5)
    ok=False
    if not ok:
        time.sleep(0.75)
        card.prinS('continue?(y)', [110,110], [0,255,0])
        while True:
            if card.pressing(['any']):
                break
            time.sleep(0.05)
        if card.pressing(['any']) and not card.pressing(['y']):
            time.sleep(0.1)
            break 
    card.fbdraw(0, 0)
