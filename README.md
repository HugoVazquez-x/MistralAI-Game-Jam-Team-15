# Make Debates Great Again!

An awesome game built during the Mistral AI Gaming Hackathon **You Don't Control the Character** (@[Photoroom](https://www.photoroom.com/company), 24-26 January 2024)

![Main image](assets/title.png)

Step into the shoes of a TV debate presenter tasked with helping a candidate win the election. Your mission? Polarize the public’s opinion by cleverly angling the debate against your opponent. Chose wisely your questions to stir up emotions, but beware—cross the line and you might push the opponent to leave the stage!

In our game, the player doesn't directly control the candidate seeking to win the debate by polarizing the opinion against his opponent. To reach this goal, the player controls the TV presenter who influences the course of the debates through carefully chosen questions. The presenter’s choices indirectly affect the debaters’ emotions and the public’s opinion. 

Our theme encouraged us to explore new ways of influencing characters and outcomes without directly controlling the characters themselves, which is exactly what our game proposes by steering the environment to make our champion win the game.

---
- [Make Debates Great Again!](#make-debates-great-again)
  - [Instructions](#instructions)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
    - [Project architecture](#project-architecture)
    - [LLM backbones](#llm-backbones)
  - [Contributors](#contributors)
  - [License](#license)

---

## Instructions

Our game is playable on [HuggingFace 🤗](https://huggingface.co/spaces/Mistral-AI-Game-Jam/Team15). 

The debate begins, and the candidates start speaking in turn. The player can choose to play a card from their hand to ask a question or let the debate continue.

The exchanges between the candidates affect their state of mind, particularly their level of anger. The angrier a candidate becomes, the more they polarize the audience against them. If a candidate gets too angry, they may suddenly leave the debate.

Certain cards are designed to provoke one candidate more than the other. They must be played strategically to help the Tycoon's preferred candidate win.

The player wins if they manage to polarize the public opinion against the opponent of the candidate chosen by the Tycoon when time runs out. To do this, they must anger the opponent. However, they must be careful not to anger them too much, as if any candidate leaves the debate, the player loses.

The player wins if, at the end of the time limit, they have succeeded in polarizing the opinion against the opponent of the Tycoon's chosen candidate, and no candidate has left the debate.

When it’s your turn, use the `Right Arrow` to navigate through the cards and press the `Spacebar` to play a card.

## Features

* LLM-based characters
  * Dynamic mood
  * Dynamic updating of the short term memory of the character as the Debate goes on
* Synthetic voices to make them more lovely for the candidates using Speech-to-Voice models
* The playable cards can be more or less targeted toward one of the opponents

## Tech Stack

### Project architecture

The server project is hosted on a Scaleway server. This server communicates with a Unity client that controls the visual aspects of the Game and the interactions with the player. The Server calls the Mistral API to generate the prompts of the Candidates and of the Presenter. We have an additional Referral LLM that regularily summarizes the debate and sends this debate to the memory of the Candidates and that evaluates the current mood and anger level of the opponents. 

We have an additonal layer that generate speech from the prompts and returns the `mp3` files to the Unity Client in order to render the debate as speeches. 

### LLM backbones

Our Opponents are embodied by Mistral AI LLM models. We prompt those models with a context, the personality and the mood of the opponents. In each prompt, we hard-coded a constraint aiming to prevent the generation of hateful speech.

We also used Text-to-Speech models to generate Audio files from the texts generated by the LLMs.

### LLM agents architecture

To control the debate and make the characters speak naturally and be coherent with the debate subjects, we add some specific context to the different characters. There is static and dynamic context.

The static context $S$ is composed by :
- The general context of the debate;
- The personal context of the character : how he's feeling right now and how some specific subjects could impact himself (cases that could hurt him during the debate);
- His goal during the debate;
- His character : how he behave in life;
- 
The dynamic context $D$ is composed by :
- His memory of what happen before during the debate;
- His emotions, in particular his anger : which drives the dynamic of the game;
- His attitudes, how the character is acting right now;

Firstly, the static context is enhanced with agregation of imaginatory statements and references to the cards that will be played by the player. 

Then, We use prompting to updates each dynamic context based on the last message $M_k$, the static component $S$ and the last context $D_n$ :

$$
D_{n+1} = F(S, M_k, D_n)
$$

Where F is caracterized by the LLM model used and is modulated by the intention of the game. The intention should be to stabilized the debate to a calm behaviour are, at the contrary to make the debate go **out of control**.

## Contributors

- (Gabriel Vidal)[https://github.com/GabrielVidal1]
- (Hugo Vazquez)[https://github.com/HugoVazquez-x]
- (Raphaël Jean)[https://github.com/RaphJean]
- (Louis Martnez)[https://github.com/lmartinez2001]
- (Yongkang Zou)[https://github.com/inin-zou]
- (Gabriel Kasmi)[https://github.com/gabrielkasmi]


## License

