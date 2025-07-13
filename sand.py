import time
import cardputerlib as card
import machine
import mpu6050
import random

# Initialize MPU-6050
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(2))
try:
    mpu = mpu6050.MPU6050(i2c)
except Exception as e:
    card.clear()
    card.setfont('16x32')
    card.prinS('GYRO NOT FOUND', [0,0], [255,0,0])
    card.setfont('8x8')
    card.prinS(str(e), [0,30],[0,255,0])
    time.sleep(2)
    import sys
    sys.exit()
# Simulation grid
WIDTH, HEIGHT = 240, 135
grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Track active sand particles
sand_particles = set()

# Colors
BLACK = [0, 0, 0]
SAND_COLOR = [194, 178, 128]

# Function to place sand at random top positions
def add_sand():
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT-1)
    if grid[y][x] == 0:  # Place sand only if empty
        grid[y][x] = 1
        sand_particles.add((x, y))

# Read and normalize tilt data
def get_tilt():
    accel = mpu.get_accel()
    
    x_tilt = accel['y'] / -16384.0  # Left/Right tilt
    y_tilt = accel['x'] / -16384.0  # Up/Down tilt

    dx = int(x_tilt * 10)  # Sensitivity
    dy = int(y_tilt * 10)

    # Only move in a direction if the tilt is significant
    if abs(dx) < 1:
        dx = 0
    if abs(dy) < 1:
        dy = 0

    return dx, dy

# Sand physics
def update_grid():
    dx, dy = get_tilt()
    
    # Stop if there's no tilt at all
    if dx == 0 and dy == 0:
        return []

    updated_pixels = []
    new_positions = set()

    # Move only active sand particles
    for x, y in list(sand_particles):  # Convert to list to allow modification
        new_x, new_y = x, y  # Start with current position

        # Apply movement **only** if tilt is nonzero in that direction
        if dx != 0:
            temp_x = x + dx
            if 0 <= temp_x < WIDTH and grid[y][temp_x] == 0:  # Ensure empty space
                new_x = temp_x

        if dy != 0:
            temp_y = y + dy
            if 0 <= temp_y < HEIGHT and grid[temp_y][new_x] == 0:  # Ensure empty space
                new_y = temp_y

        # Only update if movement happened
        if (new_x, new_y) != (x, y):
            grid[y][x] = 0
            grid[new_y][new_x] = 1
            updated_pixels.append((x, y, new_x, new_y))
            new_positions.add((new_x, new_y))
        else:
            new_positions.add((x, y))  # Stay in place if no movement

    sand_particles.clear()
    sand_particles.update(new_positions)

    return updated_pixels

# Render function (only updates changed pixels)
def render(updated_pixels):
    for x, y, new_x, new_y in updated_pixels:
        card.pixel(x, y, BLACK)  # Clear old position
        card.pixel(new_x, new_y, SAND_COLOR)  # Draw new position

# Main loop
card.clear()
while True:
    if card.pressing(['any']):  # Add sand when button is pressed
        add_sand()
    if card.button():
        sand_particles.clear()
        card.clear()
    updated_pixels = update_grid()
    render(updated_pixels)
    time.sleep(0.05)

