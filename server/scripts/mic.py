import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading

sample_rate = 16000  
channels = 1
output_file = "../audio/Audio.wav"

recording = True
paused = False

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

record_thread = threading.Thread(target=record)
record_thread.start()

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

record_thread.join()

if audio_buffer:
    audio_data = np.concatenate(audio_buffer, axis=0)
    write(output_file, sample_rate, audio_data)
    print(f"✅ Recording saved as {output_file}")
else:
    print("⚠️ No audio recorded")