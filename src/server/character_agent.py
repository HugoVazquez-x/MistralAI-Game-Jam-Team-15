from typing import Union
from mistralai import Mistral
import yaml
from pathlib import Path
import re
import json
import time
from arbitrary_agent import EmotionAgent


class AIAgent:
    def __init__(
        self,
        name,
        character,
        emotions,
        attitudes,
        goal,
        general_context,
        client,
        arbitrary_agent=None
    ):
        """
        Initialise l'agent IA avec ses attributs de base.

        :param name: Nom de l'agent
        :param character: dict décrivant la personnalité de l'IA
        :param emotions: dict des émotions actuelles de l'IA
        :param goal: Objectif principal de l'IA
        :param general_context: Contexte général (ex: sujet du débat)
        :param arbitrary_agent: Objet gérant la logique de mise à jour des émotions
        """
        self.client = client
        self.model = "mistral-large-latest"

        self.name = name
        self.character = character
        self.emotions = emotions
        self.attitudes = attitudes
        self.goal = goal

        self.general_context = general_context
        self.arbitrary_agent = arbitrary_agent

        self.context_memory = ""
    
    @classmethod
    def from_yaml(cls, character_yaml: Union[Path, str], general_context_yaml:  Union[Path, str], client, arbitrary_agent: EmotionAgent=None):
        """
        Initialize an object using YAML content.
        """
        character_data = cls.parse_yaml_to_dict(str(character_yaml))
        context_data = cls.parse_yaml_to_dict(str(general_context_yaml))
        if character_data:
            return cls(
                client=client,
                name=character_data.get("name"),
                character=character_data.get("character"),
                emotions=character_data.get("emotions"),
                attitudes=character_data.get("attitudes"),
                goal=character_data.get("goal"),
                general_context = context_data.get("general_context"),
                arbitrary_agent = arbitrary_agent

            )
        else:
            raise ValueError("Failed to parse YAML content.")
    
    @staticmethod
    def parse_yaml_to_dict(yaml_content):
        """
        Parse YAML content into a Python dictionary.
        """
        try:
            with open(yaml_content, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: The file '{yaml_content}' was not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None
    
    def __repr__(self):
        return (f"TrumpProfile(\n"
                f"  general_context={self.general_context},\n"
                f"  {self.name}_character={self.character},\n"
                f"  {self.name}_emotions={self.emotions},\n"
                f"  {self.name}_attitudes={self.attitudes},\n"
                f"  {self.name}_goal='{self.goal}'\n"
                f")")
    
    def respond(self, input_text):
        """
        Génère une réponse basée sur le contexte fourni.

        :param input_text: Texte reçu
        :param opponent_state: État actuel de l'adversaire (dict)
        :return: Réponse de l'IA
        """
        
        response = self._generate_response(
            instructions=input_text,
            environment_description="N/A"
        )
        return response

    def update_emotions(self, input_text):
        """
        Met à jour les émotions en fonction d'une analyse via l'arbitrary_agent (LLM).
        """
        self.context_memory = self.create_memory_context(input_text)

        if self.arbitrary_agent is not None:
            self.emotions, self.attitudes = self.arbitrary_agent.update_emotions(character=self)
        else:
            print("No arbitrary agent provided. Emotions remain unchanged.")

    def _generate_response(self, instructions, environment_description, max_tokens=None):
        messages = [
            {
                "role": "system",
                "content": (
                    f"General context: {self.general_context}\n"
                    f"Character: {self.character}\n"
                    f"Goal: {self.goal}\n"
                    f"Emotions: {self.emotions}\n"
                    f"Attitudes: {self.attitudes}\n"
                    f"Environment: {environment_description}\n"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Instructions: {instructions}\n"
                    f"Conversation history: {self.context_memory}"
                ),
            },
        ]
        # ------------------------------
        # Hypothetical call to LLM API
        # ------------------------------
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens if max_tokens else None
        )
        # ------------------------------------------------
        return chat_response.choices[0].message.content

    def create_memory_context(
        self,
        current_input,
        additional_instructions="Summarize recent key points and emotional undertones."
    ):
        """
        Calls LLM to produce a memory context (summary, emotional tone, etc.) in valid JSON.
        """

        system_prompt = (
            "You are a memory transformation engine. "
            "Based on the agent's current input, current context memory, character personality, and current emotions, "
            "produce a concise memory context in valid JSON."
        )

        user_prompt = f"""
                        Character: {self.name}
                        Emotions: {self.emotions}
                        Current answer he get: {current_input}
                        Context memory: {self.context_memory}

                        Task:
                        - {additional_instructions}
                        - Return structured memory context in valid JSON. Example:
                        {{
                            "summary": "...",
                            "emotionalTone": "..."
                        }}
                        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            max_tokens=300
        )
        time.sleep(1)

        raw_text = response.choices[0].message.content.strip()
        cleaned_response = re.sub(r"```(json)?", "", raw_text).strip()

        try:
            memory_context = json.loads(cleaned_response)
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON for memory context. Using fallback.\nResponse: {cleaned_response}")
            memory_context = {
                "summary": "No valid summary",
                "emotionalTone": "neutral"
            }

        return memory_context

    
    
if __name__ == "__main__":
    
    api_key = ""
    client = Mistral(api_key=api_key)

    trump_yaml = Path(__file__).parents[1] / 'config' / 'trump.yaml'
    kamala_yaml = Path(__file__).parents[1] / 'config' / 'trump.yaml'
    context_yaml = Path(__file__).parents[1] / 'config' / 'context.yaml'

    arbitrary_agent = EmotionAgent(client, model="mistral-large-latest")
    
    trump =  AIAgent.from_yaml(trump_yaml, context_yaml, client, arbitrary_agent)
    kamala =  AIAgent.from_yaml(kamala_yaml, context_yaml, client, arbitrary_agent)

    # print(f'{trump.emotions=}')
    # print(f'{trump.attitudes=}')
    import time

    txt_list = ["trump is an asshole", "Sorry mr trump, youre very strong, powerful and intelligent", "Trump, you know I like your wife. Even if you could be a little bit rude, I know you have a great heart.", "Actualy youre politic is not so bad", "in fact the economical situation of the country improve during your presidence"]
    for inpt in txt_list:
        previous_speaker = 'kamala'
        #previous_character_text = "trump is an asshole"
        previous_character_text = inpt
        opponent = kamala

        print()
        print("__________BEFORE UPDATE__________")

        input = f"{previous_speaker} said to you:{previous_character_text}. It's your turn to respond to {previous_speaker}"
        
        print(f'{input=}')
        trump.update_emotions(input)
        print()
        print("__________AFTER UPDATE__________")
        print(f"{trump.emotions['anger']=}")
        print(f'{trump.context_memory=}')
        print(f"{trump.attitudes=}")
        print()
        time.sleep(1)
    
    #print(trump.respond(input_text, opponent_state))

