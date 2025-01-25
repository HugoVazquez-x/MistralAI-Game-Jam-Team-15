import json
import re
from mistralai import Mistral
import time
import hackathon.game_mechanics.entities as entities
from typing import Tuple, List
import hackathon.agent.character as ch


class Agent:
    def __init__(self, client: Mistral, model: str):
        self.client = client
        self.model = model


class CardAgent(Agent):
    def add_card_to_personal_context(self, character:ch.AIAgent, card:entities.Card):
        if card.change_personnal_context:
            system_prompt = (
                "You are a conversationnal game update engine "
                "Given the two AI characters traits, and his current personnal context, "
                "you will propose a new personnal personal context"
            )
            user_prompt = f"""
            Character: {character}
            Current personal context: {character.personal_context}
            The context to be added to the personnal context : 
                Fact description : {card.description}
                Description of the effect on the player : {card.game_context}
            """
            user_prompt += f"""
                Instructions:
                    Gives a new synthetic personal context to take into account this new description.
                """
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            #print(f"{messages=}")

            response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                max_tokens=200
            )

            time.sleep(1)

            raw_text = response.choices[0].message.content.strip()
            character.personal_context = raw_text

class EmotionAgent:
    """
    Uses a LLM (Mistral) to handle:
     - update_emotions
     - update_attitude
     - create_memory_context
    Each method returns strictly valid JSON, parsed into Python dicts.
    """

    def __init__(self, client: Mistral, model: str):
        self.client = client
        self.model = model

    def update_emotions(self, character):
        """
        Calls the LLM to produce new emotion values in valid JSON.
        Each emotion in [0.0, 1.0].
        """

        system_prompt = (
            "You are an emotion update engine. "
            "Given the AI's character traits, current emotions, general context, and context memory, "
            "you will propose updated emotion  and attitudes values. The output must be strictly valid JSON, "
            "Give a particular  attention to anger value."
        )

        user_prompt = f"""
        Character: {character}
        Current Emotions: {character.emotions}
        Current Attitudes: {character.attitudes}
        Conversation History: {character.context_memory}

        Instructions:
        1. Analyze the information provided above.
        2. Propose new values for emotions and attitudes in valid JSON format.

        JSON structure attributes must be respected:
        {{
            "emotions": {character.emotions},
            "attitudes": {character.attitudes}
        }}

        Requirements:
        - All numeric values must be floats in the range [0.0, 1.0].
        - Text values should be descriptive and context-appropriate.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        #print(f"{messages=}")

        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            max_tokens=200
        )

        time.sleep(1)

        raw_text = response.choices[0].message.content.strip()
        #print(f'{raw_text=}')
        cleaned_response = re.sub(r"```(json)?", "", raw_text).strip()

        try:
            updated_emotions = json.loads(cleaned_response)
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON for emotions. Using old emotions.\nResponse: {cleaned_response}")
            return updated_emotions

        # Clamp to [0.0, 1.0]
        final_emotions = {}
        final_attitudes = {}

        for emotion, val in updated_emotions['emotions'].items():
            if isinstance(val, (int, float)):
                final_emotions[emotion] = max(0.0, min(1.0, float(val)))
            else:
                # Fallback if invalid
                final_attitudes[emotion] = updated_emotions.get(emotion, 0.5)
        
        for attitude, val in updated_emotions['attitudes'].items():
            if attitude == 'patience':
                final_attitudes['patience'] = 0
            else:    
                final_attitudes[attitude] = val
        
        return final_emotions, final_attitudes