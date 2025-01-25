import pygame
import sys
from mistralai import Mistral
from time import sleep

# Votre clé Mistral
MISTRAL_KEY = "MaFKaY7R8TYrOLd56ZDRBcUfatOrebRh"

# Nom du modèle Mistral
MODEL_NAME = "ministral-8b-latest"

# Initialisation du client Mistral
client = Mistral(api_key=MISTRAL_KEY)

# Paramètres généraux
TILE_SIZE = 50
FPS = 2  # images par seconde (pour laisser le temps de "voir" le mouvement)
WINDOW_TITLE = "Agent LLM avec Mistral sur PyGame"

# Grille : 
# - 'o' = espace libre
# - 'x' = mur
# - 'g' = objectif (goal) à atteindre
GRID = [
    "ooooo",
    "oxxoo",
    "oxxoo",
    "oooog",  # Le 'g' en fin de ligne représente la cible
]

# Position initiale du joueur (coordonnées [ligne, colonne])
player_row = 0
player_col = 0

# Couleurs (R, G, B)
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
GRAY   = (128, 128, 128)
BLUE   = (  0, 128, 255)  # Joueur
YELLOW = (255, 255,   0)  # Objectif

# --------------------------------------------------------------------------
# Fonction pour construire le prompt décrivant l’environnement
# --------------------------------------------------------------------------
def build_environment_prompt(grid, player_row, player_col):
    """
    Construit une chaîne de caractères décrivant la grille, 
    en marquant :
      - la position du joueur par 'P'
      - les murs par 'x'
      - les espaces libres par 'o'
      - l'objectif par 'g'
    """
    lines = []
    for r, row_str in enumerate(grid):
        row_representation = []
        for c, cell in enumerate(row_str):
            if r == player_row and c == player_col:
                row_representation.append("P")
            else:
                row_representation.append(cell)
        lines.append(" ".join(row_representation))

    grid_desc = "\n".join(f"Ligne {i}: {line}" for i, line in enumerate(lines))

    # On fournit aussi quelques instructions à l'LLM :
    # - Les actions possibles (LEFT, RIGHT, UP, DOWN)
    # - L'objectif : atteindre la case 'g'.
    prompt = (
        "Tu es un agent placé sur cette grille. "
        "'P' indique ta position actuelle, 'o' indique un espace libre, 'x' indique un mur, "
        "'g' indique l'objectif à atteindre. "
        "À chaque étape, tu dois renvoyer la meilleure action parmi [LEFT, RIGHT, UP, DOWN] pour te déplacer dans la grille "
        "sans traverser les murs, et atteindre la case marquée par 'g'.\n\n"
        f"{grid_desc}\n\n"
        "Quelle est la meilleure action (LEFT, RIGHT, UP ou DOWN) à effectuer ?"
    )
    return prompt

# --------------------------------------------------------------------------
# Fonction interrogeant l'LLM Mistral pour choisir l'action
# --------------------------------------------------------------------------
def get_action_from_llm(prompt):
    """
    Envoie le prompt à l'LLM Mistral et récupère la meilleure action (texte).
    On effectue un parsing très simple pour détecter si la réponse contient
    LEFT, RIGHT, UP ou DOWN. S'il n'y a pas de mot-clé détecté, on renvoie 'NONE'.
    """
    try:
        print("\n=== Prompt envoyé à Mistral ===")
        print(prompt)
        print("===============================")
        
        chat_response = client.chat.complete(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un agent qui se déplace dans une grille. "
                        "Ton but est de choisir l'une des actions dans la liste suivante : [LEFT, RIGHT, UP, DOWN]. "
                        "Ne propose aucune autre action. Tu n'as qu'un seul mot à dire."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.0,  # on force la cohérence, donc température basse
            max_tokens=50,
        )
        # On ajoute un petit délai pour éviter d'appeler trop vite l'API
        sleep(1)

        llm_answer = chat_response.choices[0].message.content.strip().upper()
        print("Réponse brute de l'LLM :", llm_answer)
        
    except Exception as e:
        print("Erreur lors de l'appel à Mistral:", e)
        return "NONE"

    # Parsing très simple de la réponse
    if "LEFT" in llm_answer:
        return "LEFT"
    elif "RIGHT" in llm_answer:
        return "RIGHT"
    elif "UP" in llm_answer:
        return "UP"
    elif "DOWN" in llm_answer:
        return "DOWN"
    else:
        return "NONE"


# --------------------------------------------------------------------------
# Vérifie si la position (row, col) est valide et non bloquée par un mur.
# --------------------------------------------------------------------------
def is_valid_position(grid, row, col):
    # On vérifie que (row, col) est dans les bornes de la grille
    if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
        return False
    
    cell = grid[row][col]
    # On vérifie que la case n'est pas un mur
    if cell == 'x':
        return False
    
    return True

# --------------------------------------------------------------------------
# Boucle principale
# --------------------------------------------------------------------------
def main():
    global player_row, player_col

    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)

    rows = len(GRID)
    cols = len(GRID[0])

    screen_width = cols * TILE_SIZE
    screen_height = rows * TILE_SIZE

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(FPS)

        # Événements pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Construire le prompt en fonction de l'état actuel
        prompt = build_environment_prompt(GRID, player_row, player_col)
        action = get_action_from_llm(prompt)
        print("Action choisie par l'LLM :", action)

        # Calculer la future position du joueur
        new_row, new_col = player_row, player_col
        if action == "LEFT":
            new_col -= 1
        elif action == "RIGHT":
            new_col += 1
        elif action == "UP":
            new_row -= 1
        elif action == "DOWN":
            new_row += 1
        else:
            # Aucune action reconnue, on reste sur place
            pass

        # Vérifier si cette nouvelle position est valide
        if is_valid_position(GRID, new_row, new_col):
            player_row, player_col = new_row, new_col

        # Vérifier si l'objectif est atteint
        if GRID[player_row][player_col] == 'g':
            print("Objectif atteint ! Bravo !")
            running = False

        # Dessiner la scène
        screen.fill(BLACK)

        for r in range(rows):
            for c in range(cols):
                cell = GRID[r][c]
                rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                if cell == 'o':
                    color = WHITE  # espace libre
                elif cell == 'x':
                    color = GRAY   # mur
                elif cell == 'g':
                    color = YELLOW # objectif
                else:
                    color = BLACK  # au cas où, mais normalement pas utilisé
                
                pygame.draw.rect(screen, color, rect, 0)

                # Dessine le joueur (BLEU)
                if r == player_row and c == player_col:
                    pygame.draw.rect(screen, BLUE, rect, 0)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()