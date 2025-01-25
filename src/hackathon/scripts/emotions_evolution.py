import hackathon.agent.arbitrary as ar
import hackathon.agent.character as ch
from pathlib import Path
from mistralai import Mistral



def anger_evolution():
    api_key = ""
    client = Mistral(api_key=api_key)
    print(Path(__file__))

    trump_yaml = Path(__file__).parents[2] / 'config' / 'trump.yaml'
    kamala_yaml = Path(__file__).parents[2] / 'config' / 'trump.yaml'
    context_yaml = Path(__file__).parents[2] / 'config' / 'context.yaml'

    arbitrary_agent = ar.EmotionAgent(client, model="mistral-large-latest")
    
    trump =  ch.AIAgent.from_yaml(trump_yaml, context_yaml, client, arbitrary_agent)
    kamala =  ch.AIAgent.from_yaml(kamala_yaml, context_yaml, client, arbitrary_agent)

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



if __name__ == "__main__":
    anger_evolution()