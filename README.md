# MCP Basic Agent

A FastAPI-based agent that leverages OpenAI's LLMs and supports tool calls for tasks like fetching the current time. This project demonstrates how to orchestrate LLM interactions with custom tools using Python.

## Features

- **LLM Chat**: Communicate with OpenAI models via API.
- **Tool Calls**: Extend LLM capabilities with custom Python functions (e.g., get current time).
- **Environment Variable Support**: Securely manage API keys using `.env` files.

## Getting Started

### Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- OpenAI API key

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/mcp-basic-agent.git
   cd mcp-basic-agent
    ```
2. Install dependencies
    ```sh
    pip install -r requirements.txt
    ```
3. Set up environment variables
    Create a .env file in the project root:
    OPENAI_API_KEY=your_openai_api_key_here

### Running the Agent
Start the FastAPI server using Uvicorn:
    ```sh
    uvicorn main-backup:app --reload
    ```

The API will be available at http://127.0.0.1:8000

## API Usage
Endpoint: /ask
POST request to interact with the agent.

Request Body

```json
{
"message": "What time is it?"
}
```
Example Response

```json
{
"response": "The current system time is 2025-07-13 14:23:45"
}
```

## Project Structure
```
mcp-basic-agent/
├── app/
│   ├── client/
│   │   └── openai_client.py
│   ├── main.py
│   ├── orchestrator/
│   │   └── agent_router.py
│   ├── schema.py
│   └── tools/
│       └── time.py
├── [main-backup.py]
├── [requirements.txt]
├── .env
└── [README.md]
```

Basic MCP architecture

```

                        ┌──────────────────────────────┐
                        │         MCP Host (UI)         │
                        │  e.g., VS Code, FastAPI App   │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │      MCP Client (LLM SDK)     │
                        │    e.g., openai.ChatCompletion│
                        └──────────────┬───────────────┘
                                       │
                            Tool calls/Functions
                                       ▼
                 ┌─────────────────────────────────────────┐
                 │              MCP Server                 │
                 │  Interprets tool request and routes it  │
                 └──────────────┬──────────────┬────────────┘
                                │              │
                         ┌──────▼─────┐   ┌─────▼────────┐
                         │ Inline Tool│   │ External Tool│
                         │ (Python fn)│   │(API endpoint)│
                         └────────────┘   └──────────────┘

```

