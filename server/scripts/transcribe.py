from faster_whisper import WhisperModel

model = WhisperModel("small", compute_type="int8")


def transcribe_audio(input_path, output_path):
    segments, info = model.transcribe(input_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Detected language: {info.language}\n\n")

        for segment in segments:
            line = f"{segment.text}\n"
            print(line.strip())
            f.write(line)

    print(f"✅ Transcript saved at {output_path}")