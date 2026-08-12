import os
import json
import re
import asyncio
import cohere
from dotenv import load_dotenv
from tenacity import retry, wait_random_exponential, stop_after_attempt

load_dotenv()

# Initialize Cohere Async Client
client = cohere.AsyncClient(api_key=os.getenv("COHERE_API_KEY"))

# 1. Define ask_cohere ABOVE final_report with Retry Logic
# Tenacity will automatically catch any API hiccups (like 503s or temporary 429s) and retry safely
@retry(
    wait=wait_random_exponential(multiplier=2, max=32),
    stop=stop_after_attempt(5)
)
async def ask_cohere(prompt: str) -> str:
    response = await client.chat(
        model="command-r-08-2024",  # <-- Updated to the strict version name
        message=prompt,
        response_format={"type": "json_object"}
    )
    return response.text.strip()


# 2. Define final_report using ask_cohere and re.sub
async def final_report(final_llm_prompt: str) -> dict:
    raw_text = await ask_cohere(final_llm_prompt)
    
    # Clean markdown blocks if present
    raw_text = raw_text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    elif raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    raw_text = raw_text.strip()

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        if "Extra data" in str(e):
            try:
                # Convert back-to-back objects into a valid JSON array
                array_string = re.sub(r'\}\s*\{', '},{', raw_text)
                json_array = json.loads(f"[{array_string}]")
                
                # Merge into one single dictionary
                merged_dict = {}
                for obj in json_array:
                    merged_dict.update(obj)
                return merged_dict
            except Exception:
                decoder = json.JSONDecoder()
                parsed_obj, _ = decoder.raw_decode(raw_text)
                return parsed_obj
        else:
            raise e