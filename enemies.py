import pygame
import random


class Enemy:
    def __init__(self, x, y, tile_size, game_map):
        self.size = tile_size // 2
        self.hitbox = pygame.Rect(
            x + (tile_size - self.size) // 2,
            y + (tile_size - self.size) // 2,
            self.size,
            self.size
        )
        self.color = (0, 255, 0)
        self.speed = 2
        self.tile_size = tile_size
        self.game_map = game_map
        self.direction = random.choice([-1, 1])
        self.vertical_direction = random.choice([-1, 1])  # Add vertical movement

    def update(self, player):
        # Store old position
        old_x, old_y = self.hitbox.x, self.hitbox.y
        
        # Try horizontal movement
        self.hitbox.x += self.speed * self.direction
        
        # Check horizontal collision
        if self._check_collision():
            self.hitbox.x = old_x
            self.direction *= -1
            # Try vertical movement when horizontal is blocked
            self.hitbox.y += self.speed * self.vertical_direction
            if self._check_collision():
                self.hitbox.y = old_y
                self.vertical_direction *= -1

        # Check player collision
        if self.hitbox.colliderect(player.hitbox):
            print("Le joueur est touché !")

    def _check_collision(self):
        """Optimized collision check using nearby tiles only"""
        start_x = max(0, self.hitbox.left // self.tile_size - 1)
        end_x = min(len(self.game_map.tiles[0]), (self.hitbox.right // self.tile_size) + 1)
        start_y = max(0, self.hitbox.top // self.tile_size - 1)
        end_y = min(len(self.game_map.tiles), (self.hitbox.bottom // self.tile_size) + 1)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.game_map.tile_kinds[self.game_map.tiles[y][x]].is_solid:
                    wall_rect = pygame.Rect(
                        x * self.tile_size,
                        y * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    if self.hitbox.colliderect(wall_rect):
                        return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.hitbox)