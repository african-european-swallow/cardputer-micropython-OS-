import cardputerlib as card
from gamepad import SeesawGamepad
import time
import random

BUTTON_PINS = [0, 1, 2, 5, 6, 16]
gamepad = SeesawGamepad(button_pins=BUTTON_PINS)
if gamepad.setup():
    gaming = True
else:
    del BUTTON_PINS
    del gamepad
    gaming = False

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
    SDCARD_MOUNTED = False

card.initbuff()
mode = 0 if not gaming else 2
card.setrotation(1+mode)
# === Grid Configuration ===
grid_w, grid_h = 10, 20  # grid_w: vertical, grid_h: horizontal
block_size = 9
offset_x = 0  # Horizontal offset for sideways grid
hiscore_file = "/sd/tetris_score.txt"

# === Tetris Pieces ===
SHAPES = {
    'I': [[(0,0), (1,0), (2,0), (3,0)]],
    'O': [[(0,0), (0,1), (1,0), (1,1)]],
    'T': [[(0,0), (1,0), (2,0), (1,1)]],
    'L': [[(0,0), (1,0), (2,0), (2,1)]],
    'J': [[(0,0), (1,0), (2,0), (0,1)]],
    'S': [[(1,0), (2,0), (0,1), (1,1)]],
    'Z': [[(0,0), (1,0), (1,1), (2,1)]],
}
COLORS = {
    'I': [0, 255, 255],
    'O': [255, 255, 0],
    'T': [160, 0, 240],
    'L': [255, 128, 0],
    'J': [0, 0, 255],
    'S': [0, 255, 0],
    'Z': [255, 0, 0]
}

SPEEDS = {
    0:500,
    1:448,
    2:396,
    3:344,
    4:292,
    5:240,
    6:188,
    7:136,
    8:84,
    9:63,
    10:52
}

# === Game State Variables ===
grid = []
current = None
cur_x, cur_y = 0, 0
score = 0
level = 0
neclvl = 0
paused = False
next_piece = None

def draw_box(x, y, color):
    if 0 <= x < grid_w and 0 <= y < grid_h:
        px = offset_x + y * block_size + 1
        py = 125 - x * block_size
        card.fbrect(px, py, 8, 8, color, fill=True)

def draw_grid():
    card.fbfill([0, 0, 0])
    for x in range(grid_w):
        for y in range(grid_h):
            color = grid[x][y]
            px = offset_x + y * block_size
            py = 125 - x * block_size
            if color:
                card.fbrect(px + 1, py, 8, 8, color, fill=True)
            else:
                card.fbrect(px, py, 10, 10, [40, 40, 40])

def draw_next():
    if not next_piece:
        return
    name = next_piece['name']
    blocks = next_piece['blocks']
    color = next_piece['color']
    ox, oy = 180, 20
    for dy, dx in rotate(blocks):
        px = ox + dy * 8
        py = oy + dx * 8
        card.fbrect(px, py, 7, 7, color, fill=True)

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

def spawn_piece():
    global current, cur_x, cur_y, next_piece
    if next_piece:
        current = next_piece
    else:
        shape = random.choice(list(SHAPES.keys()))
        current = {
            'name': shape,
            'rot': 0,
            'blocks': SHAPES[shape][0],
            'color': COLORS[shape]
        }
    shape = random.choice(list(SHAPES.keys()))
    next_piece = {
        'name': shape,
        'rot': 0,
        'blocks': SHAPES[shape][0],
        'color': COLORS[shape]
    }
    cur_x, cur_y = 3, 0

def get_piece_coords(x, y, blocks):
    return [(x + dx, y + dy) for dx, dy in blocks]

def valid(pos):
    for x, y in pos:
        if x < 0 or x >= grid_w or y < 0 or y >= grid_h:
            return False
        if grid[x][y] is not None:
            return False
    return True

def rotate(blocks):
    px, py = blocks[1]  # pivot block
    rotated = []
    for x, y in blocks:
        rel_x, rel_y = x - px, y - py
        new_x = px + rel_y
        new_y = py - rel_x
        rotated.append((new_x, new_y))
    return rotated

def freeze_piece():
    global current
    for x, y in get_piece_coords(cur_x, cur_y, current['blocks']):
        if 0 <= x < grid_w and 0 <= y < grid_h:
            grid[x][y] = current['color']
    clear_lines()
    spawn_piece()

def clear_lines():
    global grid, score, level, neclvl
    cleared = 0
    y = 0
    while y < grid_h:
        if all(grid[x][y] for x in range(grid_w)):
            for yy in range(y, 0, -1):
                for x in range(grid_w):
                    grid[x][yy] = grid[x][yy - 1]
            for x in range(grid_w):
                grid[x][0] = None
            cleared += 1
            neclvl += 1
            if neclvl >= 10:
                neclvl = 0
                level += 1
        else:
            y += 1
    score += [0, 40, 100, 300, 1200][cleared] * (level + 1)

def game_over():
    hiscore = load_hiscore()
    if score > hiscore:
        save_hiscore(score)
        new_record = True
    else:
        new_record = False
    card.clear()
    card.setrotation(0+mode)
    card.prinS("GAME OVER", [0, 50], [255, 0, 0])
    card.prinS(f"Score: {score}", [0, 80], [255, 255, 0])
    card.prinS(f"High: {max(score, hiscore)}", [0, 90], [255, 255, 0])
    if new_record:
        card.prinS("NEW RECORD!", [0, 120], [0, 255, 0])
    card.prinS('Play again? \\n(y/A)/(n/B)', [0,140],[255,255,255])
    card.setrotation(1+mode)
    time.sleep(2)

def restart_game():
    global grid, score, current, cur_x, cur_y, next_piece, level, neclvl, paused
    grid = [[None for _ in range(grid_h)] for _ in range(grid_w)]
    score = 0
    paused = False
    level = 0
    neclvl = 0
    current = None
    next_piece = None
    spawn_piece()
    draw_grid()
    card.fbdraw(0, 0)

restart_game()
last_drop = time.ticks_ms()

while True:
    now = time.ticks_ms()
    key = card.dpad()
    if gaming:
        joy_x, joy_y = gamepad.read_joystick()
        buttons = gamepad.read_buttons()
    else:
        joy_x, joy_y = 500, 500
        buttons = []
    moved = False
    if card.pressing(['p']) or 5 in buttons:
        paused = not paused
    if not paused:
        if key == 'DOWN' or joy_x >= 716:
            new_x = cur_x - 1
            if valid(get_piece_coords(new_x, cur_y, current['blocks'])):
                cur_x = new_x
                moved = True
        elif key == 'UP' or joy_x <= 292:
            new_x = cur_x + 1
            if valid(get_piece_coords(new_x, cur_y, current['blocks'])):
                cur_x = new_x
                moved = True
        elif False:#key == 'LEFT' and joy_y <= 300 and False:
            '''new_y = cur_y - 1
            if valid(get_piece_coords(cur_x, new_y, current['blocks'])):
                cur_y = new_y
                moved = True'''
        elif key == 'RIGHT' or joy_y >= 724:
            new_y = cur_y + 1
            score += 1
            if valid(get_piece_coords(cur_x, new_y, current['blocks'])):
                cur_y = new_y
                moved = True
        elif card.pressing(['[',']']) or 2 in buttons or joy_y <= 300 or key == 'LEFT':
            rotated = rotate(current['blocks'])
            if valid(get_piece_coords(cur_x, cur_y, rotated)):
                current['blocks'] = rotated
                moved = True
        elif card.pressing(['r']) or 1 in buttons:
            restart_game()
        elif card.pressing(['`','ESC','q']) or 0 in buttons or 16 in buttons:
            card.setrotation(1)
            break
        elif card.pressing(['OPT']) or 6 in buttons:
            mode = 0 if mode == 2 else 2

        if time.ticks_diff(now, last_drop) >= int(SPEEDS[level]*1.5) if level <= 10 else 52:
            last_drop = now
            if valid(get_piece_coords(cur_x, cur_y + 1, current['blocks'])):
                cur_y += 1
            else:
                freeze_piece()
                if not valid(get_piece_coords(cur_x, cur_y, current['blocks'])):
                    game_over()
                    while True:
                        if gaming:
                            buttons = gamepad.read_buttons()
                        else:
                            buttons = []
                        if card.pressing(['y','r']) or 5 in buttons:
                            resat = True
                            break
                        elif card.pressing(['n']) or 2 in buttons:
                            resat = False
                            break
                    if resat:
                        restart_game()
                    else:
                        card.setrotation(1)
                        break

        draw_grid()
        for x, y in get_piece_coords(cur_x, cur_y, current['blocks']):
            draw_box(x, y, current['color'])
        draw_next()
        card.fbdraw(0, 0)
        card.setrotation(0+mode)
        card.prinS(f"Score: {score}\\nLvl: {level}", [0, 184], [255, 255, 0], end=95)
        card.prinS("Next", [94, 162], [255, 255, 255]) 
        card.setrotation(1+mode)
    else:
        card.setrotation(1+mode)
        card.rect(60,42,60,94,[70,70,70],fill=True)
        card.setrotation(0+mode)
        card.setfont('16x32')
        card.prinS('Paused',[0,70],[0,255,0],outline=[70,70,70])
        card.setfont('8x8')
        card.setrotation(1+mode)
    time.sleep(0.05)

