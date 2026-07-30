import pygame
from scenes.scene import Scene
from sprites.player import Player
from sprites.camera import Camera
from sprites.lantern import Lantern
from sprites.hazard import Hazard
import config as cfg

class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.start_pos = (100, 100)
        self.player = Player(*self.start_pos)

        self.world_width = 2000
        self.world_height = cfg.SCREEN_HEIGHT

        self.platforms = [
            pygame.Rect(0, cfg.SCREEN_HEIGHT - 40, self.world_width, 40),
            pygame.Rect(200, 480, 150, 20),
            pygame.Rect(450, 420, 150, 20),
            pygame.Rect(900, 450, 150, 20),
            pygame.Rect(1300, 400, 150, 20),
        ]

        self.hazards = [
            Hazard(650, cfg.SCREEN_HEIGHT - 40 - 20, 100, 20),
        ]

        self.lantern = Lantern(1850, cfg.SCREEN_HEIGHT - 35 - 160) 
        self.camera = Camera(cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT, self.world_width, self.world_height)

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

        for hazard in self.hazards:
            if self.player.rect.colliderect(hazard.rect):
                self.respawn()
                return

        if self.player.rect.colliderect(self.lantern.rect):
            self.won = True
            print("Level complete!")

    def draw(self, screen):
        screen.fill((0, 0, 51))
        for platform in self.platforms:
            pygame.draw.rect(screen, (153, 153, 0), self.camera.apply(platform))
        for hazard in self.hazards:
            hazard.draw(screen, self.camera)
        self.lantern.draw(screen, self.camera)
        self.player.draw(screen, self.camera)
        
        if self.won:
            font = pygame.font.SysFont(None, 48)
            text = font.render("Ember Reached the Lantern!", True, (255, 230, 140))
            screen.blit(text, (cfg.SCREEN_WIDTH // 2 - 220, cfg.SCREEN_HEIGHT // 2))