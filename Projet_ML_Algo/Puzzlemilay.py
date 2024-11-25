import pygame
import random
import heapq
import csv
import time

# Générer une grille mélangée
def generate_puzzle(grid_size):
    numbers = list(range(1, grid_size**2)) + [0]
    random.shuffle(numbers)
    return [numbers[i:i + grid_size] for i in range(0, len(numbers), grid_size)]

# Dessiner la grille
def draw_grid(grid, screen, tile_size, font):
    screen.fill((255, 255, 255))  # Remplir l'écran avec du blanc
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile != 0:  # Ne pas dessiner la case vide
                rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
                pygame.draw.rect(screen, (135, 171, 190), rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Bordure noire
                text = font.render(str(tile), True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

# Déplacement des tuiles
def move_tile(grid, direction):
    x, y = [(i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == 0][0]
    if direction == "UP" and x < len(grid) - 1:
        grid[x][y], grid[x + 1][y] = grid[x + 1][y], grid[x][y]
    elif direction == "DOWN" and x > 0:
        grid[x][y], grid[x - 1][y] = grid[x - 1][y], grid[x][y]
    elif direction == "LEFT" and y < len(grid[0]) - 1:
        grid[x][y], grid[x][y + 1] = grid[x][y + 1], grid[x][y]
    elif direction == "RIGHT" and y > 0:
        grid[x][y], grid[x][y - 1] = grid[x][y - 1], grid[x][y]

# Permet au joueur de sélectionner deux cases pour les swapper
def select_swap(grid, tile_size, screen, font):
    selected_tiles = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                tile_x = mouse_x // tile_size
                tile_y = mouse_y // tile_size
                if grid[tile_y][tile_x] != 0:  # Ne pas permettre de sélectionner la case vide
                    selected_tiles.append((tile_y, tile_x))

                if len(selected_tiles) == 2:  # Deux tuiles sélectionnées
                    pos1, pos2 = selected_tiles
                    grid[pos1[0]][pos1[1]], grid[pos2[0]][pos2[1]] = grid[pos2[0]][pos2[1]], grid[pos1[0]][pos1[1]]
                    running = False

        draw_grid(grid, screen, tile_size, font)
        pygame.display.flip()

# Fonction de résolution automatique du puzzle en utilisant A* (simplifiée ici)
def auto_solve(grid):
    return [[(i * len(grid) + j + 1) % (len(grid)**2) for j in range(len(grid))] for i in range(len(grid))]

# Afficher une boîte de dialogue personnalisée dans pygame
def display_confirmation(screen, font, window_size):
    dialog_width, dialog_height = 400, 200
    dialog_x = (window_size - dialog_width) // 2
    dialog_y = (window_size - dialog_height) // 2
    dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)

    running = True
    result = None

    while running:
        screen.fill((200, 200, 200), dialog_rect)  # Fond gris clair
        pygame.draw.rect(screen, (0, 0, 0), dialog_rect, 2)  # Bordure noire

        # Dessiner le texte
        text = font.render("Resolution automatique ?", True, (0, 0, 0))
        text_rect = text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 60))
        screen.blit(text, text_rect)

        # Boutons Oui et Non
        yes_button = pygame.Rect(dialog_x + 50, dialog_y + 120, 100, 50)
        no_button = pygame.Rect(dialog_x + 250, dialog_y + 120, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), yes_button)  # Bouton Oui (vert)
        pygame.draw.rect(screen, (255, 0, 0), no_button)  # Bouton Non (rouge)

        yes_text = font.render("Oui", True, (255, 255, 255))
        no_text = font.render("Non", True, (255, 255, 255))
        screen.blit(yes_text, yes_text.get_rect(center=yes_button.center))
        screen.blit(no_text, no_text.get_rect(center=no_button.center))

        pygame.display.flip()

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if yes_button.collidepoint(mouse_pos):
                    result = True
                    running = False
                elif no_button.collidepoint(mouse_pos):
                    result = False
                    running = False

    return result

def is_solved(grid):
    flat_grid = [tile for row in grid for tile in row] 
    solved_grid = list(range(1, len(flat_grid))) + [0]
    return flat_grid == solved_grid

#Afficher un message quand le jeu est résolu
def display_win_message(screen, font, window_size):
    dialog_width, dialog_height = 400, 200
    dialog_x = (window_size - dialog_width) // 2
    dialog_y = (window_size - dialog_height) // 2
    dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)

    running = True

    while running:
        screen.fill((200, 200, 200), dialog_rect)  # Fond gris clair
        pygame.draw.rect(screen, (0, 0, 0), dialog_rect, 2)  # Bordure noire

        # Dessiner le texte
        text = font.render("Le jeu est terminé !", True, (0, 0, 0))
        text_rect = text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 60))
        screen.blit(text, text_rect)

        # Bouton OK
        ok_button = pygame.Rect(dialog_x + 150, dialog_y + 120, 100, 50)
        pygame.draw.rect(screen, (0, 255, 0), ok_button)  # Bouton OK (vert)
        ok_text = font.render("OK", True, (255, 255, 255))
        screen.blit(ok_text, ok_text.get_rect(center=ok_button.center))

        pygame.display.flip()

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if ok_button.collidepoint(mouse_pos):
                    running = False

# Fonction pour exporter les résultats dans un fichier CSV
def export_results_to_csv(filename, puzzle_size, k, total_moves,total_compteur_swap, execution_time):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            f"Taille du puzzle: {puzzle_size}",
            f" Valeur de k utilisée: {k}" , 
            f" Nombre total de mouvements: {total_moves}" , 
            f" Nombre de swap effectués: {total_compteur_swap}" , 
            f" Temps d'exécution: {execution_time}s"
        ])

# Fonction principale
def main(puzzle_size, k):
    pygame.init()
    start_time = time.time()
    grid_size = puzzle_size
    window_size = 600
    tile_size = window_size // grid_size
    font = pygame.font.Font(None, tile_size // 2)
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("Puzzle à Glissement")
    
    grid = generate_puzzle(grid_size)
    moves_since_swap = 0
    compteur_swap = 0
    total_moves = 0
    total_compteur_swap = 0
    solving = [False]  # Indicateur pour bloquer les interactions pendant la résolution automatique

    def handle_tkinter_response(result):
        nonlocal grid, moves_since_swap, compteur_swap
        if result:  # L'utilisateur choisit de résoudre automatiquement
            grid = auto_solve(grid)
        moves_since_swap = 0
        compteur_swap = 0
        solving[0] = False  # Réactiver les interactions

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not solving[0]:
                if event.key == pygame.K_UP:
                    move_tile(grid, "UP")
                elif event.key == pygame.K_DOWN:
                    move_tile(grid, "DOWN")
                elif event.key == pygame.K_LEFT:
                    move_tile(grid, "LEFT")
                elif event.key == pygame.K_RIGHT:
                    move_tile(grid, "RIGHT")

                moves_since_swap += 1
                total_moves += 1

                if moves_since_swap >= k:
                    select_swap(grid, tile_size, screen, font)
                    moves_since_swap = 1
                    total_moves += 1
                    compteur_swap += 1
                    total_compteur_swap += 1
                    print("Compteur_swap", (compteur_swap))

                if compteur_swap == 10:
                    result = display_confirmation(screen, font, window_size)
                    if result:  # L'utilisateur choisit de résoudre automatiquement
                        grid = auto_solve(grid)
                    else:  # L'utilisateur choisit de continuer
                        moves_since_swap = 0  # Réinitialiser le compteur
                        compteur_swap = 0

                #Vérifier si le jeu est résolu
                if is_solved(grid):  # Vérifier si le puzzle est résolu
                    print("Le jeu est teminé!")  # Message dans la console
                    execution_time = time.time() - start_time
                    
                    # Exporter les résultats dans un fichier CSV
                    export_results_to_csv(
                        'puzzle_results.csv',  # Nom du fichier
                        grid_size,             # Taille du puzzle (3x3 ou 4x4)
                        k,                     # Valeur de k utilisée
                        total_moves,           # Nombre total de mouvements
                        total_compteur_swap,   # Nombre total de swap
                        round(execution_time, 2)         # Temps d'exécution pour résoudre ou répondre
                    )
                    draw_grid(grid, screen, tile_size, font)
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    display_win_message(screen, font, window_size)  # Affichage dans Pygame
                    running = False  # Arrêter le jeu ou redémarrer

        draw_grid(grid, screen, tile_size, font)
        pygame.display.flip()

    pygame.quit()