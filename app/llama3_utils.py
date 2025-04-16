import httpx

GROQ_API_KEY = "your-groq-api-key"
LLM_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_llama3(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4
    }

    with httpx.Client(timeout=60) as client:
        response = client.post(LLM_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
