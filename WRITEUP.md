# Utopia Studio – Marketing & Events Agent

---

## Operator & Problem

The Marketing & Events lead at Utopia Studio (Sarah) sits in founder meetings, takes notes via Granola, then manually writes LinkedIn posts, follow-up emails, and press angles after every call — often juggling five to eight meetings a week. Each write-up takes 20–30 minutes: re-reading the transcript, deciding which LAUNCH stage the deal is in, and drafting three different outputs in the studio's voice. That is roughly two to four hours per week spent on repetitive content generation instead of relationship-building and strategy. The quality also drops on busy weeks — posts become generic, emails lose the personal details discussed in the meeting.

---

## The Agent

The agent takes a raw meeting transcript as input (pasted text or loaded from file) and produces four outputs in a single JSON response: the LAUNCH stage classification (Lead / Amplify / Unify / Nurture / Convert / Harvest), a LinkedIn post in Utopia Studio's voice, a personalized follow-up email addressed to the key attendee, and a one-sentence press angle for journalist outreach. It calls the **Google Gemini 2.5 Flash API** via the `google-genai` Python SDK with a single structured prompt that enforces JSON-only output. The Streamlit web UI lets Sarah paste a transcript and get all four deliverables in under 10 seconds, with a download button for the JSON.

---

## Sample Input (verbatim)

```
Attendees: Sarah (Utopia Studio),
Omar (Founder of LogiFlow)
Sarah: Tell me about the biggest problem you're seeing in Qatar logistics.
Omar: Mid-sized logistics companies still manage dispatching manually. Drivers use WhatsApp, spreadsheets, and phone calls. Delays are hard to track.
Sarah: What's the opportunity?
Omar: An AI-powered dispatch platform that predicts delays, assigns drivers automatically, and gives managers a live dashboard.
Sarah: Have you spoken to customers?
Omar: We've interviewed 12 companies so far. Most said they would pay if it reduced delivery delays by at least 15%.
Sarah: That's interesting because Qatar is investing heavily in logistics infrastructure.
Omar: Exactly. We think the market is ready for a regional logistics operating system.
```

---

## Sample Output (verbatim)

```json
{
  "launch_stage": "Amplify",
  "linkedin_post": "Fascinating discussions are emerging from the MENA region! We're seeing immense potential in Qatar's rapidly expanding logistics sector, particularly for AI-powered solutions. The inefficiencies of manual dispatching, highlighted by industry insights, present a ripe opportunity for platforms that can predict delays and automate operations, driving significant efficiency gains. This is precisely the kind of market-ready innovation Utopia Studio seeks to amplify and empower. #AI #Logistics #Innovation #Qatar #VentureStudio #FutureofLogistics #MENA",
  "follow_up_email": "Subject: Advancing LogiFlow's Vision: Our Next Steps\n\nDear Omar,\n\nIt was truly inspiring to connect with you today and dive deep into LogiFlow's vision for transforming Qatar's logistics landscape. Your insights into the challenges of manual dispatching and the market readiness for an AI-powered solution resonated strongly with our team at Utopia Studio.\n\nWe're particularly impressed by your initial customer validation, confirming the strong interest in a platform that could reduce delivery delays by 15% or more. Given Qatar's significant investments in logistics infrastructure, your concept of a regional logistics operating system feels incredibly timely and impactful.\n\nWe see compelling potential in LogiFlow and would love to explore this further. Our next step would be to schedule a deeper strategic session to outline how Utopia Studio's resources – from technical expertise to market access and venture building methodologies – could accelerate LogiFlow's journey from concept to market leader.\n\nPlease let me know what your availability looks like next week for a follow-up call.\n\nBest regards,\n\n[Your Name/Sarah]\nMarketing & Events Agent\nUtopia Studio",
  "press_angle": "Utopia Studio is exploring a pioneering AI-powered dispatch platform set to revolutionize Qatar's logistics sector by automating operations and predicting delays, addressing a critical market need for enhanced efficiency and regional growth."
}
```

---

## What I Cut

- **Multi-turn conversation mode.** Considered letting the user ask follow-up questions ("make the email shorter", "add a CTA"). Cut it because it adds session-state complexity and the single-shot output is already production-usable — Sarah can edit in LinkedIn directly.
- **Automatic Granola/Notion integration.** Considered pulling transcripts directly from Granola's API or a Notion database. Cut it because Granola has no public API, and the clipboard-paste flow is fast enough for an MVP that proves the value.
- **Multiple LLM comparison.** Considered running the prompt against GPT-4o and Claude in parallel to let the user pick the best output. Cut it because it triples cost and latency for marginal quality difference — Gemini 2.5 Flash is fast, cheap, and produces strong structured output.

---

## What Broke or Surprised Me

- **Gemini sometimes wraps JSON in markdown fences** (` ```json ... ``` `) even when the prompt explicitly says "no markdown fences." I had to add stripping logic (`strip("```json").strip("```")`) to handle this reliably. The newer `google-genai` SDK does not fix this at the API level.
- **The deprecated `google.generativeai` library vs the new `google.genai` SDK.** All the top Google AI tutorials still reference the old library. I wasted time on import errors before discovering the migration to `google-genai`. The new SDK's API surface (`client.models.generate_content`) is cleaner but poorly documented.
- **LAUNCH stage classification is subjective.** The model occasionally classifies the same transcript as "Lead" or "Amplify" on different runs. Without a ground-truth dataset of stage-labeled transcripts, there is no way to fine-tune this — it is an inherent ambiguity in the framework itself, not a model failure.

---

## If I Had Two More Days

- **Add a tone/style selector.** Let the operator choose between "formal studio voice," "casual founder update," and "investor-facing" — each would modify the system prompt to shift the output register. This directly multiplies the agent's utility without adding new API calls.
- **Batch processing mode.** Accept a folder of transcript files (or a CSV export from Granola) and generate all outputs in one run, saving results as a structured spreadsheet. This turns a per-meeting tool into a weekly workflow.
- **Slack integration.** Post the LinkedIn draft and email directly to a `#marketing-drafts` Slack channel via webhook, so the team can review and approve without opening the Streamlit app. This is the fastest path to real adoption inside the studio.
