import machine
import os
import sdcard

# Define SPI and CS pins
spi = machine.SPI(2, baudrate=1000000, sck=machine.Pin(40), mosi=machine.Pin(14), miso=machine.Pin(39))
cs = machine.Pin(12, machine.Pin.OUT)

# Initialize and mount SD card
sd = sdcard.SDCard(spi, cs)
os.mount(sd, "/sd")

# List files to confirm contents
print("Files on SD card:", os.listdir("/sd"))

# Correct filename from SD card directory
file_path = "/sd/sample-15s.wav"

# Check if file exists before opening
if file_path.split("/")[-1] in os.listdir("/sd"):
    with open(file_path, "rb") as file:
        data = file.read(100)  # Read first 100 bytes
        print("First 100 bytes of file:", data)
else:
    print(f"Error: File '{file_path}' not found!")

# Unmount SD card
os.umount("/sd")
