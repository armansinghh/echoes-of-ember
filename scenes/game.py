import pygame
from scenes.scene import Scene
from sprites.player import Player
from sprites.camera import Camera
from sprites.lantern import Lantern
from sprites.hazard import Hazard
from sprites.platform import Platform
from sprites.background import Background, ParallaxLayer
from utils.spritesheet import load_frames
import config as cfg

class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.start_pos = (100, 100)
        self.player = Player(*self.start_pos)

        self.world_width = 2000
        self.world_height = cfg.VIRTUAL_HEIGHT

        # Collision rects - UNCHANGED, Player still collides against these directly
        self.platforms = [
            pygame.Rect(0, cfg.VIRTUAL_HEIGHT - 32, self.world_width, 24),
            # pygame.Rect(200, 140, 96, 12),
            # pygame.Rect(450, 112, 96, 12),
            # pygame.Rect(900, 128, 96, 12),
            # pygame.Rect(1300, 96, 96, 12),
        ]

        # Visual layer only - tiled art built on top of the same rects above
        tile_variants = load_frames("assets/images/tiles.png", 4)
        self.platform_visuals = [
            Platform(rect.x, rect.y, rect.width, rect.height, tile_variants)
            for rect in self.platforms
        ]

        # self.hazards = [
        #     Hazard(650, cfg.VIRTUAL_HEIGHT - 40 - 20, 100, 20),
        # ]

        self.lantern = Lantern(1850, cfg.VIRTUAL_HEIGHT - 35 - 160)
        self.camera = Camera(cfg.VIRTUAL_WIDTH, cfg.VIRTUAL_HEIGHT, self.world_width, self.world_height)
        self.background = Background([
            ParallaxLayer("assets/images/sky.png", scroll_factor=0.0),
            ParallaxLayer("assets/images/distant-ruins.png", scroll_factor=0.3),
            ParallaxLayer("assets/images/mid-ruins.png", scroll_factor=0.6),
        ])

        self.won = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_scene("pause")

    def respawn(self):
        self.player.rect.topleft = self.start_pos
        self.player.vel_x = 0
        self.player.vel_y = 0

    def update(self, dt):
        if self.won:
            return

        self.player.update(dt, self.platforms)
        self.camera.update(self.player.rect)

        if self.player.rect.top > self.world_height + 200:
            self.respawn()
            return

        # for hazard in self.hazards:
        #     if self.player.rect.colliderect(hazard.rect):
        #         self.respawn()
        #         return

        if self.player.rect.colliderect(self.lantern.rect):
            self.won = True
            print("Level complete!")

    def draw(self, screen):
        self.background.draw(screen, self.camera)
        for platform_visual in self.platform_visuals:
            platform_visual.draw(screen, self.camera)
        # for hazard in self.hazards:
        #     hazard.draw(screen, self.camera)
        self.lantern.draw(screen, self.camera)
        self.player.draw(screen, self.camera)

        if self.won:
            font = pygame.font.SysFont(None, 48)
            text = font.render("Ember Reached the Lantern!", True, (255, 230, 140))
            screen.blit(text, (cfg.SCREEN_WIDTH // 2 - 220, cfg.SCREEN_HEIGHT // 2))