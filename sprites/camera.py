import pygame

class Camera:
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self, target_rect):
        self.offset_x = target_rect.centerx - self.screen_width // 2
        self.offset_y = target_rect.centery - self.screen_height // 2

        self.offset_x = max(0, min(self.offset_x, self.world_width - self.screen_width))
        self.offset_y = max(0, min(self.offset_y, self.world_height - self.screen_height))

    def apply(self, rect):
        return pygame.Rect(rect.x - self.offset_x, rect.y - self.offset_y, rect.width, rect.height)