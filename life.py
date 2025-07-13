import time
import random
import cardputerlib as card
card.clear()
card.initbuff()
def create_grid(rows, cols):
    """Creates a grid of the specified size, initialized with random dead or alive cells."""
    return [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

def get_neighbors(grid, row, col):
    """Counts the number of live neighbors for a given cell."""
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            neighbor_row = (row + i) % len(grid)
            neighbor_col = (col + j) % len(grid[0])
            count += grid[neighbor_row][neighbor_col]
    return count

def next_generation(grid):
    """Generates the next generation of the game."""
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            neighbors = get_neighbors(grid, row, col)
            if grid[row][col] == 1:  # Live cell
                if neighbors < 2 or neighbors > 3:
                    new_grid[row][col] = 0
                else:
                    new_grid[row][col] = 1
            else:  # Dead cell
                if neighbors == 3:
                    new_grid[row][col] = 1
    return new_grid

def print_grid(grid):
    """Prints the current grid."""
    card.fbclear()
    for row in range(len(grid)):
        card.fbrect(row*4-1,0, 2,135, [0,0,0])
        for life in range(len(grid[row])):
            #print(life)
            #card.rect(row*4-1,0, 2,135, [0,0,0])
            if grid[row][life]:
                card.fbpixel(row*4,life*4, [255,255,255])
                card.fbpixel((row*4)-1, life*4, [255,255,255])
                card.fbpixel((row*4)-1,(life*4)-1, [255,255,255])
                card.fbpixel(row*4, (life*4)-1, [255,255,255])
            '''else:
                card.pixel(row*4,life*4, [0,0,0])
                card.pixel((row*4)-1, life*4, [0,0,0])
                card.pixel((row*4)-1,(life*4)-1, [0,0,0])
                card.pixel(row*4, (life*4)-1, [0,0,0])'''
    card.fbdraw(0,0)
        #print(row,'heheh')
        #print(''.join(['#' if cell else '.' for cell in grid[row]]))


rows = 60
cols = 33
cx = 0
cy = 0
grid = create_grid(rows, cols)
while True:
    if card.pressing(['`']):
        break
    print_grid(grid)
    if card.button():
        time.sleep(1)
        while True:
            print_grid(grid)
            if card.pressing([';']):
                cy -= 1
            if card.pressing(['.']):
                cy += 1
            if card.pressing([',']):
                cx -= 1
            if card.pressing(['/']):
                cx += 1
            if cx > 60:
                cx = 0
            if cx < 0:
                cx = 60
            if cy > 33:
                cy = 0
            if cy < 0:
                cy = 33
            if grid[cx][cy]:
                card.pixel(cx*4,cy*4, [0,0,255])
                card.pixel((cx*4)-1, cy*4, [0,0,255])
                card.pixel((cx*4)-1,(cy*4)-1, [0,0,255])
                card.pixel(cx*4, (cy*4)-1, [0,0,255])
            else:
                card.pixel(cx*4,cy*4, [255,0,0])
                card.pixel((cx*4)-1, cy*4, [255,0,0])
                card.pixel((cx*4)-1,(cy*4)-1, [255,0,0])
                card.pixel(cx*4, (cy*4)-1, [255,0,0])
            if card.pressing(['BSPC']):
                grid = [[0 for _ in range(cols)] for _ in range(rows)]
            if card.pressing(['ENT']):
                print(grid[cx][cy])
                grid[cx][cy] = not grid[cx][cy]
            if card.button():
                break
            time.sleep(0.09)
    grid = next_generation(grid)
    #print("\033[{}A".format(rows+1), end="") # Move cursor up to overwrite previous grid
    time.sleep(0.02)
    

