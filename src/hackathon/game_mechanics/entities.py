
import yaml
from dataclasses import dataclass
from typing import List, Dict, Union
from pathlib import Path
from hackathon.utils import util
from dataclasses import asdict
import random
import json

class Deck:
    def __init__(self, data_path_char_1:Path, data_path_char_2:Path, 
                 data_path_neutral:Path):
        self.cards_1 = self.add_cards_from_path(data_path_char_1, -1)
        self.cards_2 = self.add_cards_from_path(data_path_char_2, 1)
        self.cards_neutral = self.add_cards_from_path(data_path_neutral, 0)
        self.cards_samples = None

    def add_cards_from_path(self, data_path_char:Path, side:int):
        cards = util.read_yaml(data_path_char)
        cards_ = []
        for card_dict in cards:
            card_dict.update({"side":side})
            cards_.append(Card.from_dict(card_dict))
        return cards_

    def shuffle_all(self):
        random.shuffle(self.all_cards)

    def sample(self):
        n_1 = min(len(self.cards_1), random.randint(5, 10))
        self.cards_1 = random.sample(self.cards_1, n_1)

        n_2 = min(len(self.cards_2), random.randint(5, 10))
        self.cards_2 = random.sample(self.cards_2, n_2)

        n_neutral = min(len(self.cards_neutral), random.randint(5, 10))
        self.cards_neutral = random.sample(self.cards_neutral, n_neutral)

        self.all_cards = self.cards_1 + self.cards_2 + self.cards_neutral
        self.shuffle_all()

    def to_list(self): 
        return [asdict(card) for card in self.all_cards]


@dataclass
class Card:
    title: str
    description: str
    source: str
    game_context: str
    change_personal_context: bool
    information_intensity: str
    year:Union[None, int] = None
    side:Union[None, int] = None 

    @classmethod
    def from_yaml(cls, file_path: str) -> List["Card"]:
        """Reads a YAML file and returns a list of Card instances."""
        with open(file_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        # Ensure `data` is a list of dictionaries
        if not isinstance(data, list):
            raise ValueError("YAML content is not a list of items.")

        return [cls(**item) for item in data]
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Card":
        return cls(**data)

@dataclass
class Environment:
    description:str

@dataclass
class Game_history:
    conversation: List[str]
    sentiments_history: List[dict]



def read_yaml_to_dataclass(file_path: str) -> List[Card]:
    # Open and parse the YAML file
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    # Convert each dictionary entry into a Card dataclass
    return [Card(**item) for item in data]


