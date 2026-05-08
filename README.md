# Vapi HVAC Voice AI Receptionist

An AI-powered inbound voice receptionist for HVAC contractors, built with [Vapi](https://vapi.ai). The agent ("Joey") handles inbound calls, qualifies leads, books appointments, and routes emergencies — all without human intervention.

## What it does

- **Lead qualification** — Identifies whether the caller needs residential or commercial HVAC service
- **Appointment booking** — Checks availability and books jobs into Google Calendar
- **Emergency triage** — Routes urgent calls (no heat, no AC, gas smell, CO alarm) with appropriate urgency
- **Lead logging** — Records caller details and job type into Google Sheets
- **Service area validation** — Confirms the job is within the service radius (Mississauga, Brampton, Oakville, etc.)

## Tech stack

| Component | Technology |
|---|---|
| Voice AI platform | [Vapi](https://vapi.ai) |
| LLM | GPT-4.1 (OpenAI) |
| Transcription | Deepgram |
| Calendar | Google Calendar API |
| Lead logging | Google Sheets API |
| Webhooks / automation | Make.com |

## Project structure

```
├── prompts/
│   └── joey-system.md        # Full system prompt for the Joey persona
├── scripts/
│   ├── create-assistant.py   # Deploys assistant config to Vapi
│   ├── test-call.py          # Triggers a test inbound call
│   ├── check-joey.py         # Verifies assistant is live
│   ├── patch-model.py        # Updates LLM model on existing assistant
│   └── n8n-workflow.json     # n8n automation workflow
├── knowledge/
│   ├── polarcrest_hvac_knowledge_base.md   # Services, pricing, hours
│   └── northflow_hvac_knowledge_base.md    # Second client knowledge base
└── CLAUDE.md                 # Full spec and build instructions
```

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials:
   ```
   VAPI_API_KEY=your_vapi_api_key
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_CALENDAR_ID=your_calendar_id
   ```

2. Deploy the assistant to Vapi:
   ```bash
   python scripts/create-assistant.py
   ```

3. Trigger a test call:
   ```bash
   python scripts/test-call.py
   ```

## Key features

- Handles emergency calls with clear triage protocols (no heat in winter, gas smell → advise to call gas company)
- Graceful handoff to human when the AI can't help
- Bilingual-ready architecture
- Configurable for multiple HVAC clients (knowledge base swap)
