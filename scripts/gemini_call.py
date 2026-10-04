#!/usr/bin/env python3
import sys, json, os, urllib.request

model = sys.argv[1] if len(sys.argv) > 1 else "gemini-3.8-flash"
prompt = sys.stdin.read()

url = "http://localhost:4000/v1/chat/completions"
headers = {"Content-Type": "application/json"}
if "LITELLM_MASTER_KEY" in os.environ:
    headers["Authorization"] = f"Bearer {os.environ['LITELLM_MASTER_KEY']}"

data = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode("utf-8")

req = urllib.request.Request(url, data=data, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
        content = res["choices"][0]["message"]["content"]
        print(content)
        
        with open("logs/llm_usage.csv", "a") as f:
            usage = res.get("usage", {})
            f.write(f"{model},{usage.get('prompt_tokens', 0)},{usage.get('completion_tokens', 0)}\n")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
