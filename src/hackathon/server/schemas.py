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

class AudienceRequest(BaseModel): # ce dont j'ai besoin comme info pour l'audience
    pass

class AudienceResponse(BaseModel): # envoie un float
    current_audience_count: int
    pass

class CardsRequest(BaseModel):
    pass

class CardsResponse(BaseModel):
    pass

class StartRequest(BaseModel):
    """
    Available name for now: ['trump', 'kamala']
    """
    candidate_1_name: str 
    candidate_2_name: str   

class StartResponse(BaseModel):
    status: str