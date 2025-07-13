# brawlclone_maptest.py
import time
import cardputerlib as cp  # Your custom lib with fb, kb, etc.
cp.initbuff()

# === Tilemap setup ===
tilemap = [
    "WWWWWWWWWWWWWWWWWWWWWWWW",
    "W..........WW..........W",
    "W..WW......W....WW.....W",
    "W......................W",
    "W....W...WWW..W........W",
    "W......................W",
    "W..W......WW...........W",
    "W..........W..WW..W....W",
    "W..............W.......W",
    "W..WW.............WW...W",
    "W..........W...........W",
    "W......................W",
    "WWWWWWWWWWWWWWWWWWWWWWWW"
]

tile_definitions = {
    "W": {"color": [255,0,0], "solid": True},   # Wall (Blue)
    ".": {"color": [0,255,0], "solid": False},  # Ground (Green)
}

tile_size = 10

# === Player setup ===
class Player:
    def __init__(self, x, y, color=[255,255,255]):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        cp.fbrect(self.x, self.y, tile_size, tile_size, self.color, fill=True)

player = Player(20, 20)

# === Projectile setup ===
class Bullet:
    def __init__(self, x, y, dx, dy, color=[255, 0, 0]):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.alive = True

    def move(self):
        new_x = self.x + self.dx
        new_y = self.y + self.dy
        if is_solid(new_x, new_y, 4, 4):
            self.alive = False
        else:
            self.x = new_x
            self.y = new_y

    def draw(self):
        cp.fbrect(self.x, self.y, 4, 4, self.color, fill=True)

bullets = []

# === Draw tilemap ===
def draw_tilemap():
    for y, row in enumerate(tilemap):
        for x, ch in enumerate(row):
            tile = tile_definitions.get(ch, {"color": [0,0,0], "solid": False})
            cp.fbrect(x * tile_size, y * tile_size, tile_size, tile_size, tile["color"], fill=True)

# === Check solid tile ===
def is_solid(px, py, w=tile_size, h=tile_size):
    # Check corners of bounding box
    corners = [
        (px, py),
        (px + w - 1, py),
        (px, py + h - 1),
        (px + w - 1, py + h - 1)
    ]
    for cx, cy in corners:
        tile_x = cx // tile_size
        tile_y = cy // tile_size
        if tile_y < 0 or tile_y >= len(tilemap) or tile_x < 0 or tile_x >= len(tilemap[0]):
            return True
        ch = tilemap[tile_y][tile_x]
        if tile_definitions.get(ch, {"solid": False})["solid"]:
            return True
    return False

# === Move with collision ===
def move_player(dx, dy):
    new_x = player.x + dx
    new_y = player.y + dy
    if not is_solid(new_x, player.y):
        player.x = new_x
    if not is_solid(player.x, new_y):
        player.y = new_y
def is_colliding(ax, ay, aw, ah, bx, by, bw, bh):
    return (
        ax < bx + bw and
        ax + aw > bx and
        ay < by + bh and
        ay + ah > by
    )

# === Main game loop ===
while True:
    cp.fbclear()
    draw_tilemap()
    player.draw()

    # Update and draw bullets
    for b in bullets:
        if b.alive:
            b.move()
            b.draw()
    bullets = [b for b in bullets if b.alive]

    cp.fbdraw(0, 0)

    # Movement controls
    if cp.pressing(['a']):
        move_player(-5, 0)
    if cp.pressing(['d']):
        move_player(5, 0)
    if cp.pressing(['e']):
        move_player(0, -5)
    if cp.pressing(['s']):
        move_player(0, 5)

    # Shooting controls
    if cp.pressing([';']):  # Up
        bullets.append(Bullet(player.x + 3, player.y - 5, 0, -5))
    if cp.pressing(['.']):  # Down
        bullets.append(Bullet(player.x + 3, player.y + tile_size, 0, 5))
    if cp.pressing([',']):  # Left
        bullets.append(Bullet(player.x - 5, player.y + 3, -5, 0))
    if cp.pressing(['/']):  # Right
        bullets.append(Bullet(player.x + tile_size, player.y + 3, 5, 0))

    time.sleep(0.01)
