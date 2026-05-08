import urllib.request, json, os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("VAPI_API_KEY")
assistant_id = "0a841403-2753-4179-a33b-b0999106d264"

with open("prompts/joey-system.md", encoding="utf-8") as f:
    prompt = f.read()

body = json.dumps({
    "model": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "temperature": 0.3,
        "maxTokens": 300,
        "messages": [{"role": "system", "content": prompt}]
    }
}).encode("utf-8")

req = urllib.request.Request(
    f"https://api.vapi.ai/assistant/{assistant_id}",
    data=body,
    method="PATCH",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    print("SUCCESS")
    print(f"  model       : {data['model']['model']}")
    print(f"  provider    : {data['model']['provider']}")
    print(f"  temperature : {data['model']['temperature']}")
    print(f"  updatedAt   : {data['updatedAt']}")
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.reason}")
    print(e.read().decode())
