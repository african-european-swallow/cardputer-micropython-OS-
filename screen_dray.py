# Draw a filled rectangle (x, y, width, height, color)

from machine import Pin, SPI
import st7789py as st7789
import random
from font import vga2_16x32 as font
import time
import math
tft = st7789.ST7789(
    SPI(2, baudrate=40000000, sck=Pin(36), mosi=Pin(35), miso=None),
    135,
    240,
    reset=Pin(33, Pin.OUT),
    cs=Pin(37, Pin.OUT),
    dc=Pin(34, Pin.OUT),
    backlight=Pin(38, Pin.OUT),
    rotation=0,
    color_order=st7789.BGR
    )
tft.fill(st7789.color565(0, 0, 255))

# Draw a red filled rectangle
tft.fill_rect(20, 20, 100, 50, st7789.color565(255, 0, 0))

# Draw a green border rectangle
tft.rect(20, 80, 100, 50, st7789.color565(0, 255, 0))

# Draw a blue line
tft.line(10, 150, 150, 150, st7789.color565(0, 0, 255))

# Function to draw a polygon by connecting points
def draw_polygon(points, color):
    # Draw lines between each consecutive pair of points
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]  # Connect last point back to the first
        tft.line(x1, y1, x2, y2, color)

# Clear the screen with black
tft.fill(st7789.color565(0, 0, 0))

# Draw a triangle with vertices at (50, 50), (150, 50), (100, 150)
def draw_line(x1, y1, x2, y2, color):
    tft.line(x1, y1, x2, y2, color)

# Optimized function to fill a triangle (skip every other row)
def fill_triangle_skip_rows(x1, y1, x2, y2, x3, y3, color):
    # Sort the points by their y-coordinates (ascending)
    points = sorted([(x1, y1), (x2, y2), (x3, y3)], key=lambda p: p[1])

    # Unpack the points after sorting
    (x1, y1), (x2, y2), (x3, y3) = points

    # Calculate the slopes of the two sides
    def interpolate(x1, y1, x2, y2, y):
        if y2 == y1:  # Prevent division by zero
            return x1
        return x1 + (y - y1) * (x2 - x1) / (y2 - y1)

    # Fill the upper half (from the top vertex to the middle horizontal edge)
    for y in range(y1, y2 + 1, 2):  # Skip every other row (step=2)
        x_left = interpolate(x1, y1, x2, y2, y)
        x_right = interpolate(x1, y1, x3, y3, y)
        for x in range(int(x_left), int(x_right) + 1):
            tft.pixel(x, y, color)

    # Fill the lower half (mirror the top half)
    for y in range(y2, y3 + 1, 2):  # Skip every other row (step=2)
        x_left = interpolate(x2, y2, x3, y3, y)
        x_right = interpolate(x1, y1, x3, y3, y)
        for x in range(int(x_left), int(x_right) + 1):
            tft.pixel(x, y, color)

# Clear the screen with black
tft.fill(st7789.color565(0, 0, 0))

# Define the vertices of the triangle
x1, y1 = 50, 50
x2, y2 = 150, 50
x3, y3 = 100, 150

# Fill the triangle with a color, skipping every other row
fill_triangle_skip_rows(x1, y1, x2, y2, x3, y3, st7789.color565(255, 165, 0))  # Orange

# Wait before exit
def draw_circle(x_center, y_center, radius, color):
    for angle in range(0, 360, 5):
        x = int(x_center + radius * math.cos(math.radians(angle)))
        y = int(y_center + radius * math.sin(math.radians(angle)))
        tft.pixel(x, y, color)

# Fill screen with black
tft.fill(st7789.color565(0, 0, 0))

# Draw a red line
tft.line(10, 10, 230, 230, st7789.color565(255, 0, 0))

# Draw a green rectangle
tft.fill_rect(50, 50, 100, 50, st7789.color565(0, 255, 0))

# Draw a blue circle
draw_circle(120, 120, 50, st7789.color565(0, 0, 255))

# Display text
# Wait for a few seconds before clearing the screen
time.sleep(5)

# Clear the screen with black
tft.fill(st7789.color565(0, 0, 0))
polygon_points = [(0, 0), (100, 0), (50, 100)]

# Set color in 565 format (e.g., Green)
color = st7789.color565(0, 255, 0)

# Position of the polygon (screen offset)
x_offset = 50
y_offset = 50

# Rotation angle in radians (e.g., 45 degrees)
rotation_angle = pi / 4  # 45 degrees in radians

# Draw the polygon with rotation and positioning
tft.polygon(polygon_points, x_offset, y_offset, color, angle=rotation_angle)

time.sleep(5) 



