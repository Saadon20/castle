import pygame
import sys
import os
from castle.map import Map, TileKind
from castle.soldier import Player
from castle.enemies import Enemy
from castle.collision import check_collision_with_enemies
from castle.diamonds import Diamond, generate_diamonds

def main():
    # Initialisation Pygame
    pygame.init()
    screen_width = 640
    screen_height = 640
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Maze Game")
    font = pygame.font.Font(None, 36)

    #ééééééééééééééééééééééééééééConfiguration des tuiles
    tile_size = 32
    tile_kinds = [
        TileKind("floor", (200, 200, 200), False),  # 0
        TileKind("wall", (50, 50, 50), True),       # 1
        TileKind("start", (0, 255, 0), False),      # 2 (non-solide)
        TileKind("end", (255, 0, 0), False)         # 3 (non-solide)
    ]
    
    # Game states
    PLAYING = 0
    GAME_OVER = 1
    game_state = PLAYING
    
    

    # Chargement de la carte
    try:
        map_path = os.path.join(os.path.dirname(__file__), "start.map")
        game_map = Map(map_path, tile_kinds, tile_size)
    except FileNotFoundError:
        print("ERREUR: Fichier start.map introuvable!")
        pygame.quit()
        sys.exit()

    # Initialisation des entités
    player = Player(1 * tile_size, 1 * tile_size, tile_size)
    enemies = [
        Enemy(5 * tile_size, 3 * tile_size, tile_size, game_map),
        Enemy(8 * tile_size, 7 * tile_size, tile_size, game_map),
        Enemy(13 * tile_size, 13 * tile_size, tile_size, game_map),
        Enemy(13 * tile_size, 15 * tile_size, tile_size, game_map),
        Enemy(13 * tile_size, 17 * tile_size, tile_size, game_map),
        Enemy(16 * tile_size, 1 * tile_size, tile_size, game_map)
    ]
    diamonds = generate_diamonds(game_map, tile_size, density=0.15)
    score = 0
    game_won = False

    # Boucle principale
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_state == GAME_OVER:
                if event.key == pygame.K_r:  # Restart game
                    game_state = PLAYING
                    player = Player(1 * tile_size, 1 * tile_size, tile_size)
                    enemies = [
                        Enemy(5 * tile_size, 3 * tile_size, tile_size, game_map),
                        Enemy(4 * tile_size, 15 * tile_size, tile_size, game_map),
                        Enemy(8 * tile_size, 7 * tile_size, tile_size, game_map),
                        Enemy(13 * tile_size, 13 * tile_size, tile_size, game_map),
                        Enemy(13 * tile_size, 15 * tile_size, tile_size, game_map),
                        Enemy(16 * tile_size, 1 * tile_size, tile_size, game_map)
                    ]
                    diamonds = generate_diamonds(game_map, tile_size, density=0.15)
                    score = 0
        
        # Mise à jour du jeu
        if game_state == PLAYING:
            # Gestion des entrées joueur
            keys = pygame.key.get_pressed()
            player.handle_movement(keys, game_map)
            
            # Update bullets and check for enemy hits
            for bullet in player.bullets[:]:  # Use a copy to safely modify during iteration
                if not bullet.update(game_map, enemies):
                    player.bullets.remove(bullet)
                else:
                    # If bullet hit an enemy, increase score
                    score += 5
            
            # Mise à jour des ennemis
            for enemy in enemies[:]:  # Use a copy to safely modify during iteration
                enemy.update(player)
            
            # Vérification des collisions avec les ennemis
            if check_collision_with_enemies(player.hitbox, enemies):
                game_state = GAME_OVER
            
            # Vérification des collisions avec les diamants
            for diamond in diamonds[:]:  # Utilisez une copie de la liste
                if not diamond.collected:
                    if player.hitbox.colliderect(diamond.rect):
                        diamond.collected = True
                        score += 10
                        diamonds.remove(diamond)  # Retire immédiatement le diamant

        # Rendu
        screen.fill((0, 0, 0))  # Fond noir
        game_map.draw(screen)
        
        # Draw bullets
        for bullet in player.bullets:
            bullet.draw(screen)
            
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
            
        # Dessin des diamants
        for diamond in diamonds:
            diamond.draw(screen)
        
        # Affichage du score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Afficher le message de fin de jeu
        if game_state == GAME_OVER:
            game_over_text = font.render("GAME OVER - Press R to restart", True, (255, 0, 0))
            screen.blit(game_over_text, (screen_width//2 - 180, screen_height//2 - 18))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()