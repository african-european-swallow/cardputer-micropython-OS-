import machine
import os
import sdcard
import time
import struct
from machine import I2S, Pin

# === SPI & SD Card Setup ===
spi = machine.SPI(2, baudrate=1000000, sck=machine.Pin(40), mosi=machine.Pin(14), miso=machine.Pin(39))
cs = machine.Pin(12, machine.Pin.OUT)

sd = sdcard.SDCard(spi, cs)
os.mount(sd, "/sd")

# === I2S Pins ===
SCK_PIN = 41
WS_PIN = 43
SD_PIN = 42
I2S_ID = 1
BUFFER_LENGTH = 8192  # Experimenting with smaller buffer size for cleaner playback

# === Function to Parse WAV Header ===
def parse_wav_header(file):
    file.seek(0)  # Go to the beginning
    header = file.read(44)  # WAV header is 44 bytes

    # Unpack header using struct
    chunk_id, _, format, subchunk1_id, _, audio_format, num_channels, sample_rate, _, _, bits_per_sample, subchunk2_id, _ = struct.unpack('<4sI4s4sIHHIIHH4sI', header)

    if chunk_id != b'RIFF' or format != b'WAVE':
        raise ValueError("Invalid WAV file")

    print(f"Sample Rate: {sample_rate} Hz, Channels: {num_channels}, Bits: {bits_per_sample}")
    
    return sample_rate, num_channels, bits_per_sample

# === Function to Play WAV ===
def play_wav(filename):
    with open(filename, "rb") as file:
        sample_rate, num_channels, bits_per_sample = parse_wav_header(file)

        # Adjust the I2S configuration based on the file properties
        audio_out = I2S(
            I2S_ID,
            sck=Pin(SCK_PIN),
            ws=Pin(WS_PIN),
            sd=Pin(SD_PIN),
            mode=I2S.TX,
            bits=16,  # We will set it to 16 bits, assuming most WAVs are 16-bit
            format=I2S.MONO, #if num_channels == 2 else I2S.MONO,
            rate=sample_rate,  # Ensure correct sample rate
            ibuf=BUFFER_LENGTH,  # Buffer for audio streaming
        )

        # Skip the WAV header
        file.seek(44)

        # Read & stream audio data
        while True:
            data = file.read(BUFFER_LENGTH)
            if not data:
                break
            # Debugging: check data length
            print(f"Read {len(data)} bytes of audio data.")
            audio_out.write(data)

        audio_out.deinit()  # Clean up I2S

# === Play WAV File ===
try:
    play_wav("/sd/BabyElephantWalk60.wav")
except Exception as e:
    print("Error:", e)

os.umount("/sd")
print("Playback complete!")
