import pygame

class Lantern:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/images/lantern.png").convert_alpha()
        self.width, self.height = self.image.get_size()

        # collision rect - kept smaller/centered than the full sprite so
        # touching the lantern feels fair (not the whole tall sprite is "solid")
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen, camera):
        screen_rect = camera.apply(self.rect)
        screen.blit(self.image, screen_rect.topleft)