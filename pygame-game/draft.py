import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir la taille de la fenêtre
LARGEUR_ECRAN, HAUTEUR_ECRAN = 800, 600
fenetre = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Déplacement d'un personnage")

# Couleurs
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

# Définir la position initiale du personnage
x_joueur = LARGEUR_ECRAN // 2
y_joueur = HAUTEUR_ECRAN // 2

# Dimensions du "personnage" (un simple rectangle ici)
largeur_joueur = 50
hauteur_joueur = 50

# Vitesse de déplacement
vitesse = 5

# Boucle principale
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # Limiter à 60 images par seconde
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    
    # Récupérer l'état des touches du clavier
    touches = pygame.key.get_pressed()

    # Avancer (vers le haut) - Touche "UP" ou "Z"
    if touches[pygame.K_UP] or touches[pygame.K_z]:
        y_joueur -= vitesse

    # Reculer (vers le bas) - Touche "DOWN" ou "S"
    if touches[pygame.K_DOWN] or touches[pygame.K_s]:
        y_joueur += vitesse

    # Aller à gauche - Touche "LEFT" ou "Q"
    if touches[pygame.K_LEFT] or touches[pygame.K_q]:
        x_joueur -= vitesse

    # Aller à droite - Touche "RIGHT" ou "D"
    if touches[pygame.K_RIGHT] or touches[pygame.K_d]:
        x_joueur += vitesse

    # (Optionnel) Empêcher le personnage de sortir de l'écran
    if x_joueur < 0:
        x_joueur = 0
    elif x_joueur + largeur_joueur > LARGEUR_ECRAN:
        x_joueur = LARGEUR_ECRAN - largeur_joueur
    
    if y_joueur < 0:
        y_joueur = 0
    elif y_joueur + hauteur_joueur > HAUTEUR_ECRAN:
        y_joueur = HAUTEUR_ECRAN - hauteur_joueur

    # Remplir l'écran en blanc
    fenetre.fill(BLANC)

    # Dessiner le joueur (un rectangle rouge)
    joueur_rect = pygame.Rect(x_joueur, y_joueur, largeur_joueur, hauteur_joueur)
    pygame.draw.rect(fenetre, ROUGE, joueur_rect)

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter le programme
pygame.quit()
sys.exit()