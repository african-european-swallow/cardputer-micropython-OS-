import time
import random
from gamepad import SeesawGamepad
import cardputerlib as card  # your card library
card.initbuff()

# Constants
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 135
PLAYER_SIZE = 10
ENEMY_SIZE = 10

# Starting speed and interval
enemy_speed = 2.0
spawn_interval = 20.0

# Limits
MAX_ENEMY_SPEED = 8.0
MIN_SPAWN_INTERVAL = 5.0

# Scaling factor
DIFFICULTY_INCREMENT = 0.01

BUTTON_PINS = [0, 1, 2, 5, 6]
gamepad = SeesawGamepad(button_pins=BUTTON_PINS)
gamepad.setup()

def map_joystick_to_screen(val, max_screen):
    val = max(0, min(val, 1023))
    return int((val / 1023) * (max_screen - PLAYER_SIZE))

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_SIZE - 10

    def update(self, joy_x, joy_y):
        self.x = map_joystick_to_screen(1023 - joy_x, SCREEN_WIDTH)
        self.y = map_joystick_to_screen(joy_y, SCREEN_HEIGHT)

    def draw(self):
        card.fbrect(self.x, self.y, PLAYER_SIZE, PLAYER_SIZE, [0, 255, 0], fill=True)

class Enemy:
    def __init__(self, speed):
        self.x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        self.y = 0
        self.speed = speed

    def update(self):
        self.y += int(self.speed)

    def draw(self):
        card.fbrect(self.x, self.y, ENEMY_SIZE, ENEMY_SIZE, [255, 0, 0], fill=True)

    def offscreen(self):
        return self.y > SCREEN_HEIGHT

    def collides_with(self, player):
        return not (
            self.x > player.x + PLAYER_SIZE or
            self.x + ENEMY_SIZE < player.x or
            self.y > player.y + PLAYER_SIZE or
            self.y + ENEMY_SIZE < player.y
        )

def reset_game():
    global enemies, score, game_over, paused, spawn_timer, enemy_speed, spawn_interval
    enemies = []
    score = 0
    game_over = False
    paused = False
    spawn_timer = 0
    enemy_speed = 2.0
    spawn_interval = 20.0
    return enemies, score, game_over, paused, spawn_timer

enemies, score, game_over, paused, spawn_timer = reset_game()
player = Player()

while True:
    card.fbclear()
    joy_x, joy_y = gamepad.read_joystick()
    buttons = gamepad.read_buttons()

    if 2 in buttons:
        paused = not paused
        time.sleep(0.3)
    if 1 in buttons:
        enemies, score, game_over, paused, spawn_timer = reset_game()
    if 0 in buttons:
        break
    if not paused and not game_over:
        player.update(joy_x, joy_y)

        # Scale difficulty: spawn interval drops 2× faster than speed increases
        enemy_speed = min(MAX_ENEMY_SPEED, enemy_speed + DIFFICULTY_INCREMENT)
        spawn_interval = max(MIN_SPAWN_INTERVAL, spawn_interval - 64 * DIFFICULTY_INCREMENT)

        spawn_timer += 1
        if spawn_timer >= int(spawn_interval):
            spawn_timer = 0
            enemies.append(Enemy(enemy_speed))

        for enemy in enemies:
            enemy.update()

        removed = [e for e in enemies if e.offscreen()]
        score += len(removed)
        enemies = [e for e in enemies if not e.offscreen()]

        for enemy in enemies:
            if enemy.collides_with(player):
                game_over = True
                break

    player.draw()
    for enemy in enemies:
        enemy.draw()

    card.fbdraw(0, 0)
    card.prinS(f"Score: {score}", [5, 5], [255, 255, 255])
    if paused:
        card.prinS("PAUSED", [SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2], [255, 255, 0])
    if game_over:
        card.prinS("GAME OVER", [SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2], [255, 0, 0])
        card.prinS("Press Btn 1 to reset", [SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 20], [255, 255, 255])

    time.sleep(0.03)
