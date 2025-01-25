import hackathon.agent.character as ch
import hackathon.agent.arbitrary as ar
from typing import Tuple, List
import time

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
    initial_context = f"I am {character.name}. And here is my personal context :" + character.personal_context + f"The response should be shorter than 150 words."
    instructions = (
        f"Here is the background story of a political personality. "
        f"Seamlessly fill in missing information marked with the <TO_FILL> tag using realistic and coherent details. "
        f"The added content doesn't need to be completely factual but must align with the character's personality. "
        f"Avoid using bold formatting and steer clear of overly controversial ideas: {initial_context}."
        f"The response should be shorter than 150 words."
    )    
    messages = [
             {
                "role": "system",
                "content": (
                    f"Initial context: {initial_context}\n"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Instructions: {instructions}\n"
                ),
            },
        ]
    chat_response = client.chat.complete(
        model=character.model,
        messages=messages
    )
    # ------------------------------------------------
    character.personal_context = chat_response.choices[0].message.content
    time.sleep(1)
    

def add_cards_to_personal_context_full_prompt(card_agent:ar.CardAgent, characters: Tuple[ch.AIAgent, ch.AIAgent], deck:entities.Deck):
    for idx, character in enumerate(characters):
        if idx == 0:
            card_agent.add_cards_to_personal_context(character, deck.cards_1)
        else:
            card_agent.add_cards_to_personal_context(character, deck.cards_2)

if __name__ == "__main__":
    pass