from dotenv import load_dotenv
from pydantic import BaseModel,Field
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main import agent
load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])

#pydantic class

class UserRequirements(BaseModel):
    conversation_id : str = Field("connversation id.")
    user_query:str = Field(description="user query about the trip and the requirements.")

class AiResponse(BaseModel):
    results:str = Field(description="the ai response based on the user requirements.")


conversation = {}

@app.post("/ask",response_model=AiResponse)
def Chatbot(query:UserRequirements):

    if query.conversation_id not in conversation:
        conversation[query.conversation_id] = []

    messages = conversation[query.conversation_id]

    messages.append({"role":"user","content":query.user_query})

    response = agent.invoke({"messages":messages})

    conversation[query.conversation_id] = response['messages']

    # response = agent.invoke({"messages":[{"role":"user","content":query.user_query}]})

    return AiResponse(results=response["messages"][-1].content)

    
    