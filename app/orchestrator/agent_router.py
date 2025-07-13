# app/orchestrator/agent_router.py

from app.client.openai_client import chat_with_llm
from app.tools.time_tool import get_current_time, tool_schema as time_tool_schema
from app.tools.weather_tool import get_weather, tool_schema as weather_tool_schema
from app.tools.github_tool import summarize_github_issue, tool_schema as github_tool_schema

def run_agent(user_input: str) -> str:
    user_msg = {"role": "user", "content": user_input}
    tools = [time_tool_schema, weather_tool_schema, github_tool_schema]

    # Step 1 — let model pick the tool
    response = chat_with_llm(
        messages=[user_msg],
        tools=tools,
        tool_choice="auto",
        model="gpt-4.1-nano",
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        fn_name = tool_call.function.name
        args = tool_call.function.arguments

        import json
        args_dict = json.loads(args)

        if fn_name == "get_current_time":
            result = get_current_time()
        elif fn_name == "get_weather":
            result = get_weather(args_dict.get("city"))
        elif fn_name == "summarize_github_issue":
            result = summarize_github_issue(args_dict.get("url"))
        else:
            result = "Unknown tool."

        tool_result = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": fn_name,
            "content": result
        }

        # Step 2 — return tool result back to model
        second_response = chat_with_llm(
            messages=[user_msg, response_message, tool_result],
            model="gpt-4.1-nano",
        )

        return second_response.choices[0].message.content

    return response_message.content
