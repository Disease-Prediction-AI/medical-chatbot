from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis
import requests
import json
import os


r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    username=os.getenv("REDIS_USERNAME"), # use your Redis user. More info https://redis.io/docs/management/security/acl/
    password=os.getenv("REDIS_PASSWORD"), # use your Redis password
    db=0)

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

    response = requests.post(f"http://{os.getenv('chat-service')}/chat/{conversation_id}", json=existing_conversation)
    response.raise_for_status()
    assistant_message = response.json()["reply"]

    existing_conversation["conversation"].append({"role": "assistant", "content": assistant_message})

    r.set(conversation_id, json.dumps(existing_conversation))

    return existing_conversation