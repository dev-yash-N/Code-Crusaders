import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def extract_main_points(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            conversation = f.read()

        prompt = f"""
You are a clinical documentation assistant.

Extract structured EMR data from the conversation.

Return ONLY valid JSON with this schema:

{{
  "patient_details": {{
    "name": "",
    "age": "",
    "gender": ""
  }},
  "symptoms": [],
  "duration": "",
  "severity": "",
  "patient_history": "",
  "diagnosis": "",
  "medications": [],
  "tests_recommended": [],
  "doctor_notes": "",
  "referral_needed": "",
  "follow_up": ""
}}

Rules:
- Do NOT hallucinate
- Keep it concise
- If missing, return empty

Conversation:
{conversation}
"""

        response = client.responses.create(
    model="gpt-3.5-turbo",
    input=[{"role": "user", "content": prompt}]
)

        output_text = response.output_text

        try:
            return json.loads(output_text)
        except json.JSONDecodeError:
            print("Failed to parse JSON. Raw output:\n", output_text)
            return None

    except FileNotFoundError:
        print("File not found:", filepath)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    result = extract_main_points("../transcripts/transcription.txt")
    print(json.dumps(result, indent=4))