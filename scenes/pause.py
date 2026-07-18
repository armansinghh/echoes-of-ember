import pygame
from scenes.scene import Scene

class PauseScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.SysFont(None, 32)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_scene("game")

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.render("PAUSED - press ESC to resume", True, (255, 255, 255))
        screen.blit(text, (20, 20))