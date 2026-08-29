import pygame

import config as cfg
from scenes.scene import Scene
from sprites.background import Background, ParallaxLayer
from sprites.camera import Camera
from sprites.lantern import Lantern
from sprites.platform import Platform
from sprites.player import Player
from utils.spritesheet import load_frames

LEVELS = [
    {"id": "level_00", "name": "Tutorial", "x": 300, "state": "unlocked"},
    {"id": "level_01", "name": "The Ruins", "x": 700, "state": "locked"},
]

PROXIMITY_RANGE = 70


class LevelSelectScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.world_width = 1200
        self.world_height = cfg.VIRTUAL_HEIGHT

        ground_y = cfg.VIRTUAL_HEIGHT - 40
        self.platforms = [pygame.Rect(0, ground_y, self.world_width, 40)]

        tile_variants = load_frames("assets/images/tiles.png", 4)
        self.platform_visuals = [
            Platform(rect.x, rect.y, rect.width, rect.height, tile_variants)
            for rect in self.platforms
        ]

        self.player = Player(100, ground_y - 72)
        self.camera = Camera(cfg.VIRTUAL_WIDTH, cfg.VIRTUAL_HEIGHT, self.world_width, self.world_height)

        self.background = Background([
            ParallaxLayer("assets/images/sky.png", scroll_factor=0.0, repeats=0, world_width=self.world_width),
            ParallaxLayer("assets/images/distant-ruins.png", scroll_factor=0.3, repeats=2, world_width=self.world_width),
            ParallaxLayer("assets/images/mid-ruins.png", scroll_factor=0.6, repeats=2, world_width=self.world_width),
        ])

        self.lanterns = [
            Lantern(level["x"], ground_y - 160, is_lit=(level["state"] == "unlocked")) 
            for level in LEVELS
        ]

        self.near_level = None
        self.prompt_font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 32)

    def on_enter(self):
        self.player.reset(100, cfg.VIRTUAL_HEIGHT - 40 - 72)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_ESCAPE:
            self.manager.set_scene("menu")
        elif event.key == pygame.K_RETURN and self.near_level:
            if self.near_level["state"] == "unlocked":
                self.manager.selected_level = self.near_level["id"]
                self.manager.transition_to("game")

    def update(self, dt):
        self.player.update(dt, self.platforms)
        self.camera.update(self.player.rect)

        self.near_level = None
        for level in LEVELS:
            if abs(self.player.rect.centerx - level["x"]) <= PROXIMITY_RANGE:
                self.near_level = level
                break

    def draw(self, screen):
        self.background.draw(screen, self.camera)
        for platform_visual in self.platform_visuals:
            platform_visual.draw(screen, self.camera)
            
        for lantern in self.lanterns:
            lantern.draw(screen, self.camera)

        self.player.draw(screen, self.camera)

        if self.near_level:
            screen_x = self.near_level["x"] - self.camera.offset_x
            screen_y = (cfg.VIRTUAL_HEIGHT - 200) - self.camera.offset_y
            
            title_text = self.title_font.render(self.near_level["name"], True, (255, 255, 255))
            screen.blit(title_text, (screen_x + 16 - title_text.get_width() // 2, screen_y - 30))

            if self.near_level["state"] == "unlocked":
                label = "Press ENTER"
                color = (255, 230, 140)
            else:
                label = "Locked"
                color = (150, 150, 150)
                
            prompt_text = self.prompt_font.render(label, True, color)
            screen.blit(prompt_text, (screen_x + 16 - prompt_text.get_width() // 2, screen_y - 10))