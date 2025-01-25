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

def generate_background_personality(character: ch.AIAgent, client):
    initial_context = character.general_context

    message = f"Here is the background story of a political personality. Replace simlessly missing values identified by the <TO_FILL> tag with some realistic information. All the facts don't have to be truse but they must make sense with the rest of the personality of the character. Don't make the added text appear in bold. Absolutely avoid filling holes with too controversial ideas: {initial_context}"
    
    chat_response = client.chat.complete(
        model=character.model,
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )
    # ------------------------------------------------
    character.general_context = chat_response.choices[0].message.content
    

def add_cards_to_personal_context_full_prompt(card_agent:ar.CardAgent, characters: Tuple[ch.AIAgent, ch.AIAgent], deck:entities.Deck):
    for idx, character in enumerate(characters):
        print("------trump enrischment------")
        if idx == 0:
            card_agent.add_cards_to_personal_context(character, deck.cards_1)
        else:
            card_agent.add_cards_to_personal_context(character, deck.cards_2)

if __name__ == "__main__":
    pass