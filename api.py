from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from main import agent
load_dotenv()

app = FastAPI()


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request / Response Models
# --------------------------------------------------

class UserRequirements(BaseModel):
    conversation_id: str = Field(
        description="Unique ID for the user's conversation."
    )

    user_query: str = Field(
        description="User's travel question or requirements."
    )


class AiResponse(BaseModel):
    results: str = Field(
        description="AI response based on the user's requirements."
    )


# --------------------------------------------------
# Conversation Memory
# --------------------------------------------------

conversation = {}

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "AI Travel Agent API",
    }


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@app.post("/ask", response_model=AiResponse)
async def chatbot(query: UserRequirements):

    if query.conversation_id not in conversation:
        conversation[query.conversation_id] = []

    messages = conversation[query.conversation_id]

    messages.append(
        {
            "role": "user",
            "content": query.user_query,
        }
    )

    response = await agent.ainvoke(
        {
            "messages": messages
        }
    )

    conversation[query.conversation_id] = response["messages"]

    return AiResponse(
        results=response["messages"][-1].content
    )
