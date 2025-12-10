import os
import asyncio
from dotenv import load_dotenv
from pathlib import Path
from openai import AsyncOpenAI

async def test_key():
    # Explicitly load .env from the same directory
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY not found in .env")
        return
        
    print(f"Loaded Key: {key[:5]}...{key[-5:]}")
    
    client = AsyncOpenAI(
        api_key=key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    # Test 1: Standard Model
    print("\n--- Testing gemini-1.5-flash ---")
    try:
        response = await client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": "user", "content": "Hi"}],
        )
        print("SUCCESS: 1.5-flash works!")
    except Exception as e:
        print(f"FAILURE: 1.5-flash error: {e}")

    # Test 2: Configured Model (2.5-flash?)
    print("\n--- Testing gemini-2.5-flash ---")
    try:
        response = await client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[{"role": "user", "content": "Hi"}],
        )
        print("SUCCESS: 2.5-flash works!")
    except Exception as e:
        print(f"FAILURE: 2.5-flash error: {e}")

if __name__ == "__main__":
    asyncio.run(test_key())
