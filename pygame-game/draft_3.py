import gym
import numpy as np
import random
from collections import deque

import torch
import torch.nn as nn
import torch.optim as optim

# =========================
# 1) Définition de l'environnement Gym
# =========================

class GridEnv(gym.Env):
    """
    Environnement simple :
      - Grille 4x5 (4 lignes, 5 colonnes).
      - 'o' = case libre, 'x' = mur, 'g' = goal.
      - L'agent démarre en (row=0, col=0).
      - Actions (0=UP, 1=RIGHT, 2=DOWN, 3=LEFT).
    """
    def __init__(self):
        super(GridEnv, self).__init__()
        
        self.grid = [
            "ooooo",
            "oxxoo",
            "oxxoo",
            "oooog"
        ]
        self.n_rows = len(self.grid)      # 4
        self.n_cols = len(self.grid[0])   # 5

        # Gym: définition espaces d'actions et d'observations
        # Observation: la position (row, col) -> on peut coder en 2 entiers
        # ou on peut "aplatir" en un seul entier row * n_cols + col
        # Action: 4 (UP, RIGHT, DOWN, LEFT)
        self.action_space = gym.spaces.Discrete(4)
        
        # Observation space : on encode la position dans [0, n_rows*n_cols-1]
        self.observation_space = gym.spaces.Discrete(self.n_rows * self.n_cols)

        # Position de départ
        self.start_row = 0
        self.start_col = 0

        # État interne (row, col)
        self.state = (self.start_row, self.start_col)

        # Nombre max de pas par épisode (pour éviter de tourner en rond)
        self.max_steps = 50
        self.current_step = 0

    def reset(self):
        """
        Réinitialise l'environnement et renvoie l'observation initiale.
        """
        self.state = (self.start_row, self.start_col)
        self.current_step = 0
        return self._to_obs(self.state)

    def step(self, action):
        """
        Exécute l'action (UP, RIGHT, DOWN, LEFT),
        renvoie (obs, reward, done, info).
        """
        self.current_step += 1

        row, col = self.state

        if action == 0:   # UP
            new_row, new_col = row - 1, col
        elif action == 1: # RIGHT
            new_row, new_col = row, col + 1
        elif action == 2: # DOWN
            new_row, new_col = row + 1, col
        elif action == 3: # LEFT
            new_row, new_col = row, col - 1
        else:
            new_row, new_col = row, col

        # Vérifie si on sort de la grille ou si on tombe sur un mur
        if (new_row < 0 or new_row >= self.n_rows or
            new_col < 0 or new_col >= self.n_cols or
            self.grid[new_row][new_col] == 'x'):
            # Coup invalide => fin d'épisode, grosse punition
            reward = -1.0
            done = True
            new_row, new_col = row, col  # pas forcément utile vu done = True
        else:
            # Déplacement valide
            # Savoir si on atteint l'objectif
            if self.grid[new_row][new_col] == 'g':
                reward = 10.0
                done = True
            else:
                reward = -0.1  # léger coût de mouvement
                done = False

        # Mettre à jour l'état
        self.state = (new_row, new_col)

        # Vérifie si on a dépassé le nombre max de steps
        if self.current_step >= self.max_steps:
            done = True

        return self._to_obs(self.state), reward, done, {}

    def render(self, mode='human'):
        """
        Optionnel: affichage simplifié de la grille.
        """
        row, col = self.state
        grid_disp = []
        for r, row_str in enumerate(self.grid):
            row_list = list(row_str)
            if r == row:
                row_list[col] = 'P' if row_list[col] != 'g' else 'G'
            grid_disp.append(" ".join(row_list))
        print("\n".join(grid_disp))
        print()

    def _to_obs(self, state):
        """
        Convertit (row, col) en un entier (index).
        """
        (r, c) = state
        return r * self.n_cols + c


# =========================
# 2) Définition du réseau de neurones (DQN)
# =========================

class QNetwork(nn.Module):
    def __init__(self, state_size, action_size, hidden_size=64):
        super(QNetwork, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, action_size)
        )

    def forward(self, x):
        return self.net(x)


# =========================
# 3) Agent DQN
# =========================

class DQNAgent:
    def __init__(
        self,
        state_size,
        action_size,
        lr=1e-3,
        gamma=0.99,
        batch_size=32,
        buffer_size=10_000,
        epsilon_start=1.0,
        epsilon_end=0.01,
        epsilon_decay=0.995
    ):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.batch_size = batch_size
        self.buffer_size = buffer_size

        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_end
        self.epsilon_decay = epsilon_decay

        # Réseaux
        self.q_network = QNetwork(self.state_size, self.action_size)
        self.target_network = QNetwork(self.state_size, self.action_size)
        self.update_target()  # copie initiale des poids

        self.optimizer = optim.Adam(self.q_network.parameters(), lr=lr)
        self.loss_fn = nn.MSELoss()

        # Mémoire de replay : on stocke (state, action, reward, next_state, done)
        self.memory = deque(maxlen=self.buffer_size)

    def update_target(self):
        """
        Copie les poids du réseau principal vers le réseau cible.
        """
        self.target_network.load_state_dict(self.q_network.state_dict())

    def remember(self, state, action, reward, next_state, done):
        """
        Stocke la transition dans la mémoire.
        """
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        """
        Choisit une action selon une politique epsilon-greedy.
        """
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)
        else:
            state_t = torch.FloatTensor([state])
            q_values = self.q_network(state_t)
            action = torch.argmax(q_values, dim=1).item()
            return action

    def replay(self):
        """
        Entraîne le réseau sur un batch de transitions échantillonnées.
        """
        if len(self.memory) < self.batch_size:
            return  # pas assez d'échantillons

        minibatch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*minibatch)

        # Convertir en tenseurs
        states_t = torch.FloatTensor(states)
        actions_t = torch.LongTensor(actions)
        rewards_t = torch.FloatTensor(rewards)
        next_states_t = torch.FloatTensor(next_states)
        dones_t = torch.FloatTensor(dones)

        # Q(s, a) actuel
        print(states_t)
        q_values = self.q_network(states_t)
        # On récupère la valeur Q des actions choisies
        q_values = q_values.gather(1, actions_t.unsqueeze(1)).squeeze(1)

        # Q-target = r + gamma * max(Q_target(s'), a) * (1 - done)
        with torch.no_grad():
            q_next = self.target_network(next_states_t)
            q_next_max = torch.max(q_next, dim=1)[0]
            q_targets = rewards_t + self.gamma * q_next_max * (1 - dones_t)

        loss = self.loss_fn(q_values, q_targets)

        # Backprop
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Mise à jour epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


# =========================
# 4) Programme principal: entraînement
# =========================

def main():
    env = GridEnv()
    state_size = env.observation_space.n   # (n_rows * n_cols)
    action_size = env.action_space.n       # 4
    agent = DQNAgent(state_size, action_size)

    n_episodes = 300
    update_target_freq = 20  # tous les 20 épisodes, on met à jour le réseau cible

    for episode in range(1, n_episodes + 1):
        state = env.reset()
        done = False
        total_reward = 0
        step_count = 0

        while not done:
            # Choix d'action
            action = agent.act(state)
            next_state, reward, done, info = env.step(action)

            agent.remember(state, action, reward, next_state, float(done))
            agent.replay()

            state = next_state
            total_reward += reward
            step_count += 1

        # Mise à jour du réseau cible
        if episode % update_target_freq == 0:
            agent.update_target()

        print(f"Episode {episode}: reward={total_reward:.2f}, steps={step_count}, epsilon={agent.epsilon:.2f}")

    # Test final: on observe ce que fait l'agent
    print("\n--- Test de l'agent entraîné ---")
    state = env.reset()
    done = False
    env.render()  # affichage initial

    while not done:
        action = agent.act(state)
        # On force epsilon=0 pour un test "greedy"
        # (ou on re-sauvegarde agent.epsilon avant, puis on la remet)
        saved_epsilon = agent.epsilon
        agent.epsilon = 0.0
        action = agent.act(state)
        agent.epsilon = saved_epsilon

        next_state, reward, done, info = env.step(action)
        state = next_state
        env.render()

    print("Fin de l'épisode test.")


if __name__ == "__main__":
    main()