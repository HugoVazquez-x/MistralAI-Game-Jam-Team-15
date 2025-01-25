from fastapi import FastAPI, Request
import os
from mistralai import Mistral
from pydantic import BaseModel
from dataclasses import dataclass, field
from pathlib import Path
from character_agent import AIAgent
from arbitrary_agent import EmotionAgent

# Initialize FastAPI app
app = FastAPI()


# Define the request and response schema
class InferenceRequest(BaseModel):
    previous_character_text: str 
    previous_speaker: str   #['trump', 'kamala', 'player']
    current_speaker: str    #['trump', 'kamala']

class InferenceResponse(BaseModel):
    generated_text: str
    anger: float

api_key = ""
#api_key = "MaFKaY7R8TYrOLd56ZDRBcUfatOrebRh"
client = Mistral(api_key=api_key)
trump_yaml = Path(__file__).parents[1] / 'config' / 'trump.yaml'
kamala_yaml = Path(__file__).parents[1] / 'config' / 'trump.yaml'
context_yaml = Path(__file__).parents[1] / 'config' / 'context.yaml'

arbitrary_agent = EmotionAgent(client, model="mistral-large-latest")
    
trump =  AIAgent.from_yaml(trump_yaml, context_yaml, client, arbitrary_agent)
kamala =  AIAgent.from_yaml(kamala_yaml, context_yaml, client, arbitrary_agent)

@app.post("/infer", response_model=InferenceResponse)
async def infer(request: InferenceRequest):
    if request.current_speaker == "trump":
        current_speaker = trump
        opponent = kamala

    elif request.current_speaker == "kamala":
        current_speaker = kamala
        opponent = trump
    
    else:
        raise ValueError()

    input_text = f"{request.previous_speaker} said :{request.previous_character_text}. You respond to {request.previous_speaker}"
    f"You're opponent is in this state: {opponent.emotions}"

    current_speaker.update_emotions(input_text)
    msg = current_speaker.respond(input_text)
    
    return {"generated_text": msg, "anger": current_speaker.emotions['anger']}

# @app.post("/audience", response_model=InferenceResponse)
# async def get(request: InferenceRequest):
#     audience.udpate(trump, kamala)
#     #audience = update(trump, kamala)
#     return audiance.value