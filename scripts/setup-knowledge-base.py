"""
setup-knowledge-base.py
Run from project root: python scripts/setup-knowledge-base.py

Steps:
  1. Upload polarcrest_hvac_knowledge_base.md to Vapi
  2. Create a queryKnowledgeBase tool (type: query) referencing that file
  3. PATCH the assistant with the lean prompt + all 6 toolIds
  4. Print a summary of what changed
"""

import urllib.request, json, os, sys
from dotenv import load_dotenv
load_dotenv()

API_KEY       = os.getenv("VAPI_API_KEY")
ASSISTANT_ID  = "0a841403-2753-4179-a33b-b0999106d264"
EXISTING_TOOL_IDS = [
    "9e6d2a80-3112-4573-bd6d-434f90444e11",  # checkAvailability
    "7407b9e3-1ad8-4656-87ed-fd2683dd919a",  # bookAppointment
    "0141dc31-8505-4a90-8c08-d413ef613912",  # logLead
    "ffb2c9e3-9abc-4a99-ab8a-8c3696e5bb9d",  # endCall
    "d28f40c7-ec26-4749-8f17-ce96a495e357",  # transferToOffice
]
KB_FILE   = "polarcrest_hvac_knowledge_base.md"
PROMPT_FILE = "prompts/joey-system.md"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}

ok  = lambda msg: print(f"  [OK]  {msg}")
err = lambda msg: (print(f"  [!!]  {msg}"), sys.exit(1))
sep = lambda t:   print(f"\n{'='*52}\n  {t}\n{'='*52}")


def post_json(path, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://api.vapi.ai{path}",
        data=body,
        method="POST",
        headers={**HEADERS, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


def patch_json(path, payload):
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://api.vapi.ai{path}",
        data=body,
        method="PATCH",
        headers={**HEADERS, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


# ── 1. Upload the KB file (or reuse existing) ────────────
sep("1. KNOWLEDGE BASE FILE")

# Set to an existing file ID to skip re-upload, or None to upload fresh
EXISTING_FILE_ID = "39ada0cc-ee88-4579-8305-160c8736e547"

if EXISTING_FILE_ID:
    file_id = EXISTING_FILE_ID
    ok(f"Reusing uploaded file: {file_id}")
else:
    if not os.path.exists(KB_FILE):
        err(f"File not found: {KB_FILE}  (run from project root)")

    with open(KB_FILE, "rb") as f:
        file_data = f.read()

    boundary = "VapiFormBoundary7xTy9kPlmQ"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{KB_FILE}"\r\n'
        f"Content-Type: text/markdown\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        "https://api.vapi.ai/file",
        data=body,
        method="POST",
        headers={
            **HEADERS,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            file_resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        err(f"File upload failed {e.code}: {e.read().decode()}")

    file_id = file_resp["id"]
    ok(f"File ID   : {file_id}")
    ok(f"File name : {file_resp.get('name', KB_FILE)}")
    ok(f"Bytes     : {file_resp.get('bytes', '?')}")


# ── 2. Create the query tool ─────────────────────────────
sep("2. CREATING queryKnowledgeBase TOOL")

try:
    tool_resp = post_json("/tool", {
        "type": "query",
        "function": {
            "name": "queryKnowledgeBase",
            "description": (
                "Search the PolarCrest HVAC knowledge base. Use this tool when a caller asks about: "
                "services we offer, pricing, whether their city is in our service area, equipment brands, "
                "available rebates or incentives, FAQs, or any HVAC question you need to look up."
            ),
        },
        "knowledgeBases": [
            {
                "name": "polarcrest-hvac-kb",
                "description": "PolarCrest HVAC Solutions knowledge base — services, pricing, service areas, equipment brands, rebates, FAQs, and seasonal info.",
                "provider": "google",
                "model": "gemini-1.5-flash",
                "fileIds": [file_id],
            }
        ],
    })
except urllib.error.HTTPError as e:
    err(f"Tool creation failed {e.code}: {e.read().decode()}")

query_tool_id = tool_resp["id"]
ok(f"Tool ID   : {query_tool_id}")
ok(f"Tool name : {tool_resp['function']['name']}")


# ── 3. Load the lean system prompt ───────────────────────
sep("3. LOADING SYSTEM PROMPT")

if not os.path.exists(PROMPT_FILE):
    err(f"Prompt file not found: {PROMPT_FILE}  (run from project root)")

with open(PROMPT_FILE, encoding="utf-8") as f:
    prompt = f.read()

ok(f"Prompt length: {len(prompt)} chars")


# ── 4. PATCH the assistant ───────────────────────────────
sep("4. PATCHING ASSISTANT")

all_tool_ids = EXISTING_TOOL_IDS + [query_tool_id]

try:
    patch_resp = patch_json(f"/assistant/{ASSISTANT_ID}", {
        "model": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "maxTokens": 300,
            "toolIds": all_tool_ids,
            "messages": [{"role": "system", "content": prompt}],
        }
    })
except urllib.error.HTTPError as e:
    err(f"Assistant PATCH failed {e.code}: {e.read().decode()}")

ok(f"Model       : {patch_resp['model']['model']}")
ok(f"Temperature : {patch_resp['model']['temperature']}")
ok(f"Tool count  : {len(patch_resp['model'].get('toolIds', []))} (expected 6)")
ok(f"Prompt len  : {len(patch_resp['model']['messages'][0]['content'])} chars")
ok(f"Updated at  : {patch_resp['updatedAt']}")


# ── 5. Save outputs ──────────────────────────────────────
sep("5. SAVING CONFIG")

with open("config/assistant.json", "w", encoding="utf-8") as f:
    json.dump(patch_resp, f, indent=2)
ok("Saved: config/assistant.json")

ids_out = {
    "fileId": file_id,
    "queryToolId": query_tool_id,
}
with open("config/knowledge-base.json", "w", encoding="utf-8") as f:
    json.dump(ids_out, f, indent=2)
ok("Saved: config/knowledge-base.json")

print(f"\n{'='*52}")
print("  Done. Add queryToolId to scripts/check-joey.py TOOL_IDS.")
print(f"  queryKnowledgeBase : {query_tool_id}")
print(f"{'='*52}\n")
