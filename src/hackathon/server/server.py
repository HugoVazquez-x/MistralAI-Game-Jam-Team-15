from http.client import HTTPException
from fastapi import FastAPI, Request
from hackathon.server.schemas import AudienceRequest, CardsRequest, CardsResponse, InferenceRequest, InferenceResponse, StartRequest, StartResponse
from hackathon.speech.speech import text_to_speech_file,read_audio_config, read_audio_file
from mistralai import Mistral
from pathlib import Path
from hackathon.agent.character import AIAgent
from hackathon.agent.character import EmotionAgent
from hackathon.agent.engagement import Engagement
from hackathon.agent.presenter import Presenter


# Initialize FastAPI app
app = FastAPI()


class GameEngine:
    def __init__(self,
                 candidate_1_name: str,
                 candidate_2_name: str,
                 api_key: str = "",
                 model_name: str = "mistral-large-latest"):

        self.model_name = model_name
        self.api_key = api_key

        context_yaml = Path(__file__).parents[3] / 'src' / 'config' / 'context.yaml'
        candidate_1_yaml = Path(__file__).parents[3] / 'src' / 'config' / f'{candidate_1_name}.yaml'
        candidate_2_yaml = Path(__file__).parents[3] / 'src' / 'config' / f'{candidate_2_name}.yaml'
        self.audio_yaml = Path(__file__).parents[3] / 'src' / 'config' / 'audio.yaml'
        self.data_folder = Path(__file__).parents[3] / 'src' / 'data' 
        
        self.client = Mistral(api_key=api_key)

        arbitrary_agent = EmotionAgent(self.client, model=self.model_name)
        self.candidate_1 =  AIAgent.from_yaml(candidate_1_yaml, context_yaml, self.client, arbitrary_agent)
        self.candidate_2 =  AIAgent.from_yaml(candidate_2_yaml, context_yaml, self.client, arbitrary_agent)

        self.engagement=Engagement(engagement_0=0)

        # FastAPI application instance
        self.app = FastAPI()

        # Define routes
        self.app.post("/infer", response_model=InferenceResponse)(self.infer)
        self.app.post("/audience", response_model=InferenceResponse)(self.audience)
        self.app.post("/debate-cards", response_model=InferenceResponse)(self.cards)

        # Audio config
        self.audio_config = read_audio_config(self.audio_yaml)
        

@app.post("/start", response_model=StartResponse)
async def start(request: StartRequest):

    app.state.game_engine = GameEngine(candidate_1_name=request.candidate_1_name,
                                       candidate_2_name=request.candidate_2_name)

    return {"status": "Game engine initialized successfully"}


@app.post("/infer", response_model=InferenceResponse)
async def infer(request: InferenceRequest):
    if not hasattr(app.state, "game_engine"):
        raise HTTPException(status_code=400, detail="Game engine not initialized. Call /start first.")
     
    game_engine = app.state.game_engine
    data_folder = game_engine.data_folder

    if request.current_speaker == game_engine.candidate_1.name:
        current_speaker = game_engine.candidate_1

    elif request.current_speaker == game_engine.candidate_2.name:
        current_speaker = game_engine.candidate_2
    else:
        raise ValueError("Candidate name requested do not exist.")
    
    current_audio_config = game_engine.audio_config[current_speaker.name]
    input_text = f"{request.previous_speaker} said :{request.previous_character_text}. You respond to {request.previous_speaker}"
    
    current_speaker.update_emotions(input_text)
    msg = current_speaker.respond(input_text)

    audio_file_path = text_to_speech_file(text=msg, 
                                        voice_id=current_audio_config['voice_id'], 
                                        stability=current_audio_config['stability'], 
                                        similarity=current_audio_config['similarity'], 
                                        style=current_audio_config['style'],
                                        base_path=str(data_folder)
                                        )
    
    audio_signal = read_audio_file(audio_file_path) # base64 

    return {"generated_text": msg, "anger": current_speaker.emotions['anger'], "audio": audio_signal}

@app.post("/engagement", response_model=AudienceRequest)   
async def engagement(self, request: AudienceRequest):

    trump_anger=self.trump.character['angry']
    kamala_anger=self.kamala.character['angry']

    self.engagement.steer_engagement(trump_anger,kamala_anger)
    value=self.engagement.engagement

    
    return {"current_audience_count":value}

@app.post("/debate-cards", response_model=CardsResponse)   
async def cards(self, request: CardsRequest):

    last_text=request.previous_character_text
    previous_speaker=request.previous_speaker
    card=request.chosen_card


    prompt=self.presenter.play_card(card,last_text,previous_speaker)

    return {'presenter_question' : prompt}


async def start(self,):
    pass

async def end(self,):
    pass
    