import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def read_txt_as_string(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def build_prescription_from_transcript(file_path, model):
    conversation = read_txt_as_string("../transcripts/transcription.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            conversation = f.read().strip()
    except Exception as e:
        raise Exception(f"Error reading transcript file: {e}")

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

    try:
        response = model.generate_content(prompt)
        raw_output = response.text.strip()
    except Exception as e:
        raise Exception(f"Model generation failed: {e}")

    try:
        
        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1
        json_str = raw_output[start:end]

        structured_data = json.loads(json_str)
    except Exception as e:
        raise Exception(f"JSON parsing failed: {e}\nRaw output:\n{raw_output}")
    print(structured_data)
    return structured_data
