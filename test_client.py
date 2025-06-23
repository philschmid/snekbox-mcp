import asyncio
import os
from fastmcp import Client

client = Client("http://localhost:8000/mcp")


async def call_tool(code: str):
    async with client:
        result = await client.call_tool("execute", {"code": code})
        print(result[0].text)


asyncio.run(call_tool("print('hello world')"))


def gemini_call():
    gemini_call = f"""from google import genai

client = genai.Client(api_key="{os.getenv('GEMINI_API_KEY')}")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)"""
    print(gemini_call)
    return gemini_call


asyncio.run(call_tool(gemini_call()))
