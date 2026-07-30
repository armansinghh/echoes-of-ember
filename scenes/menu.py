import pygame
import config as cfg
from scenes.scene import Scene

class MenuScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.title_font = pygame.font.SysFont(None, 36)
        self.hint_font = pygame.font.SysFont(None, 20)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.set_scene("game")

    def update(self, dt):
        pass  # nothing to animate yet

    def draw(self, screen):
        screen.fill((20, 20, 30))

        title = self.title_font.render("Echoes of the Ember", True, (255, 200, 100))
        hint = self.hint_font.render("Press ENTER to start", True, (200, 200, 200))

        title_rect = title.get_rect(center=(cfg.VIRTUAL_WIDTH // 2, cfg.VIRTUAL_HEIGHT // 2 - 12))
        hint_rect = hint.get_rect(center=(cfg.VIRTUAL_WIDTH // 2, cfg.VIRTUAL_HEIGHT // 2 + 20))

        screen.blit(title, title_rect.topleft)
        screen.blit(hint, hint_rect.topleft)