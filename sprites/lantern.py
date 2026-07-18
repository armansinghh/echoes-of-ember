import pygame

class Lantern:
    def __init__(self, x, y):
        self.width = 24
        self.height = 32
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (255, 230, 140)

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color, camera.apply(self.rect))