import hackathon.agent.arbitrary as ar
import hackathon.agent.character as ch
import hackathon.game_mechanics.entities as ent
import hackathon.game_mechanics.pre_game_mechanics as pre
from pathlib import Path
from mistralai import Mistral
import yaml
from hackathon.game_mechanics.pre_game_mechanics import generate_background_personality 


def read_yaml(file_path):
    """
    Reads a YAML file and returns its contents as a Python object.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict or list: The parsed YAML structure (dictionary or list).
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def card_enrichment():
    api_key = ""
    client = Mistral(api_key=api_key)
    print(Path(__file__))

    trump_yaml = Path(__file__).parents[2] / 'config' / 'trump.yaml'
    kamala_yaml = Path(__file__).parents[2] / 'config' / 'trump.yaml'
    context_yaml = Path(__file__).parents[2] / 'config' / 'context.yaml'
    cards_trump_yaml = Path(__file__).parents[2] / 'config' / 'cards_trump_english.yaml'
    cards_kamala_yaml = Path(__file__).parents[2] / 'config' / 'cards_kamala.yaml'
    cards_neutral_yaml = Path(__file__).parents[2] / 'config' / 'cards_neutrals.yaml'

    deck = ent.Deck(cards_trump_yaml, cards_kamala_yaml, cards_neutral_yaml)


    emotional_agent = ar.EmotionAgent(client, model="mistral-large-latest")
    card_agent = ar.CardAgent(client, model="mistral-large-latest")
    

    trump =  ch.AIAgent.from_yaml(trump_yaml, context_yaml, client, emotional_agent)
    generate_background_personality(trump, client)
    kamala =  ch.AIAgent.from_yaml(kamala_yaml, context_yaml, client, emotional_agent)
    generate_background_personality(kamala, client)
    
    print(trump.personal_context)
    pre.add_cards_to_personal_context_full_prompt(card_agent, [trump, kamala], deck)
    print("-------------")
    print(trump.personal_context)


def deck_test():
    api_key = ""
    client = Mistral(api_key=api_key)
    print(Path(__file__))

    trump_yaml = Path(__file__).parents[2] / 'config' / 'trump.yaml'
    kamala_yaml = Path(__file__).parents[2] / 'config' / 'trump.yaml'
    context_yaml = Path(__file__).parents[2] / 'config' / 'context.yaml'
    cards_trump_yaml = Path(__file__).parents[2] / 'config' / 'cards_trump.yaml'
    cards_kamala_yaml = Path(__file__).parents[2] / 'config' / 'cards_kamala.yaml'
    cards_neutral_yaml = Path(__file__).parents[2] / 'config' / 'cards_neutral.yaml'

    deck = ent.Deck(cards_trump_yaml, cards_kamala_yaml, cards_neutral_yaml)
    deck.sample()
    print(f'{deck.to_json_all()=}')


if __name__ == "__main__":
    deck_test()
    #card_enrichment()