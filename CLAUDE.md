# VapiCodeAI — Voice AI Receptionist (PolarCrest HVAC Solutions)

## What This Is

A **code-first voice AI receptionist** for PolarCrest HVAC Solutions, a residential and commercial HVAC contractor in Mississauga, Ontario. The assistant's name is **Joey**. He handles inbound calls, qualifies leads, books appointments into Google Calendar, and routes emergency calls appropriately.

**Purpose:** Demo project and reusable template for building voice AI receptionists. Built 100% through Claude Code using Vapi Skills and the Vapi MCP documentation server — no dashboard clicking.

---

## Business Context — PolarCrest HVAC Solutions

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

All credentials go in `.env` (never committed to git):

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

---

## Build Workflow — Order of Operations

Each step depends on the previous one. Follow this exact sequence.

### Phase 1: Foundation

| Step | Skill / Action | What It Does |
|------|---------------|--------------|
| **1.1** | `/vapi-setup-api-key` | Get API key from dashboard, validate it, save to `.env` |
| **1.2** | Manual (Dashboard) | Connect Google Calendar: Dashboard > Integrations > Tools Provider > Google Calendar > Connect |
| **1.3** | Manual (Dashboard) | Connect Google Sheets: Dashboard > Integrations > Tools Provider > Google Sheets > Connect |
| **1.4** | Create Google Sheet | Create "PolarCrest Leads" sheet with column headers (use Apps Script below or manually). See Google Sheets Lead Schema below. |

> Steps 1.2 and 1.3 MUST be done in the Vapi Dashboard — Google OAuth cannot be completed via API. Everything else is code-first.

### Phase 2: Tools (create before assistant — need tool IDs)

| Step | Skill | Tool |
|------|-------|------|
| **2.1** | `/vapi-create-tool` | Google Calendar — Check Availability |
| **2.2** | `/vapi-create-tool` | Google Calendar — Create Event |
| **2.3** | `/vapi-create-tool` | Google Sheets — Append Row (lead logging) — **CRITICAL: hardcode spreadsheetId and range in the tool description** (see Lessons Learned) |
| **2.4** | `/vapi-create-tool` | End Call |
| **2.5** | `/vapi-create-tool` | Transfer Call (fallback to Ryan Kowalski's number) |

### Phase 3: Assistant

| Step | Skill | What It Does |
|------|-------|--------------|
| **3.1** | `/vapi-create-assistant` | Create Joey with system prompt, model, voice, transcriber, and attach all tool IDs from Phase 2 |

### Phase 4: Phone Number

| Step | Skill | What It Does |
|------|-------|--------------|
| **4.1** | `/vapi-create-phone-number` | Buy a Vapi number and assign Joey's assistant ID |

### Phase 5: Webhook (Make.com)

> **Note:** Phase 5 is built in reverse order — the scenario (5.2) must exist before its webhook URL can be assigned to the Vapi assistant (5.1). The script `scripts/create-make-scenario.js` does the heavy lifting.

| Step | Action | What It Does |
|------|--------|--------------|
| **5.0a** | Generate Make REST API token | Profile → API access → Add token. Scopes: `scenarios:read/write`, `hooks:read/write`, `connections:read`, `teams:read`. Save to `.env` as `MAKE_API_KEY`. |
| **5.0b** | Add Gmail + Google connections in Make UI | One-time Google OAuth (cannot be done via API). Adds two connections — Gmail (for sending notifications) and Google (for Sheets append). |
| **5.0c** | Create the `Calls` tab in the spreadsheet | Run the Apps Script in the "Calls Tab Schema" section below to add a `Calls` tab with proper headers. |
| **5.2a** | Create custom webhook | `POST /api/v2/hooks` with `typeName: "gateway-webhook"` → captures `webhook URL` and `hookId`. |
| **5.2b** | Build & activate scenario | Run `node scripts/create-make-scenario.js` → POSTs the 3-module blueprint (Webhook → filter → Gmail → Sheets addRow), then PATCHes scheduling and POSTs `/start`. |
| **5.1** | PATCH Vapi assistant `server.url` | `PATCH /assistant/{id}` with `{"server":{"url":"<MAKE_WEBHOOK_URL>"}}` — wires Vapi's end-of-call reports to the Make webhook. |

### Phase 6: Testing

| Step | Skill | What It Does |
|------|-------|--------------|
| **6.1** | `/vapi-create-call` | Outbound test call to your own phone |
| **6.2** | Call the Vapi number | Inbound test — full qualifying flow end-to-end |
| **6.3** | Verify in Make + Sheets + Gmail | Make scenario history shows a successful run; `Calls` tab has a new row; an email lands in your inbox |

---

## Joey's System Prompt

Use this as the system message when creating the assistant. Source of truth is `prompts/joey-system.md`.

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

> **CRITICAL:** Hardcode the actual Google Spreadsheet ID in the tool description above. If you don't, the LLM will guess a fake ID and the tool call will fail with "Requested entity was not found."

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
| M: Call Duration | _Reserved — currently NOT filled. See `Calls` tab below for post-call data._ | — |

### Apps Script to Create the Sheet

Run this in [Google Apps Script](https://script.google.com) to auto-create the sheet with headers and formatting:

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

After running, copy the Spreadsheet ID from the logs and hardcode it in the logLead tool description and `.env`.

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

> The Make `addRow` module relies on `Calls` being a real tab with headers in row 1. If the tab doesn't exist when the scenario fires, the module will error and the whole scenario run fails (the Gmail step won't fire either).

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

**Key auth/format details (verified working on 2026-05-01):**
- Make REST API: `Authorization: Token <api_key>` (capital T, not `Bearer`)
- Webhook creation: `POST /api/v2/hooks?teamId=<id>` with `{ typeName: "gateway-webhook" }`
- Scenario creation: `POST /api/v2/scenarios?confirmed=true` — `blueprint` and `scheduling` must be **JSON-stringified** values, not nested objects
- Activation requires `scheduling: {type:"indefinitely", interval:900}` — `type` alone returns `IM008 "Invalid interval"`
- Module names that work: `gateway:CustomWebHook` v1, `google-email:sendAnEmail` v4, `google-sheets:addRow` v2, `google-sheets:updateRow` v2. Names that DON'T work: `searchRows`, `listRows`, `ActionSendEmail`. Module discovery via `/api/v2/sdk/apps/*` requires the `sdk-apps:read` scope on the API token.

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

1. Receives the webhook POST (Make replies with `{}` instantly — that's automatic)
2. Filters for `message.type == "end-of-call-report"` (skips other message types Vapi sends mid-call)
3. Reads from the payload: `transcript`, `summary`, `recordingUrl`, `durationSeconds`, `cost`, `endedReason`, `call.customer.number`
4. Formats duration as `mm:ss` and cost as `$X.XXXX`
5. Sends an HTML email notification (Module 2 — Gmail `sendAnEmail`)
6. Appends a row to the `Calls` tab of the leads spreadsheet (Module 3 — Google Sheets `addRow`)

> **Why append to a `Calls` tab instead of updating the Lead row's "Call Duration"?**
> The original design called for matching by phone number and updating the existing lead row's `Call Duration` column. That requires a `searchRows`-style module which is not exposed via Make's blueprint API at the verified module versions (only `addRow` and `updateRow` worked). Append-to-Calls keeps post-call data co-located with leads (same spreadsheet) and avoids the search-then-update dance. The original lead row in the `Leads` tab is still written by Joey during the call via the `logLead` tool.

---

## Key Vapi Concepts

| Concept | What It Means | Relevant Skill |
|---------|--------------|----------------|
| **Assistant** | AI agent = LLM + voice + transcriber + tools + prompt | `/vapi-create-assistant` |
| **Tool** | Action the assistant takes during a call | `/vapi-create-tool` |
| **Phone Number** | Real phone number assigned to an assistant | `/vapi-create-phone-number` |
| **Server URL** | Your endpoint for call events and reports | `/vapi-setup-webhook` |
| **Squad** | Multi-assistant with handoffs (NOT needed here) | `/vapi-create-squad` |
| **Workflow** | Node-based conversation flow (NOT needed here) | `/vapi-create-workflow` |
| **Hooks** | Automated actions on call events | Part of assistant config |
| **`toolIds`** | Array of saved tool IDs attached to the assistant | Part of assistant config |
| **`{{now}}`** | Template variable — Vapi replaces with current date/time | Used in prompts |

### Vapi MCP Documentation

When you need to look up anything beyond the skills, use:
```
mcp__vapi-docs__searchDocs(query: "your question here")
```

---

## Lessons Learned (from the initial build)

These are critical gotchas discovered during the first build. Read these BEFORE starting.

### 1. Google Sheets tool MUST have hardcoded spreadsheet ID

The LLM will **guess** the spreadsheet ID if you don't tell it explicitly. On the first test call, the agent called `logLead` with `spreadsheetId: "polarcrest-leads"` instead of the actual Google Sheets ID, resulting in `"Requested entity was not found."` error.

**Fix:** Hardcode the real spreadsheet ID AND the range directly in the tool's `description` field:
```
"ALWAYS use spreadsheetId: your-spreadsheet-id-here and range: Leads!A:M"
```

### 2. System prompt must explicitly tell Joey to use logLead

Just having the tool attached via `toolIds` is NOT enough. The LLM won't reliably call it unless the system prompt explicitly says to. Add it as a numbered step in "Your job on every call":
```
10. Log the lead using the logLead tool — include all collected info (name, phone, email, service type, equipment details, location, timeline, emergency flag, appointment date/time, and any notes)
```

### 3. Vapi voice `Lily` is RETIRED (as of March 1, 2026)

Lily was part of a legacy voice set that was phased out. Attempting to set `voiceId: "Lily"` returns:
```
"The Lily voice is part of a legacy voice set that is being phased out"
```

**Current supported Vapi voices (verified via API on 2026-05-01):** Clara, Godfrey, Layla, Sid, Gustavo, Elliot, Kylie, Rohan, Lily, Savannah, Hana, Neha, Cole, Harry, Paige, Spencer, Nico, Kai, Emma, Sagar, Neil, Naina, Leah, Tara, Jess, Leo, Dan, Mia, Zac, Zoe.

> Note: the API still accepts `Lily` despite the earlier deprecation message — but Vapi may remove it again. Stick with the verified list above.

**Recommended for Joey:** `Elliot` — Vapi's flagship male voice (warm, professional, 30s). `Mason` is NOT in the supported list and will return a 400 error.

### 4. firstMessage — keep it simple, no special characters

Use a clean, simple greeting. Escaped characters or punctuation can cause TTS to behave oddly:
```
"Thanks for calling PolarCrest HVAC, this is Joey. How can I help you today?"
```
No exclamation marks, no special characters, no last name.

### 5. Call Duration can't be filled by the assistant

Joey doesn't know the call duration while the call is happening — that data only exists in the **end-of-call report** sent to the webhook AFTER the call ends. The Make scenario handles this by:
- Extracting `durationSeconds` from the end-of-call report
- Formatting it as `mm:ss`
- Appending a new row to the `Calls` tab of the spreadsheet (separate from the `Leads` tab Joey writes to)

### 6. Create the Google Sheet BEFORE testing

The Google Sheets tool will fail if the spreadsheet doesn't exist yet. Create it during Phase 1 (Foundation), not during testing. Use the Apps Script function above to auto-create it with proper headers and formatting.

### 7. endCall and transferCall CAN be saved tools and attached via `toolIds`

Earlier guidance said these had to be inline in `model.tools`. That's no longer true — verified on 2026-05-01 that creating `endCall` and `transferCall` as saved tools and attaching them via `model.toolIds` works fine alongside Google Calendar and Sheets tools. Treat all 5 the same way: create once, reference by ID.

The inline-in-`model.tools` approach still works too, but the saved-tool path keeps tool definitions in one place (`config/tools.json`) and avoids redefining them in every assistant.

### 8. Vapi API env loading on Windows/Git Bash

When using `curl` with the Vapi API from Git Bash on Windows, load env vars with:
```bash
export $(grep -v '^#' .env | xargs)
```
The `source .env` approach doesn't reliably export the variables for subcommands.

### 9. Test both outbound AND inbound calls

- **Outbound** (`/vapi-create-call`): Tests that the assistant works, voice sounds good, tools fire
- **Inbound** (call the Vapi number): Tests the full production flow including phone number routing

Both are needed. Issues can appear in one but not the other.

### 10. GPT-4.1 is excellent for voice AI tool calling

GPT-4.1 reliably:
- Asks one question at a time (follows the system prompt structure)
- Calls tools in parallel when appropriate (bookAppointment + logLead in one turn)
- Handles edge cases well (emergency triage, area disqualification, transfer requests)
- Keeps responses concise for natural conversation flow

Temperature 0.7 with maxTokens 300 is a good balance for conversational yet focused responses.

### 11. HVAC-specific: Emergency triage must come BEFORE the standard flow

Unlike a construction lead qualifier, HVAC callers may have safety-critical issues. If the system prompt runs the standard flow first (ask project type, ask location, etc.) before handling gas smell or CO alarms, this is a dangerous failure mode. Emergency triage must be the FIRST conditional block in the prompt — not step 4 or 5.

### 12. Canadian phone number formatting

Vapi phone numbers for Canada follow E.164 format: `+1XXXXXXXXXX`. When transferring calls or setting the emergency line, use `+19057124499` not `(905) 712-4499`. When Joey *speaks* the number to a caller, he says it as digits: *"9-0-5, 7-1-2, 4-4-9-9"* — not as a block — for clarity over voice.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| API calls return 401 | Check `VAPI_API_KEY` in `.env` — re-run `/vapi-setup-api-key`. Use private key, not public key |
| Google Calendar tools fail | Reconnect Google Calendar in Vapi Dashboard > Integrations |
| Google Sheets tool returns "entity not found" | Hardcode the real spreadsheet ID in the logLead tool description |
| Google Sheets tool fails | Reconnect Google Sheets in Vapi Dashboard > Integrations |
| Joey doesn't speak first | Verify `firstMessageMode` is `"assistant-speaks-first"` |
| Joey gives exact pricing | Strengthen the "NEVER give exact pricing" rule in system prompt |
| Joey skips emergency triage | Move emergency triage block to the TOP of the system prompt, before the standard flow |
| Joey books appointment for gas smell caller | Add explicit rule: "For gas smell or CO alarm, do NOT book — deliver safety protocol and end call" |
| Transcription misses "PolarCrest" | Add to `transcriber.keywords` with boost value — `"PolarCrest:3"` |
| Webhook not receiving events | Check `serverUrl` on assistant — must be publicly accessible |
| Calls drop after greeting | Check `maxTokens` isn't too low in model config |
| Voice sounds wrong | Check `voiceId` against the supported list (Lesson #3). Use `Elliot` for Joey |
| Call duration not in `Calls` tab | This row is appended by the Make scenario, not Joey. Open Make → scenario history to see if it ran. Common cause: `Calls` tab missing — re-run the Apps Script from CLAUDE.md to create it |
| Make scenario shows "Sheet not found" error | The `Calls` tab doesn't exist in the spreadsheet yet — run the Apps Script `createPolarCrestCallsTab()` |
| Make scenario didn't fire | Check Vapi assistant `server.url` is pointing at the Make webhook (`PATCH /assistant/{id}` body: `{"server":{"url":"..."}}`). Then check Make scenario is **active** (toggle ON, isActive=true) |
| Joey promises specific tech | Add rule: "NEVER promise a specific technician by name" |

---

## Scope Boundaries

- **Not a Squad** — Joey is solo. Upgrade to Squad if department routing (residential vs. commercial) is needed later.
- **Not a Workflow** — Qualifying flow is prompt-driven. Upgrade to Workflow if deterministic branching is needed.
- **Not production** — PolarCrest HVAC Solutions is fictional. This is a demo/template for the Zayn.ai voice agent portfolio.
