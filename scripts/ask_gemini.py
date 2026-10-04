import os
import argparse
import requests
import json

API_KEY = "AQ.Ab8RN6JZ3IWXI378tqZVs68Dq188Q-zS_vwbOeaUUP8OpSvAiw"

def generate_content(prompt, output_path, model="flash"):
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
        "x-goog-api-key": API_KEY
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
