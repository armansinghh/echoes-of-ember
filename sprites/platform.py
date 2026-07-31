import math
import random
import pygame


class Platform:
    def __init__(self, x, y, width, height, tile_variants):
        self.rect = pygame.Rect(x, y, width, height)
        self.tile_variants = tile_variants
        self.tile_size = tile_variants[0].get_width()

        # use ceil to prevent drawing extra tiles if dimensions are exactly divisible
        cols = math.ceil(self.rect.width / self.tile_size)
        rows = math.ceil(self.rect.height / self.tile_size)

        # cache random tile choices so they don't visually flicker every frame
        self.tile_map = [
            [random.randrange(len(tile_variants)) for _ in range(cols)]
            for _ in range(rows)
        ]

    def draw(self, screen, camera):
        # apply camera offset once here to avoid expensive rect creations inside the nested loop
        base_screen_rect = camera.apply(self.rect)

        for row_index, row in enumerate(self.tile_map):
            for col_index, variant_index in enumerate(row):
                tile_image = self.tile_variants[variant_index]
                
                screen_x = base_screen_rect.x + (col_index * self.tile_size)
                screen_y = base_screen_rect.y + (row_index * self.tile_size)
                
                screen.blit(tile_image, (screen_x, screen_y))