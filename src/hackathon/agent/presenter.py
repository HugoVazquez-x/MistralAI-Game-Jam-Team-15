import time


class Presenter():
    def __init__(self, general_context, client, model):
        """
        Initialise le présentateur du débat, 
        qui reçoit les promps du joueur pour relancer
        le débat 

        contient des méthodes hard codées pour 
        lancer le débat et le clore dans le cas où 
        un candidat a quitté le débat ou si 
        tout le public est parti
        """

        self.client=client
        self.model=model
        self.general_context=general_context
        self.own_history=[]

    def play_card(self, card, last_sentence_said, 
                  previous_speaker, max_tokens=500):
        """
        card is a dictionnary
        candidates input: contains the last sentences said by
        the candidates

        card:{card topic : attitude} and comes from
        the player if the latter decided to play a card. 
        """

        topic, mood = next(iter(card.items()))

        input_instruction = """You are the moderator
        of the TV debate. You ask a question to the candidates
        about {} with the following attitude {}. You have the last answer from {} 
        to smooth the question and the transition. Keep
        it brief, and fun, it is for a video game. .      
        """.format(topic, mood, previous_speaker)


        messages = [
            {
                "role": "system",
                "content": (
                    f"General context: {self.general_context}\n"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Instructions: {input_instruction}\n"
                    f"Opponent's last sentences: {last_sentence_said}\n"
                    f"Conversation history: {self.own_history}"
                ),
            },
        ]
        # Call the chat completion API
        time.sleep(1)
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,  # Adjust this value as needed
            )
        
        # Extract and return the assistant's response
        out=chat_response.choices[0].message.content
        self.own_history.append({'user' : out})
        return out