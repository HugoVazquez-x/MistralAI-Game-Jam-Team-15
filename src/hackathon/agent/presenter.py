

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

    def launch_debate(self,candidate_name_1, candidate_name_2,max_tokens=500):
        """
        returns a prompt that launches de debate and gives 
        the floor to the first candidate candidate_name_1
        """

        instructions="""
            You are the presenter of a TV debate between two presidential candidates
            between {} and {}. You launch the debate given the context and give the floor 
            to candidate {}. Keep it brief, and fun, it is for a video game
        """.format(candidate_name_1, candidate_name_2, candidate_name_1)

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
                    f"Instructions: {instructions}\n"
                ),
            },
        ]

                # Call the chat completion API
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,  # Adjust this value as needed
            )
        
        # Extract and return the assistant's response
        intro=chat_response.choices[0].message.content
        self.own_history.append({"user": intro})
        return chat_response.choices[0].message.content
    

    def play_card(self, card, last_sentence_said, 
                  previous_speaker, max_tokens=500):
        """
        card is a dictionnary
        candidates input: contains the last sentences said by
        the candidates

        card:{card_type : sentiment} and comes from
        the player if the latter decided to play a card. 
        """

        topic, mood = next(iter(card.items()))

        input_instruction = """You are the moderator
        of the TV debate. You ask a question to the candidates
        about {} with a tone that is {}. You have the last answer from {} 
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
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,  # Adjust this value as needed
            )
        
        # Extract and return the assistant's response
        out=chat_response.choices[0].message.content
        self.own_history.append({'user' : out})
        return out
        

    

    def exit(self, audimat, candidates_input, max_tokens=500):
        """
        generate the exit prompt when the debates ends
        """

        winner='Trump' if audimat > 0 else "Harris"

        input_instructions="""
        You are the presenter of a TV show and you want to close a debate between
        two contenters. The debate ended as the time arrived to its end. You declare based 
        on the engagement of the audience that the winner of the debate is {}. 
        Keep it brief, and fun, it is for a video game
        """.format(winner)

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
                    f"Instructions: {input_instructions}\n"
                    f"Opponent's last sentences: {candidates_input}\n"
                    f"Conversation history: {self.own_history}"
                ),
            },
        ]

                # Call the chat completion API
        chat_response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,  # Adjust this value as needed
            )

        # Extract and return the assistant's response
        out=chat_response.choices[0].message.content
        self.own_history.append({'user' : out})
        return out
