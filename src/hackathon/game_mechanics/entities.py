
import yaml
from dataclasses import dataclass
from typing import List


@dataclass
class Card:
    title: str
    year: int
    description: str
    source: str
    game_context: str
    change_personnal_context: bool
    information_quality: str

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


