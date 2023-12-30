from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import get_answer
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]

@app.post("/chat/{conversation_id}")
async def chat(conversation_id: str,conversation: Conversation):
    result = await run_in_threadpool(get_answer, conversation)

    return {"id": conversation_id, "reply": result}

