# VapiCodeAI — Voice AI Receptionist (PolarCrest HVAC Solutions)

---

## What You'll Build

A fully working **AI phone receptionist** that:
- Answers inbound calls as "Joey" from PolarCrest HVAC Solutions
- Triages emergencies (gas leaks, no heat, CO alarms) and routes them instantly
- Qualifies leads by asking the right questions
- Books appointments into Google Calendar in real time
- Logs every lead into Google Sheets
- Sends you an email summary after every call
- Transfers callers to a human when needed

**Difficulty:** Beginner-friendly. No coding required — you paste commands and run scripts.
**Time to build:** ~2–3 hours (first time). ~45 minutes once you've done it before.
**This is fictional** — PolarCrest HVAC Solutions is a demo company. Swap business details to deploy for a real client.

---

## Estimated Costs

| Service | Free tier | Paid usage |
|---------|-----------|------------|
| **Vapi** | $10 free credit | ~$0.05–$0.15 per minute of call time |
| **OpenAI (GPT-4.1)** | — | ~$0.002–$0.008 per call (included in Vapi billing) |
| **Deepgram** | — | Included in Vapi billing |
| **Make.com** | 1,000 operations/month free | $9/mo Starter plan if you exceed free tier |
| **Google Calendar / Sheets** | Free | Free |
| **Vapi phone number** | — | ~$2/month for a US/Canada number |

**Realistic estimate for testing:** Under $5 total (mostly Vapi call minutes). The $10 free credit covers ~100 minutes of calls.

---

## Prerequisites — What You Need Before Starting

### Accounts to create (all free to start)

1. **Vapi** — voice AI platform (the core of this project)
   - Sign up at vapi.ai
   - Verify your email
   - You'll get $10 free credit automatically

2. **Google Account** — for Calendar and Sheets
   - You likely already have one (Gmail)
   - If not, create one at accounts.google.com

3. **Make.com** — automation platform (handles post-call emails + sheet updates)
   - Sign up at make.com
   - Free plan is enough to start

4. **Claude Code** — the AI coding assistant you're reading this from
   - Already set up if you're reading this

### Software to install on your computer

1. **Node.js** (version 18 or newer) — needed to run the Make.com setup script
   - Download from nodejs.org → click "LTS" → install
   - Verify: open a terminal and type `node --version` — should show `v18.x.x` or higher

2. **Git** — for version control (optional but recommended)
   - Download from git-scm.com
   - Already installed on most Macs; Windows users install it separately

3. **A terminal / command prompt**
   - Windows: use PowerShell or Git Bash
   - Mac: use Terminal

### What is Claude Code?
Claude Code is an AI assistant that runs in your terminal or VS Code. It reads your project files, writes code, and calls APIs for you. In this project, you give it slash commands like `/vapi-create-tool` and it builds Vapi resources automatically.

---

## Business Context — PolarCrest HVAC Solutions

This is the fictional company Joey works for. Swap these details when deploying for a real client.

| Field | Value |
|-------|-------|
| **Company** | PolarCrest HVAC Solutions |
| **Legal name** | PolarCrest Climate Services Inc. |
| **Type** | HVAC — Residential & Light Commercial |
| **Head office** | 3840 Dixie Road, Unit 12, Mississauga, ON L4Y 2B5 |
| **Service area** | Mississauga, Brampton, Oakville (primary); Etobicoke, Vaughan, Milton, Burlington (secondary +$35) |
| **Core services** | Furnace install/repair, AC install/repair, heat pumps, duct cleaning, IAQ, boilers, smart thermostats |
| **Booking duration** | 30-minute diagnostic / estimate appointments |
| **Business hours** | Mon–Fri 7AM–7PM EST, Sat 8AM–4PM EST, Sun 9AM–2PM (seasonal) |
| **Emergency line** | (905) 712-4499 — 24/7 live dispatch |
| **Main phone** | (905) 712-4480 |
| **Timezone** | America/Toronto (Eastern Time) |
| **Owner (fictional)** | Ryan Kowalski |
| **Office manager** | Sandra Beaumont |
| **Phone disposition** | All inbound — Joey answers, never cold-calls |
| **Google rating** | 4.9 ★ (614 reviews) |

---

## Joey's Personality

- **Tone:** Warm, confident, professional — like a real receptionist who knows HVAC inside out
- **Pace:** Medium. Not rushed, not slow. Mirrors the caller's energy
- **Style:** Asks one question at a time. Never dumps a list of questions on the caller
- **Empathy:** Acknowledges urgency ("That sounds stressful — let's get you sorted out fast")
- **Emergency awareness:** Immediately recognises no-heat, no-cool, and gas smell situations and routes accordingly
- **Boundaries:** Does NOT give pricing beyond published ranges, does NOT give technical repair advice, does NOT promise a specific technician
- **Fallback:** If he can't help, offers to have Sandra or Ryan call back within 2 hours (or 24 hours for non-urgent matters)
- **Voice:** Vapi `Elliot` — male, warm, professional, 30s (Vapi's flagship male voice)

---

## Joey's Qualifying Flow

1. **Greeting:** "Thanks for calling PolarCrest HVAC, this is Joey. How can I help you today?"
2. **Triage:** Determine if this is an emergency (no heat, no cool, gas smell, flooding) or a standard service/install inquiry
3. **Emergency routing:** If emergency → give emergency line (905) 712-4499 and offer to transfer immediately
4. **Service type:** Identify which service (furnace, AC, heat pump, duct cleaning, IAQ, boiler, thermostat, new install, maintenance plan)
5. **Location:** Confirm they are in the service area (Mississauga, Brampton, Oakville primary — or secondary zone for $35 surcharge)
6. **System details:** Ask make/model/age of existing equipment if repair call (helps dispatch the right tech)
7. **Timeline:** Urgency — same-day, next day, or flexible?
8. **Contact info:** Name, phone number, email (for calendar invite and invoice)
9. **Book appointment:** Check calendar and schedule a 30-minute diagnostic or estimate slot
10. **Log lead:** Save all collected info via logLead tool
11. **Confirm & close:** Repeat date/time, confirm address, tell them a certified technician will be there, thank caller

---

## Disqualification Criteria

- Outside service area (beyond 80 km from Mississauga — not in Ontario)
- Service not offered (plumbing, electrical panels, roofing, appliance repair unrelated to HVAC)
- Same-day non-emergency appointment (refer to next available slot — minimum next business day for standard calls)

When disqualified, Joey is polite: *"I completely understand — unfortunately that's outside what we're set up for, but I'd recommend checking HRAI.ca to find a qualified contractor near you. Is there anything else I can help with today?"*

---

## Emergency Handling — Critical

| Trigger phrase | Joey's response |
|---|---|
| "No heat" / "furnace not working" (winter) | Treat as emergency — offer same-day dispatch, provide (905) 712-4499 |
| "No AC" / "air conditioning not working" (summer) | Treat as urgent — offer priority booking, provide (905) 712-4499 after hours |
| "I smell gas" | Immediately: advise caller to leave the building, call Enbridge at 1-866-763-5427, then call our emergency line (905) 712-4499. Do NOT book an appointment — this is a safety emergency |
| "Water leaking from furnace / AC" | Treat as urgent — same-day dispatch if possible |
| "Carbon monoxide alarm" | Immediately: advise to evacuate, call 911, then (905) 712-4499. Do not book |

> **Agent rule:** For gas smell or CO alarm, Joey must NOT proceed with booking. Safety first, always.

---

## Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Voice AI platform | **Vapi** | Assistant hosting, telephony, call orchestration |
| LLM | **OpenAI GPT-4.1** | Joey's brain — conversation + tool calling |
| Voice (TTS) | **Vapi built-in** (`Elliot`) | Joey's speaking voice |
| Transcriber (STT) | **Deepgram Nova-3** | Caller speech recognition |
| Calendar | **Google Calendar** (Vapi native tool) | Appointment booking + availability checks |
| Lead logging | **Google Sheets** (Vapi native tool) | Log every call's lead data |
| Webhook processing | **Make.com** (cloud) | End-of-call reports, Gmail notifications, append to Calls tab |
| Phone number | **Vapi number** | Inbound line for demo |
| Documentation | **Vapi MCP Server** (`vapi-docs`) | Search Vapi docs from Claude Code |
| Build method | **Claude Code Skills** | All Vapi resources created via Skills |

---

## Environment Variables

All credentials go in `.env` in your project folder (never committed to git — the `.gitignore` already excludes it).

```
# Vapi
VAPI_API_KEY=your-vapi-api-key

# Google (connected via Vapi Dashboard OAuth — no keys needed here)
# Just note the spreadsheet ID and calendar ID after connecting

# Make.com (set in Phase 5)
MAKE_API_KEY=your-make-rest-api-token   # scopes: scenarios:read/write, hooks:read/write, connections:read, teams:read
MAKE_ZONE=eu2                            # the subdomain of your Make dashboard URL (eu1, us1, eu2, us2)
MAKE_WEBHOOK_URL=                        # populated after creating the custom webhook
MAKE_WEBHOOK_HOOK_ID=                    # populated after creating the custom webhook
MAKE_SCENARIO_ID=                        # populated after creating the scenario

# Resource IDs (populated during build)
VAPI_ASSISTANT_ID=
VAPI_PHONE_NUMBER_ID=
VAPI_GCAL_CHECK_TOOL_ID=
VAPI_GCAL_CREATE_TOOL_ID=
VAPI_GSHEETS_TOOL_ID=
VAPI_END_CALL_TOOL_ID=
VAPI_TRANSFER_CALL_TOOL_ID=
GOOGLE_SPREADSHEET_ID=
GOOGLE_CALENDAR_ID=
```

**How to find your Make zone:** Log into Make.com. Look at the URL in your browser — it starts with something like `eu2.make.com` or `us1.make.com`. The part before `.make.com` is your zone.

---

## Build Workflow — Complete Step-by-Step Guide

Each phase depends on the previous one. Follow this exact order. Do not skip ahead.

---

### Phase 0: Set Up Your Environment

**What this phase does:** Gets your project folder ready with the right files.

**Steps:**

1. Open a terminal (PowerShell on Windows, Terminal on Mac)
2. Navigate to where you want the project: `cd Documents`
3. If you received this as a zip, unzip it. If cloning from git: `git clone <repo-url>`
4. Open the project folder in VS Code or your editor
5. Create a `.env` file in the project root. Copy the template from the Environment Variables section above and paste it in — leave values blank for now
6. Open Claude Code in the project folder

**Success check:** You can see the project files (`CLAUDE.md`, `scripts/`, `config/`, etc.) and Claude Code is running.

---

### Phase 1: Foundation

**What this phase does:** Connects your Vapi account, links Google Calendar and Sheets, and creates the spreadsheet Joey will log leads into.

#### Step 1.1 — Get your Vapi API key

In Claude Code, run:
```
/setup-api-key
```

Claude Code will guide you to:
1. Go to app.vapi.ai → click your profile (top right) → API Keys
2. Click "Create API Key" → name it anything → copy the key
3. Paste it when Claude Code asks

Claude Code saves it to your `.env` file automatically.

**Success check:** Claude Code confirms the key is valid.

#### Step 1.2 — Connect Google Calendar (manual — must be done in dashboard)

> This step CANNOT be done via code. Google requires a browser-based login for security.

1. Go to app.vapi.ai
2. Click **Integrations** in the left sidebar
3. Click **Tools Provider**
4. Find **Google Calendar** → click **Connect**
5. A Google login popup appears — log in with the Google account that has the calendar you want Joey to use
6. Grant the permissions it asks for
7. You'll see "Connected" next to Google Calendar

**Which calendar?** Joey will book into whatever calendar is linked. Use a dedicated calendar for PolarCrest (create one in Google Calendar first if you want it separate from your personal calendar).

**Success check:** Google Calendar shows "Connected" in Vapi Dashboard → Integrations.

#### Step 1.3 — Connect Google Sheets (manual — must be done in dashboard)

Same process as 1.2, but for **Google Sheets**:
1. Vapi Dashboard → Integrations → Tools Provider → Google Sheets → Connect
2. Log in with the same Google account
3. Grant permissions

**Success check:** Google Sheets shows "Connected" in Vapi Dashboard → Integrations.

#### Step 1.4 — Create the "PolarCrest Leads" Google Sheet

You need to create the spreadsheet that Joey will log call data into.

**Option A — Automated (recommended):**
1. Go to script.google.com
2. Click "New project"
3. Delete the existing code and paste the `createPolarCrestLeadsSheet()` function from the "Apps Script to Create the Sheet" section below
4. Click Run (the triangle button)
5. Grant permissions when prompted
6. Check the **Logs** (View → Logs) — you'll see the Spreadsheet ID and URL
7. Copy the Spreadsheet ID (looks like `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms`)

**Option B — Manual:**
1. Go to sheets.google.com → click the "+" to create a new sheet
2. Rename it "PolarCrest Leads"
3. Rename the first tab "Leads"
4. Add headers in row 1 (columns A–M): Timestamp, Caller Name, Phone, Email, Service Type, Equipment Details, Location, Timeline, Appointment, Emergency, Qualified, Notes, Call Duration

After creating the sheet:
1. Copy the Spreadsheet ID from the URL (the long string between `/d/` and `/edit` in the sheet URL)
2. Add it to your `.env` file: `GOOGLE_SPREADSHEET_ID=your-id-here`
3. Also note your Google Calendar ID: go to calendar.google.com → click the 3-dot menu next to your calendar → Settings → scroll down to "Calendar ID" → copy it → add to `.env`: `GOOGLE_CALENDAR_ID=your-calendar-id`

**Success check:** You have a Google Sheet with 13 column headers in row 1. You have the Spreadsheet ID in your `.env`.

---

### Phase 2: Tools

**What this phase does:** Creates the 5 tools Joey uses during calls. Tools are actions Joey can take — like checking the calendar or saving a lead. You need their IDs before creating the assistant, because the assistant references them by ID.

> **Why create tools first?** The assistant config needs to reference tool IDs. You can't reference IDs that don't exist yet.

#### Step 2.1 — Google Calendar Check Availability tool

In Claude Code:
```
/create-tool
```

Tell Claude Code: "Create the Google Calendar check availability tool for PolarCrest. Business hours are Mon-Fri 7AM-7PM EST, Sat 8AM-4PM EST."

Claude Code creates the tool and saves the ID to `config/tools.json` and `.env` as `VAPI_GCAL_CHECK_TOOL_ID`.

#### Step 2.2 — Google Calendar Create Event tool

Run `/create-tool` again.

Tell Claude Code: "Create the Google Calendar create event tool for booking 30-minute appointments. Use America/Toronto timezone."

Saved as `VAPI_GCAL_CREATE_TOOL_ID`.

#### Step 2.3 — Google Sheets Log Lead tool (CRITICAL)

Run `/create-tool` again.

Tell Claude Code: "Create the Google Sheets append row tool for logging leads. Use spreadsheetId: [YOUR_ACTUAL_SPREADSHEET_ID] and range: Leads!A:M. Column order: Timestamp, Caller Name, Phone, Email, Service Type, Equipment Details, Location, Timeline, Appointment, Emergency, Qualified, Notes, Call Duration."

**Replace `[YOUR_ACTUAL_SPREADSHEET_ID]` with the real ID from your `.env`.** This is critical — see Lesson #1 in Lessons Learned below.

Saved as `VAPI_GSHEETS_TOOL_ID`.

#### Step 2.4 — End Call tool

Run `/create-tool` again.

Tell Claude Code: "Create an End Call tool. Joey should use it after confirming the appointment, after delivering emergency safety instructions, or when the caller is done."

Saved as `VAPI_END_CALL_TOOL_ID`.

#### Step 2.5 — Transfer Call tool

Run `/create-tool` again.

Tell Claude Code: "Create a Transfer Call tool that transfers to +1XXXXXXXXXX (replace with the actual office number). Use it when the caller insists on speaking to someone immediately or has a complex commercial inquiry."

**Replace `+1XXXXXXXXXX` with the real transfer number** (e.g., Ryan's cell or the office line).

Saved as `VAPI_TRANSFER_CALL_TOOL_ID`.

**Success check:** All 5 tool IDs are populated in `config/tools.json` and `.env`.

---

### Phase 3: Assistant

**What this phase does:** Creates Joey — the AI assistant with his personality, voice, transcriber, system prompt, and all 5 tools attached.

#### Step 3.1 — Create Joey

In Claude Code:
```
/create-assistant
```

Tell Claude Code: "Create Joey, the PolarCrest HVAC receptionist. Use the system prompt from prompts/joey-system.md. Voice: Vapi Elliot. Model: OpenAI GPT-4.1, temperature 0.7, maxTokens 300. Transcriber: Deepgram nova-3 with HVAC keyword boosts. Attach all 5 tool IDs from .env. Background sound: office. Enable backchanneling and denoising. Add a speech timeout hook at 8 seconds."

Claude Code creates the assistant and saves the full config to `config/assistant.json` and the ID to `.env` as `VAPI_ASSISTANT_ID`.

**Success check:** `config/assistant.json` exists and contains an `id` field. The ID is in `.env`.

---

### Phase 4: Phone Number

**What this phase does:** Buys a real phone number and assigns it to Joey. When someone calls this number, Joey answers.

#### Step 4.1 — Buy a Vapi phone number

In Claude Code:
```
/create-phone-number
```

Tell Claude Code: "Buy a Vapi phone number in Canada (area code 416 or 905 if available) and assign it to Joey's assistant ID from .env."

Claude Code purchases the number and saves the config to `config/phone-number.json` and the ID to `.env` as `VAPI_PHONE_NUMBER_ID`.

**How much does a number cost?** About $2/month, billed by Vapi. It comes out of your Vapi credit.

**Success check:** You have a phone number in `config/phone-number.json`. You can call it and hear Joey's greeting.

> **Quick test:** Call the number right now. Joey should answer: "Thanks for calling PolarCrest HVAC, this is Joey. How can I help you today?" If he answers, Phase 4 is working. Tools may not work yet (those need the Make.com webhook in Phase 5), but the assistant itself is live.

---

### Phase 5: Webhook (Make.com)

**What this phase does:** Sets up an automation that runs after every call ends. It sends you an email summary and logs call data (duration, cost, recording link) to the `Calls` tab in your spreadsheet.

**What is a webhook?** A webhook is a URL that receives data when something happens. When a call ends, Vapi sends call data to a URL you specify. Make.com receives that data and does things with it (sends email, updates spreadsheet).

**Overview of what gets built:**
```
Call ends → Vapi sends data to Make webhook URL
                    ↓
              Make receives it
                    ↓ (only if it's an end-of-call report)
              Gmail sends you an email summary
                    ↓
              Google Sheets logs the call row
```

**Build order:** You must build the Make scenario BEFORE telling Vapi the webhook URL, because you need the URL from Make first.

#### Step 5.0a — Generate a Make REST API token

What is a REST API token? It's a password that lets scripts talk to Make.com on your behalf.

1. Log into make.com
2. Click your profile icon (bottom left) → **Profile**
3. Click **API access** tab
4. Click **Add token**
5. Name it "PolarCrest HVAC" or anything
6. Set these scopes (checkboxes): `scenarios:read`, `scenarios:write`, `hooks:read`, `hooks:write`, `connections:read`, `teams:read`
7. Copy the token
8. Add to `.env`: `MAKE_API_KEY=your-token-here`

Also add your Make zone to `.env`: `MAKE_ZONE=eu2` (replace with your actual zone — check your Make.com URL).

#### Step 5.0b — Add Gmail and Google connections in Make UI (manual — browser required)

> Google OAuth can't be done via script. This is a one-time browser step.

1. Log into make.com
2. Click **Connections** in the left sidebar
3. Click **Create a connection**
4. Search for **Gmail** → select it → click **Continue** → log in with your Google account → grant permissions → Save
5. Repeat for **Google Sheets**: Create connection → search "Google Sheets" → connect same Google account

**Success check:** You see two connections (Gmail and Google Sheets/Drive) listed under Connections.

#### Step 5.0c — Create the `Calls` tab in your spreadsheet

1. Go to script.google.com
2. Open a new project (or reuse the one from Step 1.4)
3. Paste the `createPolarCrestCallsTab()` function from the "Calls Tab Schema" section below
4. **Replace `YOUR_SPREADSHEET_ID`** in the script with your actual Spreadsheet ID
5. Click Run
6. Grant permissions

**Success check:** Your Google Sheet now has two tabs: "Leads" and "Calls".

#### Step 5.0d — Find your Make Team ID

The setup script needs your Make team ID. Get it:
1. Log into Make.com
2. Click **Organization** in the left sidebar → **Teams**
3. The number in the URL is your team ID (e.g., `make.com/org/123456/teams` → ID is `123456`)
4. Or: the script will try to find it automatically if you don't know it

#### Step 5.0e — Install script dependencies

In your terminal, from the project folder:
```
npm install axios dotenv
```

This installs two libraries the setup script needs (`axios` for making web requests, `dotenv` for reading your `.env` file).

#### Step 5.2 — Run the Make scenario setup script

This script does everything automatically:
1. Creates the Make webhook
2. Builds the 3-module scenario (Webhook → Gmail → Google Sheets)
3. Activates the scenario
4. Saves the webhook URL and IDs to your `.env`

Run it:
```
node scripts/create-make-scenario.js
```

The script will prompt you for:
- Your Make team ID (from step 5.0d)
- The Gmail connection ID (shown in Make.com → Connections → click Gmail → note the ID in the URL)
- The Google Sheets connection ID (same — click the Sheets connection)
- Your Gmail address (where to send call notification emails)
- Your Google Spreadsheet ID (from `.env`)

After it runs, check your `.env` — it should now have:
```
MAKE_WEBHOOK_URL=https://hook.eu2.make.com/xxxxxxxxxxxxxxxx
MAKE_WEBHOOK_HOOK_ID=12345678
MAKE_SCENARIO_ID=87654321
```

**If the script fails:** See the Make.com troubleshooting section at the bottom.

#### Step 5.1 — Wire the webhook URL to Joey

Now tell Vapi to send call reports to your Make webhook:

```bash
curl -X PATCH "https://api.vapi.ai/assistant/$VAPI_ASSISTANT_ID" \
  -H "Authorization: Bearer $VAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"server\":{\"url\":\"$MAKE_WEBHOOK_URL\"}}"
```

On Windows PowerShell, use Claude Code to run this — tell it: "PATCH the Vapi assistant server URL to [your MAKE_WEBHOOK_URL from .env]."

**Success check:** The API returns the updated assistant JSON with `server.url` set to your Make webhook URL.

---

### Phase 6: Testing

**What this phase does:** Verifies the entire system works end to end.

#### Step 6.1 — Outbound test call (Joey calls you)

In Claude Code:
```
/create-call
```

Tell Claude Code: "Create an outbound test call from Joey's assistant to my phone number [your number]."

Joey will call your phone. Answer it and test the qualifying flow:
- Ask about furnace repair
- Give your name, phone, email
- Let Joey book an appointment
- Confirm the appointment and say goodbye

#### Step 6.2 — Inbound test (you call Joey)

Call the phone number from `config/phone-number.json`. Joey should answer immediately. Test the same flow again — inbound routing is separate from outbound and worth verifying independently.

Also test emergency flows:
- Say "I smell gas" → Joey should give safety instructions and NOT book an appointment
- Say "My furnace stopped working" → Joey should treat it as urgent and offer priority booking

#### Step 6.3 — Verify the full automation pipeline

After the call ends, within 1–2 minutes:
1. **Check your email** — you should receive an HTML email with the call summary, duration, cost, and recording link
2. **Check Google Sheets → Leads tab** — Joey should have logged the caller's info during the call
3. **Check Google Sheets → Calls tab** — Make should have appended a row with post-call data
4. **Check Make → Scenarios** — open your scenario → click the clock icon (History) → you should see a successful run

**If email arrived but Sheets didn't update (or vice versa):** Open the Make scenario run history and click the failed run to see which module errored and why.

---

## Joey's System Prompt

Source of truth is `prompts/joey-system.md`. This is what gets pasted into the assistant as the system message.

```
You are Joey, the virtual receptionist at PolarCrest HVAC Solutions. You answer inbound phone calls for a residential and commercial HVAC contractor serving Mississauga, Brampton, Oakville, and surrounding areas in Ontario, Canada.

## Your personality
- Warm, confident, professional — like a real receptionist who genuinely wants to help
- You ask ONE question at a time and wait for the answer
- You mirror the caller's energy — if they're stressed about no heat in winter, acknowledge it first
- Keep responses concise (under 30 words when possible)
- Use natural filler phrases occasionally ("Let me check on that", "Absolutely", "Of course")

## EMERGENCY TRIAGE — Handle FIRST before anything else

If the caller mentions any of the following, handle it immediately BEFORE the standard flow:

- **"No heat"** or **"furnace not working"** (especially in cold months): Say — "I'm so sorry to hear that. I'm flagging this as urgent. Let me get you priority service. Can I get your name and address first?" Then book same-day if available, or provide emergency line (905) 712-4499 for after-hours.
- **"No air conditioning"** or **"AC not working"** (especially in summer): Treat as urgent. Offer fastest available slot. Provide (905) 712-4499 for after-hours.
- **"I smell gas"**: Say — "For your safety, please leave the building immediately. Call Enbridge Gas at 1-866-763-5427 from outside. Then call our emergency line at 9-0-5, 7-1-2, 4-4-9-9. Do not re-enter until a technician has cleared the property." Then end the call. Do NOT book an appointment.
- **"Carbon monoxide alarm"**: Say — "Please evacuate now and call 911. Once you're safe, our emergency team is at 9-0-5, 7-1-2, 4-4-9-9." End the call. Do NOT book an appointment.

## Services you book appointments for
- Furnace installation, repair, or tune-up
- Air conditioning installation or repair
- Heat pump installation or repair
- Duct cleaning and ductwork repairs
- HRV / ERV ventilation units
- Whole-home humidifiers and IAQ systems
- Boiler service and replacement
- Smart thermostat supply and installation
- Annual maintenance plan enrolment
- Energy efficiency consultations (Enbridge / Greener Homes)
- Commercial HVAC maintenance contract discussions

## Your job on every call
1. Greet the caller warmly
2. Triage — determine if this is an emergency or standard service/install inquiry
3. Handle emergencies immediately using the emergency protocol above
4. Identify the service type needed
5. Confirm they are in the service area — primary: Mississauga, Brampton, Oakville. Secondary (+$35 surcharge): Etobicoke, Vaughan, Milton, Burlington. Ask for their city or postal code.
6. If it's a repair call, ask for the make, model, and approximate age of their existing equipment
7. Ask about their timeline — urgent, next day, or flexible?
8. Collect their name, phone number, and email address
9. Check calendar availability and book a 30-minute diagnostic or estimate appointment
10. Log the lead using the logLead tool — include all collected info (name, phone, email, service type, equipment details, location, timeline, appointment date/time, and any notes)
11. Confirm the appointment: date, time, and address. Let them know a certified PolarCrest technician will be there.
12. Thank them and end the call

## Rules
- NEVER give exact pricing — say "Our technician will provide an accurate quote on-site. I can share that our standard diagnostic fee is $99, which is waived if you proceed with the repair."
- NEVER give technical repair advice — say "That's a great question for our technician — they'll be able to assess everything during the visit."
- NEVER promise a specific technician by name — say "We'll assign the best available certified technician for your service type."
- NEVER book same-day appointments for non-emergency calls — earliest is next business day
- If the caller needs a service outside HVAC scope (plumbing, electrical, roofing), politely refer them to HRAI.ca
- If the caller is outside the service area, politely let them know and refer them to HRAI.ca
- If the caller asks to speak to someone directly, offer to have Sandra Beaumont (office manager) call them back within 2 hours during business hours
- Business hours for standard appointments: Mon–Fri 7AM–7PM EST, Sat 8AM–4PM EST
- All appointments are 30 minutes
- Current date/time: {{now}}
- Timezone: America/Toronto
```

---

## Tool Configurations

These are the exact JSON configs used to create each tool. Claude Code handles this for you via `/create-tool`, but you can also create them manually via the Vapi dashboard or API.

### Google Calendar — Check Availability
```json
{
  "type": "google.calendar.availability.check",
  "function": {
    "name": "checkAvailability",
    "description": "Check calendar availability for PolarCrest HVAC Solutions appointments. Use this before booking to find open 30-minute slots. Business hours: Mon-Fri 7AM-7PM EST, Sat 8AM-4PM EST. Current date/time: {{now}}"
  }
}
```

### Google Calendar — Create Event
```json
{
  "type": "google.calendar.event.create",
  "function": {
    "name": "bookAppointment",
    "description": "Book a 30-minute diagnostic or estimate appointment for PolarCrest HVAC Solutions. Use the service type as the event summary (e.g., 'Furnace Repair - Sarah Chen' or 'AC Estimate - Mike Davis'). All appointments are 30 minutes. Set timezone to America/Toronto. Current date/time: {{now}}"
  }
}
```

### Google Sheets — Log Lead
```json
{
  "type": "google.sheets.row.append",
  "function": {
    "name": "logLead",
    "description": "Log the caller's lead information to the PolarCrest leads spreadsheet after collecting their details. ALWAYS use spreadsheetId: YOUR_SPREADSHEET_ID_HERE and range: Leads!A:M. Record values in this exact column order: [Timestamp, Caller Name, Phone, Email, Service Type, Equipment Details, Location, Timeline, Appointment Date/Time, Emergency (Yes/No), Qualified (Yes/No/Partial), Notes, Call Duration]. Use current date/time for the timestamp."
  }
}
```

> **CRITICAL:** Replace `YOUR_SPREADSHEET_ID_HERE` with the actual Google Spreadsheet ID. If you don't, the AI will guess a fake ID and the tool will fail with "Requested entity was not found."

### End Call
```json
{
  "type": "endCall",
  "function": {
    "name": "endCall",
    "description": "End the call after the conversation is complete, the appointment is confirmed, the emergency protocol has been delivered, or the caller has no more questions."
  }
}
```

### Transfer Call (fallback to Ryan / Sandra)
```json
{
  "type": "transferCall",
  "destinations": [
    {
      "type": "number",
      "number": "+1XXXXXXXXXX",
      "message": "Let me transfer you to our team right now.",
      "description": "Transfer to the PolarCrest office when the caller insists on speaking to someone immediately, has a complex commercial inquiry, or has an urgent matter that Joey cannot resolve"
    }
  ],
  "function": {
    "name": "transferToOffice",
    "description": "Transfer the call to the PolarCrest office team (Ryan Kowalski or Sandra Beaumont) when the caller requests to speak with someone directly or has a matter requiring human intervention"
  }
}
```

---

## Google Sheets Lead Schema

Create a Google Sheet called "PolarCrest Leads" with a tab named "Leads" and these column headers in Row 1:

| Column | Description | Example |
|--------|-------------|---------|
| A: Timestamp | When the call happened | 2026-04-30 09:15 EST |
| B: Caller Name | Full name | Sarah Chen |
| C: Phone | Phone number | (905) 555-0198 |
| D: Email | Email address | sarah@example.com |
| E: Service Type | What they need | Furnace Repair |
| F: Equipment Details | Make / model / age | Lennox G61V, approx. 12 yrs |
| G: Location | City or postal code | Mississauga, L5B 2C3 |
| H: Timeline | Urgency level | Urgent — no heat |
| I: Appointment | Booked date/time | 2026-05-01 10:00 AM |
| J: Emergency | Was this an emergency call? | Yes |
| K: Qualified | Yes/No/Partial | Yes |
| L: Notes | Any additional context | Secondary zone (+$35), has Comfort Care Plan |
| M: Call Duration | Reserved — filled by Calls tab, not Joey | — |

### Apps Script to Create the Sheet

Run this in [Google Apps Script](https://script.google.com) (script.google.com → New project → paste this → Run):

```javascript
function createPolarCrestLeadsSheet() {
  var ss = SpreadsheetApp.create("PolarCrest Leads");
  var sheet = ss.getActiveSheet();
  sheet.setName("Leads");

  var headers = [
    "Timestamp", "Caller Name", "Phone", "Email", "Service Type",
    "Equipment Details", "Location", "Timeline", "Appointment",
    "Emergency", "Qualified", "Notes", "Call Duration"
  ];

  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  var headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setFontWeight("bold");
  headerRange.setBackground("#0C447C");
  headerRange.setFontColor("#FFFFFF");
  headerRange.setHorizontalAlignment("center");

  var widths = [160, 150, 140, 200, 150, 200, 150, 150, 180, 90, 90, 260, 100];
  for (var i = 0; i < widths.length; i++) {
    sheet.setColumnWidth(i + 1, widths[i]);
  }

  sheet.setFrozenRows(1);

  Logger.log("Spreadsheet ID: " + ss.getId());
  Logger.log("URL: " + ss.getUrl());

  return ss.getId();
}
```

After running, check **View → Logs** for the Spreadsheet ID. Copy it and add to `.env` as `GOOGLE_SPREADSHEET_ID`.

---

## Calls Tab Schema (post-call data, written by Make)

A second tab in the same spreadsheet — `Calls` — is appended to by the Make scenario after every call ends. This is separate from the `Leads` tab (which Joey populates during the call) so the two data flows don't collide.

| Column | Description | Example |
|--------|-------------|---------|
| A: Timestamp | When the call ended (Toronto time) | 2026-04-30 09:18 |
| B: Phone | Caller's number (from Vapi) | +19055550198 |
| C: Duration | mm:ss formatted | 5:14 |
| D: Cost | USD with 4-decimal precision | 0.0823 |
| E: Ended Reason | Vapi `endedReason` value | customer-ended-call |
| F: Summary | Vapi-generated call summary | Booked furnace repair for May 2 at 10am... |
| G: Recording URL | Link to MP3 recording | https://storage.vapi.ai/... |

### Apps Script to Add the Calls Tab

Run this in [Google Apps Script](https://script.google.com) attached to the **same** spreadsheet that has the Leads tab. Replace `YOUR_SPREADSHEET_ID` first.

```javascript
function createPolarCrestCallsTab() {
  var ss = SpreadsheetApp.openById("YOUR_SPREADSHEET_ID");
  var sheet = ss.insertSheet("Calls");

  var headers = [
    "Timestamp", "Phone", "Duration", "Cost",
    "Ended Reason", "Summary", "Recording URL"
  ];

  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  var headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setFontWeight("bold");
  headerRange.setBackground("#0C447C");
  headerRange.setFontColor("#FFFFFF");
  headerRange.setHorizontalAlignment("center");

  var widths = [160, 140, 100, 100, 180, 360, 320];
  for (var i = 0; i < widths.length; i++) {
    sheet.setColumnWidth(i + 1, widths[i]);
  }

  sheet.setFrozenRows(1);

  Logger.log("Calls tab created in: " + ss.getUrl());
}
```

> The Make `addRow` module requires the `Calls` tab to already exist with headers in row 1. If it's missing, the entire Make scenario run will fail (including the Gmail step).

---

## Make.com Scenario — Vapi Call Report Processor

The Make scenario is built and managed via REST API by `scripts/create-make-scenario.js`. It has **3 modules**:

```
[1] Custom Webhook (gateway:CustomWebHook v1)
        ↓ filter: only if 1.message.type == "end-of-call-report"
[2] Gmail — Send an Email (google-email:sendAnEmail v4)
        ↓
[3] Google Sheets — Add a Row (google-sheets:addRow v2)  →  appends to "Calls" tab
```

**Key technical details (verified working on 2026-05-01):**
- Make REST API auth: `Authorization: Token <api_key>` (capital T, not `Bearer`)
- Webhook creation: `POST /api/v2/hooks?teamId=<id>` with `{ typeName: "gateway-webhook" }`
- Scenario creation: `POST /api/v2/scenarios?confirmed=true` — `blueprint` and `scheduling` must be JSON-stringified strings, not nested objects
- Activation requires `scheduling: {type:"indefinitely", interval:900}` — `type` alone returns `IM008 "Invalid interval"`
- Working module names: `gateway:CustomWebHook` v1, `google-email:sendAnEmail` v4, `google-sheets:addRow` v2

---

## Assistant Configuration Summary

```json
{
  "name": "Joey - PolarCrest HVAC Receptionist",
  "firstMessage": "Thanks for calling PolarCrest HVAC, this is Joey. How can I help you today?",
  "firstMessageMode": "assistant-speaks-first",
  "model": {
    "provider": "openai",
    "model": "gpt-4.1",
    "temperature": 0.7,
    "maxTokens": 300,
    "toolIds": [
      "<gcal-check-id>",
      "<gcal-create-id>",
      "<gsheets-id>",
      "<end-call-id>",
      "<transfer-call-id>"
    ],
    "messages": [
      {
        "role": "system",
        "content": "<Joey's full system prompt from prompts/joey-system.md>"
      }
    ]
  },
  "voice": {
    "provider": "vapi",
    "voiceId": "Elliot"
  },
  "transcriber": {
    "provider": "deepgram",
    "model": "nova-3",
    "language": "en",
    "keywords": ["PolarCrest:3", "furnace:2", "HVAC:2", "air conditioning:2", "heat pump:2", "Mississauga:2", "Brampton:2"]
  },
  "backgroundSound": "office",
  "backchannelingEnabled": true,
  "backgroundDenoisingEnabled": true,
  "hooks": [
    {
      "on": "customer.speech.timeout",
      "options": { "timeoutSeconds": 8, "triggerMaxCount": 2 },
      "do": [{ "type": "say", "exact": "Are you still there? I want to make sure I get you sorted out." }]
    }
  ],
  "server": { "url": "<MAKE_WEBHOOK_URL>" }
}
```

---

## File Structure

```
VapiCodeAI/
├── CLAUDE.md              # This file — project config and build guide
├── .env                   # API keys and resource IDs (gitignored)
├── .gitignore             # Excludes .env, node_modules, etc.
├── README.md              # Public-facing project description
│
├── config/
│   ├── assistant.json     # Joey's full config (saved after creation)
│   ├── tools.json         # All tool configs (saved after creation)
│   └── phone-number.json  # Phone number config (saved after creation)
│
├── prompts/
│   └── joey-system.md     # Joey's system prompt (source of truth)
│
├── scripts/
│   ├── create-make-scenario.js  # Builds + activates the Make scenario via REST API
│   ├── test-call.sh             # Triggers an outbound test call via API
│   └── list-resources.sh        # Lists all Vapi resources
│
├── docs/
│   ├── build-log.md       # Build steps and decisions
│   └── vapi-lessons.md    # Gotchas and lessons learned
│
└── demo/
    └── call-recording.mp3 # Sample call recording for YouTube
```

**Convention:** After every Vapi API call that creates a resource, save the full JSON response into the corresponding `config/` file. This gives a local record of all IDs without querying the API.

---

## Webhook — End-of-Call Report

When Joey finishes a call, Vapi sends an `end-of-call-report` to the assistant's `server.url` — which points at the Make.com custom webhook. The Make scenario:

1. Receives the webhook POST (Make replies with `{}` instantly — automatic)
2. Filters for `message.type == "end-of-call-report"` (skips other message types Vapi sends mid-call)
3. Reads from the payload: `transcript`, `summary`, `recordingUrl`, `durationSeconds`, `cost`, `endedReason`, `call.customer.number`
4. Formats duration as `mm:ss`
5. Sends an HTML email notification (Module 2 — Gmail `sendAnEmail`)
6. Appends a row to the `Calls` tab of the leads spreadsheet (Module 3 — Google Sheets `addRow`)

> **Why append to a `Calls` tab instead of updating the Lead row?**
> Matching by phone number and updating an existing row requires a `searchRows` module which is not exposed via Make's blueprint API at the verified module versions. Append-to-Calls avoids the search-then-update complexity. Lead data from the call is already in the `Leads` tab; post-call data goes in `Calls`. Both are in the same spreadsheet.

---

## Key Vapi Concepts

| Concept | What It Means | Relevant Skill |
|---------|--------------|----------------|
| **Assistant** | The AI agent — has a voice, LLM, transcriber, tools, and a system prompt | `/create-assistant` |
| **Tool** | An action the assistant can take during a call (book calendar, log to sheets, etc.) | `/create-tool` |
| **Phone Number** | A real phone number assigned to an assistant — calls to this number reach Joey | `/create-phone-number` |
| **Server URL** | A webhook URL where Vapi sends call events after every call | `/setup-webhook` |
| **Squad** | Multiple assistants that hand off to each other (not needed here) | `/create-squad` |
| **Workflow** | Node-based conversation flow with if/else branches (not needed here) | `/create-workflow` |
| **Hooks** | Automated responses to call events (e.g., say something after 8 seconds of silence) | Part of assistant config |
| **`toolIds`** | List of tool IDs attached to an assistant — the tools it can use | Part of assistant config |
| **`{{now}}`** | Template variable — Vapi replaces it with the current date/time at call start | Used in prompts and tool descriptions |
| **E.164 format** | International phone number format: `+1XXXXXXXXXX` (country code + 10 digits, no dashes or spaces) | Used for transfer call destinations |

### Vapi MCP Documentation

When you need to look up anything beyond the skills, use:
```
mcp__vapi-docs__searchDocs(query: "your question here")
```

---

## Lessons Learned (Critical — Read Before Building)

These are gotchas discovered during the first build. Each one cost time. Read them first.

### 1. Google Sheets tool MUST have hardcoded spreadsheet ID

The LLM will **guess** the spreadsheet ID if you don't tell it explicitly. On the first test call, the agent called `logLead` with `spreadsheetId: "polarcrest-leads"` instead of the actual Google Sheets ID, resulting in `"Requested entity was not found."` error.

**Fix:** Hardcode the real spreadsheet ID AND the range directly in the tool's `description` field:
```
"ALWAYS use spreadsheetId: your-actual-spreadsheet-id and range: Leads!A:M"
```

### 2. System prompt must explicitly tell Joey to use logLead

Just having the tool attached via `toolIds` is NOT enough. The LLM won't reliably call it unless the system prompt explicitly says to. Add it as a numbered step:
```
10. Log the lead using the logLead tool — include all collected info
```

### 3. Vapi voice `Lily` was retired (March 2026)

Attempting `voiceId: "Lily"` returns an error. **Use `Elliot`** for Joey.

**Current supported Vapi voices (verified 2026-05-01):** Clara, Godfrey, Layla, Sid, Gustavo, Elliot, Kylie, Rohan, Lily, Savannah, Hana, Neha, Cole, Harry, Paige, Spencer, Nico, Kai, Emma, Sagar, Neil, Naina, Leah, Tara, Jess, Leo, Dan, Mia, Zac, Zoe. (`Mason` is NOT supported — returns 400.)

### 4. firstMessage — keep it simple, no special characters

Use a clean greeting. Escaped characters or unusual punctuation can cause TTS to behave oddly. No exclamation marks, no special characters.

### 5. Call Duration can't be filled by the assistant

Joey doesn't know the call duration mid-call — that data only exists in the end-of-call report sent AFTER the call ends. Make handles it by appending to the `Calls` tab.

### 6. Create the Google Sheet BEFORE testing

The logLead tool will fail if the spreadsheet doesn't exist. Create it in Phase 1.

### 7. endCall and transferCall can be saved tools attached via `toolIds`

No need to inline them in `model.tools` — saved tools work the same way and keep all tool configs in one place.

### 8. Loading .env on Windows Git Bash

```bash
export $(grep -v '^#' .env | xargs)
```
`source .env` doesn't reliably export variables for subcommands on Windows Git Bash.

### 9. Test both outbound AND inbound calls

Issues can appear in one flow but not the other. Always test both.

### 10. GPT-4.1 is excellent for voice AI tool calling

Temperature 0.7 + maxTokens 300 is a good balance for conversational yet focused responses. It reliably calls tools in parallel (bookAppointment + logLead simultaneously), follows the one-question-at-a-time rule, and handles edge cases well.

### 11. Emergency triage must come BEFORE the standard qualifying flow

For HVAC, gas leaks and CO alarms are safety emergencies. If the standard flow runs first (ask location, ask service type...) before the emergency check, this is a dangerous failure mode. Emergency triage is the FIRST block in the system prompt.

### 12. Canadian phone numbers in E.164 format

Use `+19057124499` in code, not `(905) 712-4499`. When Joey speaks a number to a caller, he says it digit by digit: *"9-0-5, 7-1-2, 4-4-9-9"* — not as a block — for clarity over voice.

### 13. Make.com API auth is `Token`, not `Bearer`

`Authorization: Token <api_key>` with capital T. Using `Bearer` returns a 401.

### 14. Make scenario `scheduling` must include `interval`

`{type:"indefinitely"}` alone returns error `IM008 "Invalid interval"`. Must include: `{type:"indefinitely", interval:900}`.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| API calls return 401 | Check `VAPI_API_KEY` in `.env` — use the private key, not public key |
| Google Calendar tools fail | Reconnect Google Calendar in Vapi Dashboard → Integrations |
| Google Sheets tool returns "entity not found" | Hardcode the real spreadsheet ID in the logLead tool description (Lesson #1) |
| Google Sheets tool fails | Reconnect Google Sheets in Vapi Dashboard → Integrations |
| Joey doesn't speak first | Verify `firstMessageMode` is `"assistant-speaks-first"` |
| Joey gives exact pricing | Strengthen the "NEVER give exact pricing" rule in system prompt |
| Joey skips emergency triage | Move emergency triage block to the TOP of the system prompt |
| Joey books appointment for gas smell caller | Add explicit rule: "For gas smell or CO alarm, do NOT book — deliver safety protocol and end call" |
| Transcription misses "PolarCrest" | Add to `transcriber.keywords` with boost value — `"PolarCrest:3"` |
| Webhook not receiving events | Check `server.url` on assistant — must be a publicly accessible HTTPS URL |
| Calls drop after greeting | Check `maxTokens` isn't too low in model config |
| Voice sounds wrong | Check `voiceId` against the supported list (Lesson #3). Use `Elliot` for Joey |
| Call duration not in `Calls` tab | Appended by Make, not Joey. Check Make scenario history. Common cause: `Calls` tab missing — re-run the Apps Script |
| Make scenario shows "Sheet not found" | `Calls` tab doesn't exist — run `createPolarCrestCallsTab()` Apps Script |
| Make scenario didn't fire | Check Vapi assistant `server.url` points at Make webhook. Check scenario is active (isActive=true) |
| Make API returns 401 | Auth header must be `Token <key>` not `Bearer <key>` |
| Make scenario creation fails with IM008 | Add `interval: 900` to the scheduling object alongside `type` |
| `node scripts/create-make-scenario.js` fails | Run `npm install axios dotenv` first. Check all Make connection IDs are correct |
| Joey promises specific tech | Add rule: "NEVER promise a specific technician by name" |
| No email after test call | Check Make scenario history. Check Gmail connection is valid. Check scenario is active |
| Google Calendar not booking | Verify the calendar ID in your Vapi Google Calendar integration matches `GOOGLE_CALENDAR_ID` in `.env` |

---

## Glossary

**API key** — A secret password that lets software talk to a service on your behalf. Never share it publicly.

**Assistant** — In Vapi, an assistant is a complete AI agent: it has a voice, a brain (LLM), a transcriber, tools it can use, and a system prompt that tells it how to behave.

**Blueprint** — In Make.com, a blueprint is the JSON definition of a scenario (which modules it has, how they're connected, what data they use).

**Deepgram** — The service that converts spoken audio from the caller into text. Nova-3 is its most accurate model for English.

**E.164 format** — The international standard for phone numbers: `+` country code + number, no spaces or dashes. Canada/US: `+1XXXXXXXXXX`.

**End-of-call report** — A JSON payload Vapi sends to your webhook URL when a call ends. Contains transcript, summary, duration, cost, recording URL, and how the call ended.

**GPT-4.1** — OpenAI's language model that powers Joey's reasoning and conversation. It decides what to say and when to use tools.

**Hook** — An automated action that fires on a call event (e.g., "if the caller is silent for 8 seconds, say 'Are you still there?'"). Configured in the assistant.

**LLM** — Large Language Model. The AI brain. In this project it's GPT-4.1 via OpenAI.

**Make.com** — A no-code automation platform. You connect apps and define what should happen when a trigger fires. Here it receives the call report from Vapi, sends an email, and updates Google Sheets.

**Node.js** — A JavaScript runtime that lets you run JavaScript on your computer (outside of a browser). Needed to run the `create-make-scenario.js` script.

**OAuth** — A secure way to let one service access another on your behalf without sharing your password. When you "Connect Google Calendar" in Vapi dashboard, that's OAuth.

**REST API** — A standard way for software to talk to web services using HTTP requests (GET, POST, PATCH, etc.). This whole project is built by calling REST APIs.

**Scenario** — In Make.com, a scenario is an automated workflow. It has a trigger (e.g., a webhook receives data) and actions (e.g., send email, append to sheet).

**Spreadsheet ID** — The unique identifier for a Google Sheet. Found in the URL between `/d/` and `/edit`. Example: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms`.

**Squad** — A Vapi feature where multiple assistants hand off to each other (e.g., a triage assistant hands off to a booking specialist). Not used in this project — Joey handles everything.

**TTS** — Text-to-Speech. Converts Joey's text responses into a spoken voice.

**Tool** — In Vapi, a tool is an action the assistant can take during a call. Tools are defined separately and attached to an assistant by ID. Joey has 5 tools: check calendar, book appointment, log lead, end call, transfer call.

**Transcriber** — The service that converts caller speech to text (Speech-to-Text / STT). This project uses Deepgram Nova-3.

**Vapi** — The voice AI platform that hosts Joey. It handles telephony (phone calls), routes audio to/from the LLM and TTS, and manages the call lifecycle.

**Webhook** — A URL that receives data when something happens. Vapi sends call reports to your Make.com webhook URL when calls end.

**`{{now}}`** — A Vapi template variable that gets replaced with the current date and time when a call starts. Used in Joey's system prompt so he knows today's date.

---

## FAQ

**Can I use this for a different type of business?**
Yes. Replace the business details in this file, update Joey's system prompt (`prompts/joey-system.md`), and adjust the qualifying flow questions. The infrastructure (Vapi + Make + Google) stays the same.

**Do I need to know how to code?**
No. You paste commands into Claude Code, which writes and runs the code for you. The one script you run (`create-make-scenario.js`) runs with a single command.

**Can I skip Make.com?**
Yes, with trade-offs. Without Make, you won't get post-call email notifications or the `Calls` tab data. Joey will still book appointments and log leads to the `Leads` tab. If you want to skip Make, just don't run Phase 5 — everything else still works.

**What if I want to use a different voice?**
Change `voiceId` in the assistant config. See the supported voices list in Lesson #3.

**Can I use a different LLM instead of GPT-4.1?**
Yes — Vapi supports OpenAI, Anthropic Claude, Google Gemini, and others. Change the `provider` and `model` fields in the assistant config. GPT-4.1 is recommended for tool calling reliability.

**How do I update Joey's system prompt after he's created?**
Edit `prompts/joey-system.md`, then PATCH the assistant via the Vapi API or dashboard. Claude Code can do this: "Update Joey's system prompt with the content from prompts/joey-system.md."

**Can multiple people call at the same time?**
Yes. Vapi handles concurrent calls automatically. Each call gets its own session.

**Is this HIPAA / PIPEDA compliant?**
This demo is not configured for compliance. For production use with real customer data, review Vapi's compliance documentation and configure data handling accordingly.

---

## Scope Boundaries

- **Not a Squad** — Joey is solo. Upgrade to Squad if department routing (residential vs. commercial) is needed later.
- **Not a Workflow** — Qualifying flow is prompt-driven. Upgrade to Workflow if deterministic branching is needed.
- **Not production** — PolarCrest HVAC Solutions is fictional. This is a demo/template for the Zayn.ai voice agent portfolio.
