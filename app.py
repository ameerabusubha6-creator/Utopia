import os
import json
import streamlit as st
from google import genai
from dotenv import load_dotenv

load_dotenv()

# ==========================
# CONFIG
# ==========================

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# ==========================
# PAGE
# ==========================

st.set_page_config(page_title="Utopia Studio Agent")
st.title("Utopia Studio – Marketing Agent")
st.caption("Paste a meeting transcript and the agent generates launch content automatically.")

transcript = st.text_area("Meeting Transcript", height=250, placeholder="Paste your Granola transcript here...")

# ==========================
# RUN AGENT
# ==========================

if st.button("Generate Content", type="primary"):
    if not transcript.strip():
        st.warning("Please paste a transcript first.")
    else:
        with st.spinner("Agent is thinking..."):

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

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            # Parse JSON
            try:
                result = json.loads(response.text.strip().strip("```json").strip("```"))
            except json.JSONDecodeError:
                st.error("Agent returned invalid JSON. Raw output below:")
                st.code(response.text)
                st.stop()

        # ==========================
        # DISPLAY RESULTS
        # ==========================

        st.success(f"Launch Stage: **{result['launch_stage']}**")

        st.subheader("LinkedIn Post")
        st.text_area("", value=result["linkedin_post"], height=150, key="linkedin")

        st.subheader("Follow-up Email")
        st.text_area("", value=result["follow_up_email"], height=200, key="email")

        st.subheader("Press Angle")
        st.info(result["press_angle"])

        # Save output
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        st.caption("✅ Saved to output.json")
