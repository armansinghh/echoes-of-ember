import random
import pygame

class Platform:
    def __init__(self, x, y, width, height, tile_variants):
        self.rect = pygame.Rect(x, y, width, height)
        self.tile_variants = tile_variants
        self.tile_size = tile_variants[0].get_width()  # assumes square tiles, e.g. 32

        cols = self.rect.width // self.tile_size + 1   # +1 covers any leftover partial tile
        rows = self.rect.height // self.tile_size + 1

        # Pick a tile variant for each grid cell ONCE, so it stays fixed
        # instead of flickering to a new random tile every frame
        self.tile_map = [
            [random.randrange(len(tile_variants)) for _ in range(cols)]
            for _ in range(rows)
        ]

    def draw(self, screen, camera):
        for row_index, row in enumerate(self.tile_map):
            for col_index, variant_index in enumerate(row):
                tile_image = self.tile_variants[variant_index]
                x = self.rect.x + col_index * self.tile_size
                y = self.rect.y + row_index * self.tile_size
                screen_rect = camera.apply(pygame.Rect(x, y, self.tile_size, self.tile_size))
                screen.blit(tile_image, screen_rect.topleft)