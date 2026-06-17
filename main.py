import os
import json
from google import genai
from dotenv import load_dotenv

# ==========================
# CONFIG
# ==========================

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ==========================
# LOAD TRANSCRIPT
# ==========================

with open("sample_transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

# ==========================
# PROMPT
# ==========================

prompt = f"""
You are Utopia Studio's Marketing & Events Agent.

Using the transcript below:

1. Determine the most appropriate LAUNCH stage:
   - Lead, Amplify, Unify, Nurture, Convert, Harvest

2. Create:
   - One LinkedIn post in Utopia Studio voice
   - One personalized follow-up email to the key attendee
   - One concise press-angle sentence for a journalist

Rules:
- Be specific and professional.
- Avoid generic AI language.
- Sound like a venture studio.
- Return ONLY valid JSON (no markdown fences).

JSON format:
{{
  "launch_stage": "",
  "linkedin_post": "",
  "follow_up_email": "",
  "press_angle": ""
}}

Transcript:
{transcript}
"""

# ==========================
# RUN AGENT
# ==========================

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

result = json.loads(response.text.strip().strip("```json").strip("```"))

# ==========================
# DISPLAY
# ==========================

print("\n=== AGENT OUTPUT ===\n")
print(json.dumps(result, indent=2))

# ==========================
# SAVE OUTPUT
# ==========================

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("\nSaved to output.json")