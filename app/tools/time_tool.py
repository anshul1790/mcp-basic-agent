from datetime import datetime

def get_current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

tool_schema = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Returns the current system time",
        "parameters": {
            "type": "object",
            "properties": {}
        },
        "required": []
    }
}
