import pygame
import random
    

# Paramètres du jeu
WINDOW_SIZE = 600
GRID_SIZE = 3  # Pour le puzzle (3x3)
TILE_SIZE = WINDOW_SIZE // GRID_SIZE
FONT_SIZE = TILE_SIZE // 2

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Puzzle")
font = pygame.font.Font(None, FONT_SIZE)
clock = pygame.time.Clock()

# Générer une grille mélangée
def generate_puzzle(grid_size):
    numbers = list(range(1, grid_size**2)) + [0]
    random.shuffle(numbers)
    return [numbers[i:i + grid_size] for i in range(0, len(numbers), grid_size)]

# Dessiner la grille
def draw_grid(grid):
    screen.fill((255, 255, 255))  # Remplir l'écran avec du blanc
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] != 0:
                tile_color = (135, 171, 190)
                text_color = (255, 255, 255)
                rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, tile_color, rect)
                text = font.render(str(grid[i][j]), True, text_color)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            pygame.draw.rect(screen, (0, 0, 0), (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

d = 0  # Compteur de déplacements
moves_since_swap = 0  # Compte les déplacements depuis le dernier swap

# Déplacement des tuiles
def move_tile(grid, direction):
    global d, moves_since_swap
    x, y = [(i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == 0][0]

    if direction == "DOWN" and x > 0:
        grid[x][y], grid[x - 1][y] = grid[x - 1][y], grid[x][y]
        d += 1
        moves_since_swap += 1
    elif direction == "UP" and x < GRID_SIZE - 1:
        grid[x][y], grid[x + 1][y] = grid[x + 1][y], grid[x][y]
        d += 1
        moves_since_swap += 1
    elif direction == "RIGHT" and y > 0:
        grid[x][y], grid[x][y - 1] = grid[x][y - 1], grid[x][y]
        d += 1
        moves_since_swap += 1
    elif direction == "LEFT" and y < GRID_SIZE - 1:
        grid[x][y], grid[x][y + 1] = grid[x][y + 1], grid[x][y]
        d += 1
        moves_since_swap += 1

    print(f"Déplacements: {d} (Déplacements depuis le dernier swap: {moves_since_swap})")

# Swap des tuiles
def swap_tiles(grid, pos1, pos2):
    global d, moves_since_swap
    x1, y1 = pos1
    x2, y2 = pos2
    grid[x1][y1], grid[x2][y2] = grid[x2][y2], grid[x1][y1]
    d += 1  # Incrémenter le compteur de déplacements pour chaque swap
    moves_since_swap = 0  # Réinitialiser le compteur des déplacements depuis le dernier swap
    print(f"Swap effectué. Déplacements: {d} (Déplacements depuis le dernier swap: {moves_since_swap})")

# Fenêtre de sélection pour choisir deux tuiles à échanger
def select_swap(grid):
    global d, moves_since_swap
    running = True
    selected_tiles = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Récupérer la position du clic de la souris
                mouse_x, mouse_y = event.pos
                tile_x = mouse_x // TILE_SIZE
                tile_y = mouse_y // TILE_SIZE
                if grid[tile_y][tile_x] != 0:  # On peut seulement sélectionner une tuile différente de 0
                    selected_tiles.append((tile_y, tile_x))

                if len(selected_tiles) == 2:  # Une fois que 2 tuiles sont sélectionnées, on les swappe
                    swap_tiles(grid, selected_tiles[0], selected_tiles[1])
                    running = False  # Quitter la fenêtre de sélection

        # Dessiner la grille pendant la sélection
        draw_grid(grid)
        pygame.display.flip()  # Mettre à jour l'affichage

# Boucle principale du jeu
def main(k):
    _k = int(k)
    global d, moves_since_swap
    grid = generate_puzzle(GRID_SIZE)
    selected_tile = None  # Aucune case n'est sélectionnée au départ
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_tile(grid, "UP")
                elif event.key == pygame.K_DOWN:
                    move_tile(grid, "DOWN")
                elif event.key == pygame.K_LEFT:
                    move_tile(grid, "LEFT")
                elif event.key == pygame.K_RIGHT:
                    move_tile(grid, "RIGHT")

                # Si "Entrée" est pressé, on swap la tuile sélectionnée
                if event.key == pygame.K_RETURN:
                    if selected_tile is None:
                        # Si aucune case n'est sélectionnée, on sélectionne la case vide
                        selected_tile = tuple([(i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == 0][0])
                    else:
                        # Si une case est sélectionnée, on effectue le swap avec la case actuelle
                        current_pos = tuple([(i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == 0][0])
                        if selected_tile != current_pos:  # On ne swappe pas la même case
                            swap_tiles(grid, selected_tile, current_pos)
                        selected_tile = None  # Réinitialiser la sélection

        # Afficher la fenêtre de sélection après k déplacements (y compris swaps)
        if moves_since_swap >= _k:  # On attend k déplacements depuis le dernier swap
            select_swap(grid)

        # Dessiner la grille normalement
        draw_grid(grid)
        pygame.display.flip()  # Mettre à jour l'affichage

        clock.tick(30)

    pygame.quit()


