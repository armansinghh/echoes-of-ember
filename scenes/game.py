import pygame

import config as cfg
from scenes.scene import Scene
from sprites.background import Background, ParallaxLayer
from sprites.camera import Camera
from sprites.hazard import Hazard
from sprites.lantern import Lantern
from sprites.platform import Platform
from sprites.player import Player
from sprites.leak import LeakTile
from sprites.droplet import Droplet
from utils.spritesheet import load_frames
from utils.level_loader import load_level


class GameScene(Scene):
    """
    this is da main gameplay state, handles level loading, player updates,
    collision detection, and rendering the game world
    """
    def __init__(self, manager):
        super().__init__(manager)

        level_name = getattr(manager, "selected_level", "level_00")
        level = load_level(level_name)

        self.start_pos = level["start_pos"]
        self.player = Player(*self.start_pos)

        self.world_width = level["world_width"]
        self.world_height = cfg.VIRTUAL_HEIGHT

        # these are collision rects; physics engine only cares about these invisible rectangles
        # this separation allows us to use simple math for collisions while drawing complex art
        self.ceilings = level["ceilings"]
        self.platforms = level["platforms"] + self.ceilings  # physics treats both the same

        # tile art built directly on top of the collision rects
        tile_variants = load_frames("assets/images/environment/tiles.png", 4)
        self.platform_visuals = [
            Platform(rect.x, rect.y, rect.width, rect.height, tile_variants)
            for rect in level["platforms"]
        ]

        roof_tile_variants = load_frames("assets/images/environment/roof-tiles.png", 4)
        self.ceiling_visuals = [
            Platform(rect.x, rect.y, rect.width, rect.height, roof_tile_variants)
            for rect in self.ceilings
        ]

        self.leak_visuals = [LeakTile(leak["x"], leak["y"]) for leak in level["leaks"]]

        self.droplets = [
            Droplet(leak["x"] + 32, leak["y"] + 76, leak["floor_y"])
            for leak in level["leaks"]
        ]

        self.voids = level["voids"]

        self.hazards = [
            Hazard(rect.x, rect.y, rect.width, rect.height)
            for rect in level["hazards"]
        ]

        self.lantern = Lantern(*level["lantern"])
        self.camera = Camera(cfg.VIRTUAL_WIDTH, cfg.VIRTUAL_HEIGHT, self.world_width, self.world_height)
        
        self.background = Background([
            ParallaxLayer(
                layer["image"],
                scroll_factor=layer["scroll_factor"],
                repeats=layer["repeats"],
                world_width=self.world_width,
            )
            for layer in level["background"]
        ])

        self.won = False
        
        # cache the font here so we don't instantiate it FPS times a second during the draw loop
        self.win_font = pygame.font.SysFont(None, 48)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_scene("pause")

    def respawn(self):
        # resets the player to the starting position and clears its physics state
        self.player.reset(*self.start_pos)

    def update(self, dt):
        if self.won:
            return

        self.player.update(dt, self.platforms)
        self.camera.update(self.player.rect)

        if self.player.rect.top > self.world_height + 200:
            self.respawn()
            return

        for droplet in self.droplets:
            droplet.update(dt)
            if droplet.is_hazardous() and self.player.rect.colliderect(droplet.rect):
                self.respawn()
                return

        for hazard in self.hazards:
            hazard.update(dt)
            if self.player.rect.colliderect(hazard.rect):
                self.respawn()
                return

        for leak_visual, droplet in zip(self.leak_visuals, self.droplets):
            leak_visual.update(dt)
            if leak_visual.consume_spawn_trigger():
                droplet.start_new_drop()

            droplet.update(dt)
            if droplet.is_hazardous() and self.player.rect.colliderect(droplet.rect):
                self.respawn()
                return

        # goal check
        if self.player.rect.colliderect(self.lantern.rect):
            self.won = True
            print("Level complete!") # temp

    def draw(self, screen):
        self.background.draw(screen, self.camera)
        
        for platform_visual in self.platform_visuals:
            platform_visual.draw(screen, self.camera)

        for ceiling_visual in self.ceiling_visuals:
            ceiling_visual.draw(screen, self.camera)

        for leak_visual in self.leak_visuals:
            leak_visual.draw(screen, self.camera)

        for droplet in self.droplets:
            droplet.draw(screen, self.camera)

        for rect, color in self.voids:
            pygame.draw.rect(screen, color, self.camera.apply(rect))
            
        for hazard in self.hazards:
            hazard.draw(screen, self.camera)
            
        self.lantern.draw(screen, self.camera)
        self.player.draw(screen, self.camera)

        if self.won:
            text = self.win_font.render("Ember Reached the Lantern!", True, (255, 230, 140))
            text_rect = text.get_rect(center=(cfg.VIRTUAL_WIDTH // 2, cfg.VIRTUAL_HEIGHT // 2))
            screen.blit(text, text_rect)