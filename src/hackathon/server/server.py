from http.client import HTTPException
from fastapi import FastAPI, Request
from hackathon.server.schemas import AudienceRequest, CardsRequest, InferenceRequest, InferenceResponse
from mistralai import Mistral
from pathlib import Path
from hackathon.agent.character import AIAgent
from hackathon.agent.character import EmotionAgent

# Initialize FastAPI app
app = FastAPI()


class Server:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Mistral(api_key=api_key)
        
        # Define paths to YAML configurations
        self.trump_yaml = Path(__file__).parents[1] / 'config' / 'trump.yaml'
        self.kamala_yaml = Path(__file__).parents[1] / 'config' / 'trump.yaml'
        self.context_yaml = Path(__file__).parents[1] / 'config' / 'context.yaml'

        # Initialize EmotionAgent and AI Agents
        self.arbitrary_agent = EmotionAgent(self.client, model="mistral-large-latest")
        self.trump = AIAgent.from_yaml(self.trump_yaml, self.context_yaml, self.client, self.arbitrary_agent)
        self.kamala = AIAgent.from_yaml(self.kamala_yaml, self.context_yaml, self.client, self.arbitrary_agent)

        # FastAPI application instance
        self.app = FastAPI()

        # Define routes
        self.app.post("/infer", response_model=InferenceResponse)(self.infer)
        self.app.post("/audience", response_model=InferenceResponse)(self.audience)
        self.app.post("/debate-cards", response_model=InferenceResponse)(self.cards)

    
    async def infer(self, request: InferenceRequest):
        """Endpoint to handle inference requests."""
        if request.current_speaker == "trump":
            current_speaker = self.trump
            opponent = self.kamala
        elif request.current_speaker == "kamala":
            current_speaker = self.kamala
            opponent = self.trump
        else:
            raise HTTPException(status_code=400, detail="Invalid current speaker.")

        input_text = (
            f"{request.previous_speaker} said: {request.previous_character_text}. You respond to {request.previous_speaker}. "
            f"Your opponent is in this state: {opponent.emotions}"
        )

        current_speaker.update_emotions(input_text)
        msg = current_speaker.respond(input_text)

        return {"generated_text": msg, "anger": current_speaker.emotions['anger']}
    
    async def audience(self, request: AudienceRequest):
        pass


    async def cards(self, request: CardsRequest):
        pass