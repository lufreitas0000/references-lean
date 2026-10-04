import os
import argparse
import requests
import json
from pathlib import Path

def load_api_key():
    """Load Gemini API key from environment variables or local .env file."""
    # Check standard environment variables first
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key.strip()

    # Fallback to local .env file at repo root or current working dir
    for env_path in [
        Path(__file__).resolve().parent.parent / ".env",
        Path.cwd() / ".env"
    ]:
        if env_path.is_file():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("\"'")
                        if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                            return v

    raise RuntimeError(
        "Gemini API key not found. Please set GEMINI_API_KEY in your environment or in a local .env file."
    )

def generate_content(prompt, output_path, model="flash"):
    api_key = load_api_key()
    print(f"Requesting generation from Gemini {model}...")
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    
    model_name = "gemini-1.5-pro" if model == "pro" else "gemini-1.5-flash"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 404 and model == "pro":
        # Fallback
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-latest:generateContent"
        res = requests.post(url, headers=headers, json=payload)
    elif res.status_code == 404 and model == "flash":
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        res = requests.post(url, headers=headers, json=payload)
        
    res.raise_for_status()
    
    data = res.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved generated content to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", type=str, required=True, help="Path to the file containing the prompt")
    parser.add_argument("--output-file", type=str, required=True, help="Path to save the output markdown")
    parser.add_argument("--model", type=str, choices=["flash", "pro"], default="flash", help="Which model to use")
    
    args = parser.parse_args()
    
    with open(args.prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()
        
    generate_content(prompt, args.output_file, args.model)
