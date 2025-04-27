import pygame

class TileKind:
    def __init__(self, name, color, is_solid):
        self.name = name
        self.color = color
        self.is_solid = is_solid

class Map:
    def __init__(self, map_file, tile_kinds, tile_size):
        self.tile_kinds = tile_kinds
        self.tile_size = tile_size
        self.tiles = []
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == 2:  # Départ
                    self.start_pos = (x * tile_size, y * tile_size)
                elif tile == 3:  # Arrivée
                    self.end_pos = (x * tile_size, y * tile_size)
        with open(map_file, "r") as file:
            for line in file:
                line = line.strip()
                if line:  # Ignore les lignes vides
                    row = [int(c) for c in line if c in '01']  # Ne prend que 0 et 1
                    if row:  # Si la ligne contient des données
                        self.tiles.append(row)
        
        # Debug: Affiche la carte chargée
        print("Map loaded:")
        for row in self.tiles:
            print(row)

    def draw(self, screen):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile < len(self.tile_kinds):  # Vérifie que l'index est valide
                    tile_kind = self.tile_kinds[tile]
                    rect = pygame.Rect(x * self.tile_size, y * self.tile_size, 
                                     self.tile_size, self.tile_size)
                    pygame.draw.rect(screen, tile_kind.color, rect)