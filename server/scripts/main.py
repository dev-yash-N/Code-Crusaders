import os
from mic import record_audio
from transcribe import transcribe_audio
from processorGEMINI import build_prescription_from_transcript

AUDIO_PATH = "../audio/RealSample.wav"
TRANSCRIPT_PATH = "../transcripts/transcription.txt"


def check_file(path, step):
    if not os.path.exists(path):
        raise Exception(f"{step} failed. File not found: {path}")
    if os.path.getsize(path) == 0:
        raise Exception(f"{step} failed. File is empty: {path}")
    print(f"✅ {step} completed")


def main():
    try:
        print("\n=== 🎤 RECORDING ===")
        record_audio(AUDIO_PATH)

        check_file(AUDIO_PATH, "Recording")

        print("\n=== 📝 TRANSCRIPTION ===")
        transcribe_audio(AUDIO_PATH, TRANSCRIPT_PATH)

        check_file(TRANSCRIPT_PATH, "Transcription")

        print("\n=== 🧠 LLM PROCESSING ===")
        result = build_prescription_from_transcript(TRANSCRIPT_PATH)

        print("\n=== ✅ FINAL OUTPUT ===")
        print(result)

    except Exception as e:
        print(f"\n🔥 ERROR: {e}")


if __name__ == "__main__":
    main()