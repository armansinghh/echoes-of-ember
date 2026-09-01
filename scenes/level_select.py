import copy
import random
import pygame

import config as cfg
from scenes.scene import Scene

# global level data
LEVELS = [
    {"id": "level_00", "name": "Tutorial: The Spark", "state": "unlocked"},
    {"id": "level_01", "name": "Level 1: The Ruins", "state": "locked"},
    {"id": "level_02", "name": "???", "state": "locked"},
    {"id": "level_03", "name": "???", "state": "locked"},
    {"id": "level_04", "name": "???", "state": "locked"},
    {"id": "level_05", "name": "???", "state": "locked"}
]

class LevelSelectScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        
        self.uses_virtual_canvas = False
        
        self.screen_w = pygame.display.get_surface().get_width()
        self.screen_h = pygame.display.get_surface().get_height()
        
        # generate random starts in bg (will replace with hand drawn assets later)
        random.seed(42)
        self.stars = [
            (random.randint(0, self.screen_w), random.randint(0, self.screen_h), random.randint(1, 2))
            for _ in range(120)
        ]
        
        self.levels = copy.deepcopy(LEVELS)

        cy = self.screen_h // 2
        dx = self.screen_w // 7
        y_offsets = [40, -80, 60, -70, 30, -50]
        
        for i, level in enumerate(self.levels):
            level["pos"] = (dx * (i + 1), cy + y_offsets[i])

        self.selected_index = 0
        
        self.title_font = pygame.font.SysFont(None, 36)
        self.prompt_font = pygame.font.SysFont(None, 24)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        
        if event.key == pygame.K_ESCAPE:
            self.manager.set_scene("menu")
            
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.selected_index = max(0, self.selected_index - 1)
            
        elif event.key in (pygame.K_RIGHT, pygame.K_d):
            self.selected_index = min(len(self.levels) - 1, self.selected_index + 1)
            
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            current_level = self.levels[self.selected_index]
            if current_level["state"] == "unlocked":
                self.manager.selected_level = current_level["id"]
                self.manager.transition_to("game")

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((10, 15, 30))

        current_time = pygame.time.get_ticks()
        for i, (star_x, star_y, radius) in enumerate(self.stars):
            twinkle = (current_time // 300 + i) % 3
            brightness = 140 + twinkle * 40
            pygame.draw.circle(screen, (brightness, brightness, brightness + 30), (star_x, star_y), radius)

        for i in range(len(self.levels) - 1):
            start_pos = self.levels[i]["pos"]
            end_pos = self.levels[i+1]["pos"]
            pygame.draw.aaline(screen, (55, 60, 80), start_pos, end_pos)

        for i, level in enumerate(self.levels):
            pos = level["pos"]
            is_selected = (i == self.selected_index)

            if level["state"] == "unlocked":
                pygame.draw.circle(screen, (220, 140, 40), pos, 12)
                pygame.draw.circle(screen, (255, 200, 60), pos, 6)
            else:
                pygame.draw.circle(screen, (85, 90, 105), pos, 6)

            # highlight
            if is_selected:
                pygame.draw.circle(screen, (255, 255, 255), pos, 18, width=2)

        
        selected_level = self.levels[self.selected_index]

        title_text = self.title_font.render(selected_level["name"], True, (255, 255, 255))
        screen.blit(title_text, (self.screen_w // 2 - title_text.get_width() // 2, self.screen_h - 110))

        if selected_level["state"] == "unlocked":
            prompt_label = "Press ENTER or SPACE to Play"
            prompt_color = (255, 220, 140)
        else:
            prompt_label = "Locked (Upcoming)"
            prompt_color = (130, 130, 140)

        prompt_text = self.prompt_font.render(prompt_label, True, prompt_color)
        screen.blit(prompt_text, (self.screen_w // 2 - prompt_text.get_width() // 2, self.screen_h - 70))