from fastapi import FastAPI
from app.schema import PromptRequest
from app.orchestrator.agent_router import run_agent

app = FastAPI()

@app.post("/ask")
async def ask(prompt: PromptRequest):
    result = run_agent(prompt.message)
    return {"response": result}
