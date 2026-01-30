import requests
import os
from dotenv import load_dotenv

load_dotenv()


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """
You are a productivity and planning assistant inside a CLI app called LifeOS.
just answer the questions which user asks
Give practical, concise, actionable advice only if user asks for advices/suggestions.
Prefer bullet points.
Be honest and realistic.
"""

CONTEXT_PROMPT = """
Context:
The user uses LifeOS to track habits, notes, and expenses.
They want help with planning, consistency, discipline, and organization.
Advice should be realistic for a student with limited time.
"""

def ask_ai(user_question):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY.strip()}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT.strip()},
            {"role": "system", "content": CONTEXT_PROMPT.strip()},
            {
                "role": "user",
                "content": f"""
User question:
{user_question}

Answer with clear steps or suggestions.
""".strip()
            }
        ],
        "temperature": 0.6,
        "max_tokens": 300
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        data = response.json()
    except Exception as e:
        return f"AI error : {e}"

    if "error" in data:
        return f"AI Error: {data['error'].get('message')}"

    return data["choices"][0]["message"]["content"].strip()


