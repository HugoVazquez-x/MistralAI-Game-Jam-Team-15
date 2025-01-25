from http.client import HTTPException
from fastapi import FastAPI, Request
from hackathon.server.schemas import CardsRequest, CardsResponse, CardsVoiceRequest, CardsVoiceResponse, EngagementRequest, EngagementResponse, InferenceRequest, InferenceResponse, StartRequest, StartResponse
from hackathon.speech.speech import text_to_speech_file,read_audio_config, read_audio_file
from mistralai import Mistral
from pathlib import Path
from hackathon.agent.character import AIAgent
from hackathon.agent.character import EmotionAgent
from hackathon.agent.engagement import Engagement
from hackathon.agent.presenter import Presenter
import os


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

        candidate_1_yaml = Path(__file__).parents[3] / 'src' / 'config' / f'{candidate_1_name}.yaml'
        candidate_2_yaml = Path(__file__).parents[3] / 'src' / 'config' / f'{candidate_2_name}.yaml'
        self.audio_yaml = Path(__file__).parents[3] / 'src' / 'config' / 'audio.yaml'
        self.data_folder = Path(__file__).parents[3] / 'src' / 'data' 
        context_yaml = Path(__file__).parents[3] / 'src' / 'config' / 'context.yaml'
        
        self.client = Mistral(api_key=api_key)

        arbitrary_agent = EmotionAgent(self.client, model=self.model_name)
        self.candidate_1 =  AIAgent.from_yaml(candidate_1_yaml, context_yaml, self.client, arbitrary_agent)
        self.candidate_2 =  AIAgent.from_yaml(candidate_2_yaml, context_yaml, self.client, arbitrary_agent)

        self.engagement = Engagement()

        self.presenter = Presenter(self.candidate_1.general_context, self.client, model_name)

        self.audio_config = read_audio_config(self.audio_yaml)
        self.timestamp = 0
        

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
    game_engine.timestamp += 1

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
    os.remove(audio_file_path)

    return {"generated_text": msg, "anger": current_speaker.emotions['anger'], "audio": audio_signal}


@app.get("/engagement")
async def engagement():
    
    if not hasattr(app.state, "game_engine"):
        raise HTTPException(status_code=400, detail="Game engine not initialized. Call /start first.")    
    
    game_engine = app.state.game_engine

    if game_engine.timestamp > game_engine.engagement.timestamp:
        candidate_1_anger = game_engine.candidate_1.emotions['anger']
        candidate_2_anger = game_engine.candidate_2.emotions['anger']

        game_engine.engagement.update(candidate_1_anger, candidate_2_anger)
        value = game_engine.engagement.current_value
    else:
        value = game_engine.engagement.current_value

    return {'engagement': value}


@app.post("/card-voice", response_model=CardsVoiceResponse)   
async def cards(request: CardsVoiceRequest):
    """
    WARNING CARDS HAVE AN IMPACT HERE

    """
    if not hasattr(app.state, "game_engine"):
        raise HTTPException(status_code=400, detail="Game engine not initialized. Call /start first.")
     
    game_engine = app.state.game_engine
    game_engine.timestamp += 1
    presenter = game_engine.presenter

    last_text = request.previous_character_text
    previous_speaker_name = request.previous_speaker


    if previous_speaker_name == game_engine.candidate_1.name:
        next_speaker = game_engine.candidate_2
        last_speaker = game_engine.candidate_1

    elif previous_speaker_name == game_engine.candidate_2.name:
        next_speaker = game_engine.candidate_2
        last_speaker = game_engine.candidate_1
    
    card = request.chosen_card #WARNING!!!! CHECK THE FORMAT

    current_audio_config = game_engine.audio_config['chairman']

    msg = presenter.play_card(card, last_text, last_speaker, next_speaker)
    
    data_folder = game_engine.data_folder
    
    audio_file_path = text_to_speech_file(text=msg,
                                          voice_id=current_audio_config['voice_id'], 
                                          stability=current_audio_config['stability'],
                                          similarity=current_audio_config['similarity'], 
                                          style=current_audio_config['style'],
                                          base_path=str(data_folder)
                                          )
    
    audio_signal = read_audio_file(audio_file_path) # base64 
    
    os.remove(audio_file_path)

    return {'presenter_question' : msg, "audio": audio_signal}


@app.post("/cards-request", response_model=CardsResponse)   
async def cards(request: CardsRequest):

    if not hasattr(app.state, "game_engine"):
        raise HTTPException(status_code=400, detail="Game engine not initialized. Call /start first.")
     
    game_engine = app.state.game_engine

    cards = game_engine.deck.get_deck()

    return cards   