import os
import struct
from machine import I2S, Pin

class WavPlayer:
    PLAY = 0
    PAUSE = 1
    RESUME = 2
    FLUSH = 3
    STOP = 4 

    def __init__(self, id, sck_pin, ws_pin, sd_pin, ibuf, root="/sd"):
        self.id = id
        self.sck_pin = sck_pin
        self.ws_pin = ws_pin
        self.sd_pin = sd_pin
        self.ibuf = ibuf
        self.root = root.rstrip("/") + "/"
        self.state = WavPlayer.STOP
        self.wav = None
        self.loop = False
        self.format = None
        self.sample_rate = None
        self.bits_per_sample = None
        self.first_sample_offset = None
        self.num_read = 0
        self.sbuf = 1000
        self.nflush = 0
        self.volume = 1.0  # Default to max volume

        # allocate a small array of blank audio samples used for silence
        self.silence_samples = bytearray(self.sbuf)

        # allocate audio sample array buffer
        self.wav_samples_mv = memoryview(bytearray(10000))

    def set_volume(self, volume):
        """Set volume level (0.0 to 1.0)."""
        if 0.0 <= volume <= 1.0:
            self.volume = volume
        else:
            raise ValueError("Volume must be between 0.0 and 1.0")

    def i2s_callback(self, arg):
        if self.state == WavPlayer.PLAY:
            self.num_read = self.wav.readinto(self.wav_samples_mv)
            if self.num_read == 0:  # End of file
                if not self.loop:
                    self.state = WavPlayer.FLUSH
                else:
                    _ = self.wav.seek(self.first_sample_offset)
                _ = self.audio_out.write(self.silence_samples)
            else:
                if self.volume < 1.0:
                    shift = int((1.0 - self.volume) * 8)  # Convert volume to bit shift
                    samples = memoryview(self.wav_samples_mv[:self.num_read])
                    for i in range(0, len(samples), 2):
                        sample = int.from_bytes(samples[i:i+2], 'little', signed=True)
                        sample = sample >> shift  # Fast volume adjustment using shift
                        samples[i:i+2] = sample.to_bytes(2, 'little', signed=True)
                _ = self.audio_out.write(self.wav_samples_mv[:self.num_read])
        elif self.state == WavPlayer.RESUME:
            self.state = WavPlayer.PLAY
            _ = self.audio_out.write(self.silence_samples)
        elif self.state == WavPlayer.PAUSE:
            _ = self.audio_out.write(self.silence_samples)
        elif self.state == WavPlayer.FLUSH:
            if self.nflush > 0:
                self.nflush -= 1
                _ = self.audio_out.write(self.silence_samples)
            else:
                self.wav.close()
                self.audio_out.deinit()
                self.state = WavPlayer.STOP
        elif self.state == WavPlayer.STOP:
            pass
        else:
            raise SystemError("Internal error: unexpected state")
            self.state == WavPlayer.STOP

    def parse(self, wav_file):
        chunk_ID = wav_file.read(4)
        if chunk_ID != b"RIFF":
            raise ValueError("WAV chunk ID invalid")
        chunk_size = wav_file.read(4)
        format = wav_file.read(4)
        if format != b"WAVE":
            raise ValueError("WAV format invalid")
        sub_chunk1_ID = wav_file.read(4)
        if sub_chunk1_ID != b"fmt ":
            raise ValueError("WAV sub chunk 1 ID invalid")
        sub_chunk1_size = wav_file.read(4)
        audio_format = struct.unpack("<H", wav_file.read(2))[0]
        num_channels = struct.unpack("<H", wav_file.read(2))[0]

        if num_channels == 1:
            self.format = I2S.MONO
        else:
            self.format = I2S.STEREO

        self.sample_rate = struct.unpack("<I", wav_file.read(4))[0]
        byte_rate = struct.unpack("<I", wav_file.read(4))[0]
        block_align = struct.unpack("<H", wav_file.read(2))[0]
        self.bits_per_sample = struct.unpack("<H", wav_file.read(2))[0]

        binary_block = wav_file.read(200)
        offset = binary_block.find(b"data")
        if offset == -1:
            raise ValueError("WAV sub chunk 2 ID not found")

        self.first_sample_offset = 44 + offset

    def play(self, wav_file, loop=False):
        if os.listdir(self.root).count(wav_file) == 0:
            raise ValueError("%s: not found" % wav_file)
        if self.state == WavPlayer.PLAY:
            raise ValueError("already playing a WAV file")
        elif self.state == WavPlayer.PAUSE:
            raise ValueError("paused while playing a WAV file")
        else:
            self.wav = open(self.root + wav_file, "rb")
            self.loop = loop
            self.parse(self.wav)

            self.audio_out = I2S(
                self.id,
                sck=self.sck_pin,
                ws=self.ws_pin,
                sd=self.sd_pin,
                mode=I2S.TX,
                bits=self.bits_per_sample,
                format=self.format,
                rate=self.sample_rate,
                ibuf=self.ibuf,
            )

            _ = self.wav.seek(self.first_sample_offset)
            self.audio_out.irq(self.i2s_callback)
            self.nflush = self.ibuf // self.sbuf + 1
            self.state = WavPlayer.PLAY
            _ = self.audio_out.write(self.silence_samples)

    def resume(self):
        if self.state != WavPlayer.PAUSE:
            raise ValueError("can only resume when WAV file is paused")
        else:
            self.state = WavPlayer.RESUME

    def pause(self):
        if self.state == WavPlayer.PAUSE:
            pass
        elif self.state != WavPlayer.PLAY:
            raise ValueError("can only pause when WAV file is playing")

        self.state = WavPlayer.PAUSE

    def stop(self):
        self.state = WavPlayer.FLUSH

    def isplaying(self):
        return self.state != WavPlayer.STOP
