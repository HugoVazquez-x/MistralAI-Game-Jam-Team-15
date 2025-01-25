import hackathon.agent.character as ch
import hackathon.agent.arbitrary as ar
from typing import Tuple, List

import hackathon.game_mechanics.entities as entities


def generate_background_personality(character: ch.AIAgent, client):
    initial_context = character.general_context

    message = f"Here is the background story of a political personality. Replace simlessly missing values identified by the <TO_FILL> tag with some realistic information. All the facts don't have to be truse but they must make sense with the rest of the personality of the character. Don't make the added text appear in bold. Absolutely avoid filling holes with too controversial ideas: {initial_context}"
    
    chat_response = self.client.chat.complete(
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
    

def add_cards_to_personal_context(card_agent:ar.CardAgent, characters: List[ch.AIAgent], cards:entities.Card):
    for character in characters:
        for card in cards:
            card_agent.add_card_to_personal_context(character, card)


if __name__ == "__main__":
    pass