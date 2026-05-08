import urllib.request, json, sys, os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("VAPI_API_KEY")
assistant_id = "0a841403-2753-4179-a33b-b0999106d264"
phone_number_id = "8f7cc965-6b43-4d61-a914-efa07ec2e54f"

# Pass your number as argument, e.g.: python test-call.py +19055550100
# Falls back to your number if no argument given
to_number = sys.argv[1] if len(sys.argv) > 1 else "+12892791234"  # replace with your number

body = json.dumps({
    "assistantId": assistant_id,
    "phoneNumberId": phone_number_id,
    "customer": {
        "number": to_number
    }
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.vapi.ai/call",
    data=body,
    method="POST",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    print(f"Call started!")
    print(f"  Call ID : {data['id']}")
    print(f"  To      : {to_number}")
    print(f"  Status  : {data.get('status', 'queued')}")
    print(f"\nPick up your phone — Joey will call you in a few seconds.")
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode()}")
