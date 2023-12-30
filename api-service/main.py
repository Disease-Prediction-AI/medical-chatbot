from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis
import requests
import json


r = redis.Redis(host='localhost', port=6379, db=0)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]



@app.get("/api/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    existing_conversation_json = r.get(conversation_id)
    if existing_conversation_json:
        existing_conversation = json.loads(existing_conversation_json)
        return existing_conversation
    else:
        return {"error": "Conversation not found"}



@app.post("/api/conversation/{conversation_id}")
async def create_message(conversation_id: str, conversation: Conversation):
    existing_conversation_json = r.get(conversation_id)
    if existing_conversation_json:
        existing_conversation = json.loads(existing_conversation_json)
    else:
        existing_conversation = {"conversation": [{"role": "system", "content": "You are a medical helpful assistant."}]}

    existing_conversation["conversation"].append(conversation.dict()["conversation"][-1])

    response = requests.post(f"http://localhost:8000/chat/{conversation_id}", json=existing_conversation)
    response.raise_for_status()
    assistant_message = response.json()["reply"]

    existing_conversation["conversation"].append({"role": "assistant", "content": assistant_message})

    r.set(conversation_id, json.dumps(existing_conversation))

    return existing_conversation