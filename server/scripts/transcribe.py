from faster_whisper import WhisperModel

model = WhisperModel("small", compute_type="int8")

segments, info = model.transcribe("../audio/[YOUR_FILE.wav]")


with open("../transcripts/[YOUR_FILE_TRANSCRIPT].txt", "w", encoding="utf-8") as f:
    f.write(f"Detected language: {info.language}\n\n")

    for segment in segments:
        line = f"{segment.text}\n"
        
        print(line.strip())
        f.write(line)

