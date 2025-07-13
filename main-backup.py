# from fastapi import FastAPI
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from openai import OpenAI
# import os
# from datetime import datetime

# # Load environment variable for API key
# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# app = FastAPI()

# # Tool function
# def get_current_time():
#     now = datetime.now()
#     return now.strftime("%Y-%m-%d %H:%M:%S")

# # Request schema
# class PromptRequest(BaseModel):
#     message: str

# @app.post("/ask")
# async def ask(prompt: PromptRequest):
#     user_msg = {"role": "user", "content": prompt.message}

#     # Register tool (MCP-style)
#     tools = [{
#         "type": "function",
#         "function": {
#             "name": "get_current_time",
#             "description": "Returns the current system time",
#             "parameters": {
#                 "type": "object",
#                 "properties": {}
#             },
#             "required": []
#         }
#     }]

#     # ✅ Step 1: Initial LLM call with forced tool usage
#     response = client.chat.completions.create(
#         model="gpt-4.1-nano",
#         messages=[user_msg],
#         tools=tools,
#         tool_choice={
#             "type": "function",
#             "function": {
#                 "name": "get_current_time"
#             }
#         }
#     )

#     response_message = response.choices[0].message

#     # ✅ Step 2: Tool call handling
#     if response_message.tool_calls:
#         tool_call = response_message.tool_calls[0]
#         function_name = tool_call.function.name

#         if function_name == "get_current_time":
#             result = get_current_time()

#             tool_response = {
#                 "role": "tool",
#                 "tool_call_id": tool_call.id,
#                 "name": function_name,
#                 "content": result
#             }

#             # ✅ Step 3: Let LLM incorporate tool result
#             second_response = client.chat.completions.create(
#                 model="gpt-4.1-nano",
#                 messages=[user_msg, response_message, tool_response],
#             )

#             return {
#                 "response": second_response.choices[0].message.content
#             }

#     return {
#         "response": response_message.content
#     }
