import math, time
import os
from cardputerlib import fbline, initbuff, fbdraw, pressing, fill, fbclear, button, clear, prinS, imput, dpad, removebuff  # Using your cardputerlib functions
removebuff()
initbuff()
# Screen center
W, H = 240, 135
CX, CY = W // 2, H // 2

# Rotate around Y axis
def rotate_y(x, z, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return x * cos_a - z * sin_a, x * sin_a + z * cos_a

# Rotate around X axis
def rotate_x(y, z, angle):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return y * cos_a - z * sin_a, y * sin_a + z * cos_a

# Project 3D to 2D
def project(x, y, z, fov=100, viewer_distance=3.4932):
    factor = fov / (viewer_distance + z)
    return int(CX + x * factor), int(CY + y * factor)

# Draw a shape
def draw_shape(vertices, edges, angle_x, angle_y, color=[255, 255, 255]):  # clear framebuffer instead of screen
    global foc
    projected = []
    fbclear()
    for x, y, z in vertices:
        y, z = rotate_x(y, z, angle_x)
        x, z = rotate_y(x, z, angle_y)
        px, py = project(x, y, z, fov=foc)
        projected.append((px, py))
    for a, b in edges:
        x1, y1 = projected[a]
        x2, y2 = projected[b]
        fbline(x1, y1, x2, y2, color)
    fill([0, 0, 0])
    fbdraw(0,0)  # push framebuffer to screen

# Make a cube
def make_cube(size=1.5):
    s = size / 2
    vertices = [
        [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],
        [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s],
    ]
    edges = [
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7),
    ]
    return vertices, edges

def make_diamond(size=1.5):
    s = size / 2
    vertices = [
        [0, s, 0],        # 0 top point
        [-s, 0, -s],      # 1 back-left
        [s, 0, -s],       # 2 back-right
        [s, 0, s],        # 3 front-right
        [-s, 0, s],       # 4 front-left
        [0, -s, 0],       # 5 bottom point
    ]
    edges = [
        (0,1), (0,2), (0,3), (0,4),  # top to base
        (1,2), (2,3), (3,4), (4,1),  # base square
        (5,1), (5,2), (5,3), (5,4),  # bottom to base
    ]
    return vertices, edges
def make_bowtie(size=1.5):
    s = size / 2  # Half size for scaling
    vertices = [
        [0, 0, -s],    # center back (z negative)
        [0, 0, s],     # center front (z positive)
        [-s, 0, 0],    # left side
        [s, 0, 0],     # right side
        [0, s, 0],     # top side
        [0, -s, 0],    # bottom side
        [-s*1.5, 0, 0],  # left wing outward
        [s*1.5, 0, 0],   # right wing outward
        [0, 0, -s*1.5],  # back point (behind the central z plane)
    ]
    
    edges = [
        (0, 1),  # center front to back
        (0, 2), (0, 3), (0, 4), (0, 5),  # center to all sides
        (2, 6), (3, 7),  # left to left wing, right to right wing
        (6, 8), (7, 8),  # wing points meeting at the back
        (5, 8), (4, 8)   # top and bottom meeting at back
    ]
    
    return vertices, edges

def make_something(size=1.5):
    s = size / 2  # Half size for scaling
    vertices = [
        [0, 0, s*1.5],  # Top point (above center, along Z-axis)
        [-s, -s, 0],     # Bottom-left (flat in the middle)
        [s, -s, 0],      # Bottom-right (flat in the middle)
        [s, s, 0],       # Top-right (flat in the middle)
        [-s, s, 0],      # Top-left (flat in the middle)
        [0, 0, -s*1.5]   # Bottom point (below center, along Z-axis)
    ]
    
    edges = [
        (0, 1), (0, 2), (0, 3), (0, 4),  # top to bottom square points
        (1, 2), (2, 3), (3, 4), (4, 1),  # bottom square edges
        (5, 1), (5, 2), (5, 3), (5, 4)   # bottom point to square
    ]
    
    return vertices, edges
def draw_piramid(size=1.5):
    s = size / 2  # Half size for scaling
    vertices = [
        [-s, -s, -s],  # base bottom-left
        [ s, -s, -s],  # base bottom-right
        [ s,  s, -s],  # base top-right
        [-s,  s, -s],  # base top-left
        [0, 0, s],     # top point (centered above base)
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # base square
        (0, 4), (1, 4), (2, 4), (3, 4),  # sides going up to the tip
    ]
    
    return vertices, edges
def load_shape_from_file(filename):
    vertices = []
    edges = []
    mode = None
    size = 1.0  # default scale if not in file

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith('/'):
                continue
            if not line or line.startswith("#"):
                if "s" in line:
                    mode = "size"
                elif "v" in line:
                    mode = "vertices"
                elif "e" in line:
                    mode = "edges"
                continue

            if mode == "size":
                size = float(line)
            elif mode == "vertices":
                y, z, x = map(float, line.split(","))
                print(f'[{x},{y},{z}')
                vertices.append([x * size, y * size, z * size])
            elif mode == "edges":
                a, b = map(int, line.split(","))
                edges.append((a, b))

    return vertices, edges


# Setup
def run():
    global foc
    foc = 100
    clear()
    prinS("Available files:", [0, 0], [255, 255, 255])
    lists = []
    for file in os.listdir():
        if file.endswith('3d.txt'):
            lists.append(file)
    prinS(', '.join(lists), [0, 8], [255, 255, 255])
    filename = imput('Enter filename to edit or "del": ', [0, 112], [255, 255, 255])
    if filename == 'exit' or pressing(['ESC']):
        return
    vertices, edges = load_shape_from_file(filename)
    angle_x = 0
    angle_y = 0
    draw_shape(vertices, edges, angle_x, angle_y)
    # Main loop
    
    while True:
        eas = dpad()
        if eas == 'LEFT':
            angle_y += 0.1
        elif eas == 'RIGHT':
            angle_y -= 0.1
        elif eas == 'DOWN':
            angle_x += 0.1
        elif eas == 'UP':
            angle_x -= 0.1
        
        time.sleep(0.03)
        if button():
            break
        if pressing(['BSPC', 'ESC', '`']):
            run()
            break
        bu = None
        if pressing(['=']):
            bu = True
            foc+=1
        if pressing(['_']):
            bu=True
            foc-=1
        if foc < 1:
            foc=1
        if eas != None or bu:
            draw_shape(vertices, edges, angle_x, angle_y)
run()


