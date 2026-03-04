import requests
import json
import time

def call_local_llm(prompt):
    api_key = "actualapikey"
    
    if not api_key.startswith("gsk_") or len(api_key) < 20:
        print("ERROR: Please paste your valid Groq API key into llm_client.py.")
        return {}

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Switched to 8b-instant to allow larger token payloads on the free tier
    payload = {
        "model": "llama-3.1-8b-instant", 
        "messages": [
            {
                "role": "system", 
                "content": "You are an expert operational data extraction assistant. You MUST output your response in completely valid, strict JSON format. Do not include markdown formatting like ```json in the output."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.1
    }
    
    # Retry loop to handle API rate limits gracefully
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return json.loads(content)
        except requests.exceptions.HTTPError as e:
            if response.status_code in [413, 429]:
                print(f"   [!] API Limit hit. Pausing for 15 seconds to let the server cool down... (Attempt {attempt + 1}/3)")
                time.sleep(15)
            else:
                print(f"Error calling Groq API: {e}")
                return {}
        except Exception as e:
            print(f"Error: {e}")
            return {}
            
    return {}
