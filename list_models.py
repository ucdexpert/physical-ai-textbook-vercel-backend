import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

async def list_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set")
        return

    provider = AsyncOpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    try:
        models = await provider.models.list()
        print("Available models:")
        for m in models.data:
            print(f"- {m.id}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(list_models())
