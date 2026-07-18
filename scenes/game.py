import pygame
from scenes.scene import Scene
from sprites.player import Player
import config as cfg

class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.player = Player(100, 100)
        self.ground_y = cfg.SCREEN_HEIGHT - 50  # temp floor

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_scene("pause")

    def update(self, dt):
        self.player.update(dt, self.ground_y)

    def draw(self, screen):
        screen.fill((10, 30, 20))
        pygame.draw.line(screen, (80, 60, 50), (0, self.ground_y), (cfg.SCREEN_WIDTH, self.ground_y), 4)
        self.player.draw(screen)