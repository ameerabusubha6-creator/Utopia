# Utopia Studio – Marketing & Events Agent

> An AI agent that reads meeting transcripts and instantly generates launch-stage content: LinkedIn posts, follow-up emails, and press angles — powered by Gemini 2.5 Flash.

---

## How to Run

### 1. Clone the repo
```bash
git clone https://github.com/ameerabusubha6-creator/Utopia.git
cd Utopia
```

### 2. Install dependencies
```bash
pip install streamlit google-genai python-dotenv
```

### 3. Set up your API key
```bash
cp .env.example .env
# Open .env and paste your Gemini API key
```

### 4. Run the Streamlit app
```bash
python -m streamlit run app.py
```

Or run the CLI version:
```bash
python main.py
```

---

## Prompt Used

```
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
{
  "launch_stage": "",
  "linkedin_post": "",
  "follow_up_email": "",
  "press_angle": ""
}

Transcript:
{transcript}
```

---

## Tools & APIs Called

| Tool / API | Purpose |
|---|---|
| **Google Gemini 2.5 Flash** (`google-genai`) | Core LLM — generates all content from the transcript |
| **Streamlit** | Web UI — text input, results display, download button |
| **python-dotenv** | Loads `GEMINI_API_KEY` from `.env` file securely |

---

## Architecture Diagram

```
User pastes transcript
        │
        ▼
┌─────────────────────┐
│   Streamlit UI      │  ← app.py
│  (text input box)   │
└────────┬────────────┘
         │ prompt + transcript
         ▼
┌─────────────────────┐
│  Google Gemini API  │  ← gemini-2.5-flash
│  (LLM Inference)    │
└────────┬────────────┘
         │ JSON response
         ▼
┌─────────────────────┐
│   Parsed Output     │
│  - Launch Stage     │
│  - LinkedIn Post    │
│  - Follow-up Email  │
│  - Press Angle      │
└────────┬────────────┘
         │
         ▼
   Displayed in UI
   + saved to output.json
```

---

## Project Structure

```
Utopia/
├── app.py                  # Streamlit web app
├── main.py                 # CLI script
├── sample_transcript.txt   # Example meeting transcript
├── .env.example            # Template for environment variables
├── .gitignore              # Keeps .env out of version control
└── README.md               # This file
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key — get one at [aistudio.google.com](https://aistudio.google.com) |