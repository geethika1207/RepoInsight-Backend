import os
import json
import re
import asyncio
import cohere
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client (Tier 1: ultra-low latency Llama-3 inference)
try:
    from groq import AsyncGroq
    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_client = AsyncGroq(api_key=groq_api_key) if groq_api_key else None
except ImportError:
    groq_client = None

# Initialize Cohere client (Tier 3: dependable grounded JSON synthesis)
cohere_api_key = os.getenv("COHERE_API_KEY")
cohere_client = cohere.AsyncClient(api_key=cohere_api_key) if cohere_api_key else None


# Groq (Llama-3-70B) for Fast Structural Generation

async def ask_groq(prompt: str) -> str:
    """Fast primary model to generate initial JSON report."""
    if not groq_client:
        raise ValueError("Groq client not available or GROQ_API_KEY is missing.")
    
    response = await groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a senior software architect. Analyze the provided repository context and output strictly valid JSON matching the requested report format."
            },
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    return response.choices[0].message.content.strip()


# Google Gemini 1.5 Flash Fallback (High-Context Window)

async def ask_gemini(prompt: str) -> str:
    """Fallback model if Groq is rate-limited (HTTP 429) or throttled."""
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise ValueError("GEMINI_API_KEY is missing.")

    import urllib.request
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.2
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, lambda: urllib.request.urlopen(req, timeout=30))
    res_data = json.loads(response.read().decode("utf-8"))
    return res_data["candidates"][0]["content"]["parts"][0]["text"].strip()


# Cohere Command-R (Grounded Synthesizer with Strict JSON Schema)

async def ask_cohere(prompt: str) -> str:
    """Final dependable engine with strict JSON object enforcement."""
    if not cohere_client:
        raise ValueError("Cohere client not available or COHERE_API_KEY is missing.")
        
    response = await cohere_client.chat(
        model="command-r-08-2024",
        message=prompt,
        response_format={"type": "json_object"}
    )
    return response.text.strip()


# Cascading Router with Automatic Multi-Tier Failover

async def route_llm_request(prompt: str) -> str:
    """
    Cascading Multi-LLM Router:
    1. Try Groq (Llama-3-70B) for low latency.
    2. If rate-limited (429) or down, fall back to Gemini 1.5 Flash.
    3. If Gemini fails, fall back to Cohere Command-R with exponential backoff retry.
    """
    # Try Tier 1: Groq
    try:
        return await ask_groq(prompt)
    except Exception as e:
        # Log and migrate gracefully if Groq hits rate limit or quota
        print(f"[Router Notice] Groq unavailable ({e}). Migrating request to Tier 2 (Gemini)...")

    # Try Tier 2: Gemini
    try:
        return await ask_gemini(prompt)
    except Exception as e:
        # Log and migrate to Tier 3 if Gemini fails
        print(f"[Router Notice] Gemini unavailable ({e}). Migrating request to Tier 3 (Cohere)...")

    # Final Fallback: Cohere Command-R with exponential backoff retry (up to 5 attempts)
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            return await ask_cohere(prompt)
        except Exception as e:
            if attempt == max_attempts - 1:
                # All fallbacks and attempts exhausted
                raise RuntimeError(f"All LLM tiers (Groq, Gemini, Cohere) failed. Last error: {e}")
            wait_seconds = min(2 ** attempt * 2, 32)
            print(f"[Cohere Retry] Attempt {attempt + 1} failed. Retrying in {wait_seconds}s...")
            await asyncio.sleep(wait_seconds)


# Deserialization and Self-Healing JSON Parser

async def final_report(final_llm_prompt: str) -> dict:
    # Route through cascading multi-LLM router
    raw_text = await route_llm_request(final_llm_prompt)
    
    # Strip markdown code fencing if model wrapped the JSON in ```json ... ```
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
        # Self-healing parser: catches adjacent unpunctuated JSON roots (e.g., }{ -> },{)
        if "Extra data" in str(e):
            try:
                # Insert comma between back-to-back objects and wrap in a list
                array_string = re.sub(r'\}\s*\{', '},{', raw_text)
                json_array = json.loads(f"[{array_string}]")
                
                # Merge into one clean consolidated report dictionary
                merged_dict = {}
                for obj in json_array:
                    merged_dict.update(obj)
                return merged_dict
            except Exception:
                # Fallback to streaming raw decode if array conversion fails
                decoder = json.JSONDecoder()
                parsed_obj, _ = decoder.raw_decode(raw_text)
                return parsed_obj
        else:
            raise e