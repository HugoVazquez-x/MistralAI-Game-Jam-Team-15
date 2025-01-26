from pathlib import Path
from hackathon.game_mechanics.pre_game_mechanics import generate_background_personality
from mistralai import Mistral
from hackathon.agent.character import AIAgent
from hackathon.agent.arbitrary import EmotionAgent
from hackathon.agent.engagement import Engagement
from hackathon.agent.presenter import Presenter
import hackathon.game_mechanics.entities as ent
import hackathon.game_mechanics.pre_game_mechanics as pre
import hackathon.agent.arbitrary as ar
import random




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
        
        cards_trump_yaml = Path(__file__).parents[3] /'src' / 'config' / 'cards_trump.yaml'
        cards_kamala_yaml = Path(__file__).parents[3] /'src' / 'config' / 'cards_kamala.yaml'
        cards_neutral_yaml = Path(__file__).parents[3] /'src'/ 'config' / 'cards_neutral.yaml' 
        
        self.client = Mistral(api_key=api_key)

        emotion_agent = EmotionAgent(self.client, model=self.model_name)
        self.candidate_1 =  AIAgent.from_yaml(candidate_1_yaml, context_yaml, self.client, emotion_agent)
        #generate_background_personality(self.candidate_1, self.client)
        self.candidate_2 =  AIAgent.from_yaml(candidate_2_yaml, context_yaml, self.client, emotion_agent)
        #generate_background_personality(self.candidate_2, self.client)

        self.engagement = Engagement()

        self.presenter = Presenter(self.candidate_1.general_context, self.client, model_name)

        card_agent = ar.CardAgent(self.client, model="mistral-large-latest")
        
        self.deck = ent.Deck(cards_trump_yaml, cards_kamala_yaml, cards_neutral_yaml)
        self.deck.sample()
        pre.add_cards_to_personal_context_full_prompt(card_agent, [self.candidate_1, self.candidate_2], self.deck)
    
        self.timestamp = 0
        self.speakers = [self.candidate_1, self.candidate_2, self.presenter]
        self.candidates = [self.candidate_1, self.candidate_2]

        self.current_candidate_idx = 0
        self.current_speaker_idx = 0
        self.current_card_idx = 0

        self.speaker_turns = ["presenter"]
        self.texts = ["Welcome everyone into this presidential debate."]

    def agregate(self):
        pass

    def get_current_speaker(self):
        return self.speakers[self.current_speaker_idx]
    
    def get_previous_speaker_idx(self):
        return (self.current_speaker_idx - 1) % 3

    def get_next_speaker_idx(self):
        return (self.current_speaker_idx + 1) % 3
    
    def get_next_speaker(self):
        return self.speakers[self.get_next_candidate_idx()]
    
    def get_previous_speaker(self):
        return self.speakers[self.get_previous_speaker_idx()]
    
    def change_speaker(self):
        self.current_speaker_idx = self.get_next_speaker_idx()

    def get_previous_text(self):
        self.texts[0]

    def get_next_candidate_idx(self):
        return (self.current_candidate_idx + 1) % 2
    
    def change_candidate(self):
        self.current_candidate_idx = self.get_next_candidate_idx()
    
    def get_next_candidate(self):
        return self.candidates[self.get_next_candidate_idx()]
    
    def get_previous_text(self):
        return self.texts[-1]

    def candidate_speaks(self, verbose = True):
        if self.current_speaker_idx == 2:
            raise ValueError("The speaker is not a candidate")
        self.current_candidate_idx
        speaker = self.get_current_speaker()
        previous_speaker = self.get_previous_speaker()
        next_candidate = self.get_next_candidate()
        previous_text = self.get_previous_text()
        input_text = f"{previous_speaker.name} said :{previous_text}. You have to respond to {next_candidate.name}. Limit to less than 50 words."
        speaker.update_emotions(input_text)
        msg = speaker.respond(input_text)
        self.change_candidate()
        self.change_speaker()
        
        self.texts.append(msg)
        self.speaker_turns.append(speaker.name)
        if verbose:
            print("------------------------")
            print(f"{speaker.name} : {msg}")
        return msg

    def play_card(self, verbose = True):
        if self.current_card_idx < len(self.deck.all_cards):
            card: ent.Card = self.deck.all_cards[self.current_card_idx]
            previous_speaker = self.get_previous_speaker()
            next_speaker = self.get_next_speaker()
            msg = self.presenter.play_card(card, self.get_previous_text(), previous_speaker, next_speaker)
            self.current_card_idx += 1
            self.change_speaker()
            if verbose:
                print("------------------------")
                print(f"{self.presenter.name} : {msg}")
            self.texts.append(msg)
            self.speaker_turns.append(self.presenter.name)
            return msg
        else:
            print("You don't have any card to play")
        
    def play(self, verbose):
        if self.current_speaker_idx == 2:
            return self.play_card(verbose)
        else:
            return self.candidate_speaks(verbose)


if __name__ == "__main__":
    game = GameEngine("trump", "kamala")
    nb_turns = 10
    for i in range(nb_turns):
        game.play(verbose=True)