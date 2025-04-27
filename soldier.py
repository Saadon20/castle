import pygame
from castle.bullet import Bullet

class Player:
    def __init__(self, x, y, tile_size, color=(255, 0, 0)):
        self.size = int(tile_size * 0.7)
        self.hitbox = pygame.Rect(
            x + (tile_size - self.size) // 2,
            y + (tile_size - self.size) // 2,
            self.size,
            self.size
        )
        self.color = color
        self.speed = 4
        self.tile_size = tile_size
        self.bullets = []
        self.shoot_cooldown = 0
        self.last_direction = (1, 0)  # Default to right direction
        
        # Track which keys were pressed last
        self.last_keys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_UP: False,
            pygame.K_DOWN: False
        }

    def handle_movement(self, keys, game_map):
        dx, dy = 0, 0
        
        # Update movement and track last direction
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.last_direction = (-1, 0)
            self.last_keys[pygame.K_LEFT] = True
            self.last_keys[pygame.K_RIGHT] = False
        elif keys[pygame.K_RIGHT]:
            dx = self.speed
            self.last_direction = (1, 0)
            self.last_keys[pygame.K_RIGHT] = True
            self.last_keys[pygame.K_LEFT] = False
        
        if keys[pygame.K_UP]:
            dy = -self.speed
            self.last_direction = (0, -1)
            self.last_keys[pygame.K_UP] = True
            self.last_keys[pygame.K_DOWN] = False
        elif keys[pygame.K_DOWN]:
            dy = self.speed
            self.last_direction = (0, 1)
            self.last_keys[pygame.K_DOWN] = True
            self.last_keys[pygame.K_UP] = False

        # Shooting logic
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            self.shoot()
            self.shoot_cooldown = 10  # Cooldown frames

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self._move(dx, dy, game_map)

    def shoot(self):
        # Use the last direction stored
        direction_x, direction_y = self.last_direction
        
        # Create bullet from center
        bullet_x = self.hitbox.x + self.hitbox.width // 2
        bullet_y = self.hitbox.y + self.hitbox.height // 2
        self.bullets.append(Bullet(bullet_x, bullet_y, direction_x, direction_y, self.tile_size))

    # ... (keep the rest of the methods the same)

    def _move(self, dx, dy, game_map):
        # Déplacement horizontal
        self.hitbox.x += dx
        walls = self._get_colliding_walls(game_map)
        for wall in walls:
            if dx > 0:  # Collision droite
                self.hitbox.right = wall.left
            elif dx < 0:  # Collision gauche
                self.hitbox.left = wall.right

        # Déplacement vertical
        self.hitbox.y += dy
        walls = self._get_colliding_walls(game_map)
        for wall in walls:
            if dy > 0:  # Collision bas
                self.hitbox.bottom = wall.top
            elif dy < 0:  # Collision haut
                self.hitbox.top = wall.bottom

    def _get_colliding_walls(self, game_map):
        walls = []
        player_rect = self.hitbox.copy()
        
        # Calcul des tuiles à vérifier
        start_x = max(0, player_rect.left // self.tile_size - 1)
        end_x = min(len(game_map.tiles[0]), (player_rect.right // self.tile_size) + 1)
        start_y = max(0, player_rect.top // self.tile_size - 1)
        end_y = min(len(game_map.tiles), (player_rect.bottom // self.tile_size) + 1)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if game_map.tile_kinds[game_map.tiles[y][x]].is_solid:
                    wall_rect = pygame.Rect(
                        x * self.tile_size,
                        y * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    if player_rect.colliderect(wall_rect):
                        walls.append(wall_rect)
        return walls

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.hitbox)