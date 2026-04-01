import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading

# Settings
sample_rate = 16000  # Whisper-friendly
channels = 1
output_file = "../audio/Audio.wav"

# Global flags
recording = True
paused = False

# Buffer to store recorded audio chunks
audio_buffer = []

def record():
    global recording, paused, audio_buffer
    print("🎤 Mic initialized. Press 'p' to pause/resume, 's' to stop.")

    def callback(indata, frames, time, status):
        global audio_buffer, paused
        if status:
            print(status)
        if not paused:
            audio_buffer.append(indata.copy())

    with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback):
        while recording:
            sd.sleep(100)  # keep stream alive

# Thread for recording
record_thread = threading.Thread(target=record)
record_thread.start()

# Control loop
try:
    while recording:
        cmd = input("Enter command (p=pause/resume, s=stop): ").strip().lower()
        if cmd == 'p':
            paused = not paused
            print("⏸️ Paused" if paused else "▶️ Resumed")
        elif cmd == 's':
            recording = False
except KeyboardInterrupt:
    recording = False

# Wait for thread to finish
record_thread.join()

# Combine chunks and save
if audio_buffer:
    audio_data = np.concatenate(audio_buffer, axis=0)
    write(output_file, sample_rate, audio_data)
    print(f"✅ Recording saved as {output_file}")
else:
    print("⚠️ No audio recorded")