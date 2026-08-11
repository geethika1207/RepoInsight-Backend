import os
from groq import AsyncGroq
from dotenv import load_dotenv
import json

load_dotenv()

client = AsyncGroq(api_key=os.getenv("API_KEY"))


async def ask_groq(prompt: str) -> str:
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content
    raw = raw.strip()

    if raw.startswith("```json"):
        raw = raw[7:]

    if raw.startswith("```"):
        raw = raw[3:]

    if raw.endswith("```"):
        raw = raw[:-3]

    return raw.strip()


async def final_report(final_llm_prompt):
    raw = await ask_groq(final_llm_prompt)
    return json.loads(raw)