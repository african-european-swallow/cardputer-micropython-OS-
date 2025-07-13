import time
import machine
import cardputerlib as card
from mpu6050 import MPU6050

# Initialize I2C and MPU6050
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(2))
try:
    mpu = MPU6050(i2c)
except Exception as e:
    card.clear()
    card.setfont('16x32')
    card.prinS('GYRO NOT FOUND', [0,0], [255,0,0])
    card.setfont('8x8')
    card.prinS(str(e), [0,30],[0,255,0])
    time.sleep(2)
    import sys
    sys.exit()
# Constants
WIDTH, HEIGHT = 240, 135
CENTER_Y = HEIGHT // 2
NUM_POINTS = WIDTH  # One data point per pixel column

# Initialize graph storage, starting on the far right of the screen
history_x = [CENTER_Y] * NUM_POINTS
history_y = [CENTER_Y] * NUM_POINTS
history_z = [CENTER_Y] * NUM_POINTS

# Reduced threshold for detecting smaller movements
CHANGE_THRESHOLD = 1  # Set to 1 for very sensitive movement detection

def map_value(value, in_min, in_max, out_min, out_max):
    """Maps value from one range to another."""
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def draw_graph():
    """Continuously updates and graphs accelerometer data."""
    card.clear()
    
    prev_ax, prev_ay, prev_az = 0, 0, 0  # Initialize previous values for comparison
    
    while True:
        # Read accelerometer values
        accel = mpu.get_accel()
        
        # Map accelerometer values to a larger vertical range (from center to edges)
        ax = map_value(accel['x'], -32768, 32767, 0, HEIGHT)
        ay = map_value(accel['y'], -32768, 32767, 0, HEIGHT)
        az = map_value(accel['z'], -32768, 32767, 0, HEIGHT)
        
        # Check if the change in any axis is greater than the reduced threshold
        if abs(ax - prev_ax) > CHANGE_THRESHOLD or abs(ay - prev_ay) > CHANGE_THRESHOLD or abs(az - prev_az) > CHANGE_THRESHOLD:
            # Shift history right
            for i in range(NUM_POINTS - 1, 0, -1):
                history_x[i] = history_x[i - 1]
                history_y[i] = history_y[i - 1]
                history_z[i] = history_z[i - 1]
            
            # Add new values at the leftmost position
            history_x[0] = ax
            history_y[0] = ay
            history_z[0] = az

            # Redraw the graph only if significant change occurred
            card.clear()
            for i in range(NUM_POINTS - 1):
                # Only draw the line if the value is non-zero (or non-CENTER_Y)
                if history_x[i] != CENTER_Y and history_x[i + 1] != CENTER_Y:
                    card.line(i, history_x[i], i + 1, history_x[i + 1], [255, 0, 0])  # Red for X axis
                if history_y[i] != CENTER_Y and history_y[i + 1] != CENTER_Y:
                    card.line(i, history_y[i], i + 1, history_y[i + 1], [0, 255, 0])  # Green for Y axis
                if history_z[i] != CENTER_Y and history_z[i + 1] != CENTER_Y:
                    card.line(i, history_z[i], i + 1, history_z[i + 1], [0, 0, 255])  # Blue for Z axis

            # Store current values as previous for next iteration
            prev_ax, prev_ay, prev_az = ax, ay, az

        time.sleep(0.1)  # Refresh rate

# Start the graphing function
draw_graph()
