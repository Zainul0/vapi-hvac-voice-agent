"""Create Joey - the PolarCrest HVAC voice receptionist on Vapi."""
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env():
    env = {}
    with open(os.path.join(ROOT, ".env"), "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


def update_env(key, value):
    path = os.path.join(ROOT, ".env")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            break
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def main():
    env = load_env()
    api_key = env["VAPI_API_KEY"]

    with open(os.path.join(ROOT, "prompts", "joey-system.md"), "r", encoding="utf-8") as f:
        system_prompt = f.read()

    tool_ids = [
        env["VAPI_GCAL_CHECK_TOOL_ID"],
        env["VAPI_GCAL_CREATE_TOOL_ID"],
        env["VAPI_GSHEETS_TOOL_ID"],
        env["VAPI_END_CALL_TOOL_ID"],
        env["VAPI_TRANSFER_CALL_TOOL_ID"],
    ]

    payload = {
        "name": "Joey - PolarCrest HVAC Receptionist",
        "firstMessage": "Thanks for calling PolarCrest HVAC, this is Joey. How can I help you today?",
        "firstMessageMode": "assistant-speaks-first",
        "model": {
            "provider": "openai",
            "model": "gpt-4.1",
            "temperature": 0.7,
            "maxTokens": 300,
            "toolIds": tool_ids,
            "messages": [
                {"role": "system", "content": system_prompt}
            ],
        },
        "voice": {
            "provider": "vapi",
            "voiceId": "Elliot",
        },
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-3",
            "language": "en",
            "keywords": [
                "PolarCrest:3",
                "furnace:2",
                "HVAC:2",
                "Mississauga:2",
                "Brampton:2",
                "Oakville:2",
                "Enbridge:2",
                "thermostat:1",
                "boiler:1",
            ],
        },
        "backgroundSound": "office",
        "backchannelingEnabled": True,
        "backgroundDenoisingEnabled": True,
        "hooks": [
            {
                "on": "customer.speech.timeout",
                "options": {"timeoutSeconds": 8, "triggerMaxCount": 2},
                "do": [
                    {
                        "type": "say",
                        "exact": "Are you still there? I want to make sure I get you sorted out.",
                    }
                ],
            }
        ],
    }

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.vapi.ai/assistant",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "PolarCrest-Builder/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {err_body}", file=sys.stderr)
        sys.exit(1)

    out_path = os.path.join(ROOT, "config", "assistant.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    update_env("VAPI_ASSISTANT_ID", data["id"])

    print(f"Assistant created: {data['id']}")
    print(f"Saved to: {out_path}")
    print(f"Updated .env with VAPI_ASSISTANT_ID")


if __name__ == "__main__":
    main()
