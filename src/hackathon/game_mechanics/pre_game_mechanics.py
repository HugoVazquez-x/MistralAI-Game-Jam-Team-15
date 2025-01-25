import hackathon.agent.character as ch
import hackathon.agent.arbitrary as ar
from typing import Tuple, List

import hackathon.game_mechanics.entities as entities




def add_cards_to_personal_context(card_agent:ar.CardAgent, characters: List[ch.AIAgent], cards:entities.Card):
    for character in characters:
        for card in cards:
            card_agent.add_card_to_personal_context(character, card)


if __name__ == "__main__":
    pass