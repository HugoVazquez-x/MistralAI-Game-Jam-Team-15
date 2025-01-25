import hackathon.agent.character as ch
import hackathon.agent.arbitrary as ar
from typing import Tuple, List

import hackathon.game_mechanics.entities as entities


def sample_deck(deck:entities.Deck):
    return deck.sample()

def add_cards_to_personal_context(card_agent:ar.CardAgent, characters: Tuple[ch.AIAgent, ch.AIAgent], deck:entities.Deck):
    for idx, character in enumerate(characters):
        print("------trump enrischment------")
        if idx == 0:
            for card in deck.cards_1:
                card_agent.add_card_to_personal_context(character, card)
        else:
            for card in deck.cards_2:
                card_agent.add_card_to_personal_context(character, card)

def add_cards_to_personal_context_full_prompt(card_agent:ar.CardAgent, characters: Tuple[ch.AIAgent, ch.AIAgent], deck:entities.Deck):
    for idx, character in enumerate(characters):
        print("------trump enrischment------")
        if idx == 0:
            card_agent.add_cards_to_personal_context(character, deck.cards_1)
        else:
            card_agent.add_cards_to_personal_context(character, deck.cards_2)

if __name__ == "__main__":
    pass