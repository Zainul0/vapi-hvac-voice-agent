import urllib.request, json, os
from dotenv import load_dotenv
load_dotenv()

API_KEY       = os.getenv("VAPI_API_KEY")
ASSISTANT_ID  = "0a841403-2753-4179-a33b-b0999106d264"
PHONE_ID      = "8f7cc965-6b43-4d61-a914-efa07ec2e54f"
TOOL_IDS      = {
    "checkAvailability" : "9e6d2a80-3112-4573-bd6d-434f90444e11",
    "bookAppointment"   : "7407b9e3-1ad8-4656-87ed-fd2683dd919a",
    "logLead"           : "0141dc31-8505-4a90-8c08-d413ef613912",
    "endCall"           : "ffb2c9e3-9abc-4a99-ab8a-8c3696e5bb9d",
    "transferToOffice"  : "d28f40c7-ec26-4749-8f17-ce96a495e357",
    "queryKnowledgeBase": "e1580bec-f68c-48e0-a2c1-1b383dd4b182",
}

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get(path):
    req = urllib.request.Request(f"https://api.vapi.ai{path}", headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

ok  = lambda msg: print(f"  [OK]  {msg}")
err = lambda msg: print(f"  [!!]  {msg}")
sep = lambda t:   print(f"\n{'='*50}\n  {t}\n{'='*50}")

# ── 1. Assistant config ──────────────────────────────
sep("1. ASSISTANT CONFIG")
a = get(f"/assistant/{ASSISTANT_ID}")

model = a["model"]["model"]
temp  = a["model"]["temperature"]
(ok if model == "gpt-4o-mini" else err)(f"Model      : {model}  (expected gpt-4o-mini)")
(ok if temp  <= 0.3            else err)(f"Temperature: {temp}   (expected ≤ 0.3)")
ok(f"Updated    : {a['updatedAt']}")

# ── 2. Tools attached ────────────────────────────────
sep("2. TOOLS ATTACHED")
attached = set(a["model"].get("toolIds", []))
for name, tid in TOOL_IDS.items():
    (ok if tid in attached else err)(f"{name:<22} {'attached' if tid in attached else 'MISSING'}")

# ── 3. Prompt health checks ──────────────────────────
sep("3. SYSTEM PROMPT RULES")
prompt = a["model"]["messages"][0]["content"]
checks = [
    ("Has name-spelling rule",       "NEVER skip asking for the spelling"),
    ("Has pre-booking gate",         "Pre-booking confirmation gate"),
    ("Has email spell-back",         "spell every character one at a time"),
    ("Has no-problem ban",           'NEVER say "No problem"'),
    ("Has emergency triage first",   "EMERGENCY TRIAGE"),
    ("Has {{now}} placeholder",      "{{now}}"),
    ("Has endCall step",             "Call endCall"),
    ("Has logLead step",             "Call logLead"),
]
for label, token in checks:
    (ok if token in prompt else err)(label)
print(f"\n  Prompt length: {len(prompt)} chars")

# ── 4. Phone number ──────────────────────────────────
sep("4. PHONE NUMBER")
ph = get(f"/phone-number/{PHONE_ID}")
linked = ph.get("assistantId") == ASSISTANT_ID
(ok if linked else err)(f"Linked to Joey : {'YES' if linked else 'NO — reassign needed'}")
ok(f"Number         : {ph.get('number', 'unknown')}")

# ── 5. Recent calls ──────────────────────────────────
sep("5. RECENT CALLS (last 5)")
calls = get(f"/call?assistantId={ASSISTANT_ID}&limit=5")
if not calls:
    print("  No calls found.")
else:
    for c in calls:
        cid    = c["id"][:8]
        ended  = c.get("endedReason", "unknown")
        ts     = c.get("createdAt", "")[:16]
        dur    = c.get("durationSeconds")
        dur_s  = f"{dur}s" if dur else "n/a"

        # quick compliance scan on transcript
        t = c.get("transcript", "") or ""
        violations = []
        if "no problem" in t.lower():
            violations.append("said 'No problem'")
        if "yeah" in t.lower().split():
            violations.append("said 'Yeah'")

        flag = f"  VIOLATIONS: {', '.join(violations)}" if violations else ""
        print(f"  {ts}  [{cid}]  {ended:<28}  {dur_s}{flag}")

print("\n" + "="*50)
print("  Done. Fix any [!!] items above.")
print("="*50 + "\n")
