import pygame
from scenes.scene import Scene

class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont(None, 48)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.set_scene("game")

    def update(self, dt):
        pass  # nothing to animate yet

    def draw(self, screen):
        screen.fill((20, 20, 30))
        text = self.font.render("Echoes of the Ember", True, (255, 200, 100))
        screen.blit(text, (60, 250))
        hint = pygame.font.SysFont(None, 28).render("Press ENTER to start", True, (200, 200, 200))
        screen.blit(hint, (60, 320))