from typing import Dict, List
from pydantic import BaseModel

# Define the request and response schema
class InferenceRequest(BaseModel):
    previous_character_text: str 
    previous_speaker: str   #['trump', 'kamala', 'player']
    current_speaker: str    #['trump', 'kamala']

class InferenceResponse(BaseModel):
    generated_text: str
    anger: float
    audio: str

class EngagementRequest(BaseModel): 
    pass

class EngagementResponse(BaseModel): 
    engagement: int
    

class CardsVoiceRequest(BaseModel):
    previous_character_text:str
    previous_speaker:str
    chosen_card:dict

class CardsVoiceResponse(BaseModel):
    presenter_question:str

class CardsVoiceRequest(BaseModel):
    previous_character_text:str
    previous_speaker:str
    chosen_card:dict

class CardsResponse(BaseModel):
    cards: List[Dict]

class CardsRequest(BaseModel):
    pass

class StartRequest(BaseModel):
    """
    Available name for now: ['trump', 'kamala']
    """
    candidate_1_name: str 
    candidate_2_name: str   

class StartResponse(BaseModel):
    status: str
