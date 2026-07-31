import pygame


class Lantern:
    """
    da goal object at the end; touching this triggers the win state
    """
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/images/lantern.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (96, 160))
        
        # we define the full visual boundary based on the provided x, y coordinates
        visual_rect = pygame.Rect(x, y, 96, 160)

        self.rect = visual_rect.inflate(-48, -80)

    def draw(self, screen, camera):
        # translate the collision hitbox into screen coordinates
        screen_rect = camera.apply(self.rect)
        
        draw_rect = self.image.get_rect(center=screen_rect.center)
        screen.blit(self.image, draw_rect.topleft)