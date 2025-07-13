from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_llm(messages, tools=None, tool_choice=None, model="gpt-4o"):
    kwargs = {
        "model": model,
        "messages": messages
    }

    if tools:
        kwargs["tools"] = tools
        if tool_choice:
            kwargs["tool_choice"] = tool_choice

    return client.chat.completions.create(**kwargs)
