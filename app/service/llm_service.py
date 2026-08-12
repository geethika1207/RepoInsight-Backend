import os
import json
import re
import asyncio
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Initialize Google GenAI client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 1. TEMPORARILY COMMENTED OUT the retry block to stop hiding the real error
# @retry(
#     retry=retry_if_exception_type((ServerError, APIError)),
#     wait=wait_random_exponential(multiplier=2, max=32),
#     stop=stop_after_attempt(5)
# )
async def ask_gemini(prompt: str) -> str:
    response = await client.aio.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            # 2. ADDED SAFETY SETTINGS: This prevents Google from blocking your 
            # security reviews when it sees words like "vulnerability" or "exploit"
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold="BLOCK_NONE",
                )
            ]
        ),
    )
    return response.text.strip()

# 2. Define final_report using ask_gemini and re.sub
async def final_report(final_llm_prompt: str) -> dict:
    raw_text = await ask_gemini(final_llm_prompt)
    
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