import pygame

class Hazard:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (40, 10, 50)

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color, camera.apply(self.rect))