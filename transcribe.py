from faster_whisper import WhisperModel

model = WhisperModel("small", compute_type="int8")

segments, info = model.transcribe("HIN_M_AvdheshT.wav")

print("Information regarding the audio file - ", info)

with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(f"Detected language: {info.language}\n\n")

    for segment in segments:
        line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
        
        print(line.strip())   # still prints to console (optional)
        f.write(line)         # writes to file

