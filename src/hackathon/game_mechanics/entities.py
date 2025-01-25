
import yaml
from dataclasses import dataclass
from typing import List, Dict, Union


@dataclass
class Card:
    title: str
    description: str
    source: str
    game_context: str
    change_personal_context: bool
    information_quality: str
    year:Union[None, int] = None

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


