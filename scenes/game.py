import pygame
from scenes.scene import Scene
from sprites.player import Player
from sprites.camera import Camera
import config as cfg

class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.player = Player(100, 100)
        self.world_width = 2000
        self.world_height = cfg.SCREEN_HEIGHT

        self.platforms = [
            pygame.Rect(0, cfg.SCREEN_HEIGHT - 40, self.world_width, 40),
            pygame.Rect(200, 480, 150, 20),
            pygame.Rect(450, 420, 150, 20),
            pygame.Rect(900, 450, 150, 20),
            pygame.Rect(1300, 400, 150, 20),
        ]

        self.camera = Camera(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, self.world_width, self.world_height)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_scene("pause")

    def update(self, dt):
        self.player.update(dt, self.platforms)
        self.camera.update(self.player.rect)

    def draw(self, screen):
        screen.fill((10, 30, 20))
        for platform in self.platforms:
            pygame.draw.rect(screen, (80, 60, 50), self.camera.apply(platform))
        pygame.draw.rect(screen, self.player.color, self.camera.apply(self.player.rect))