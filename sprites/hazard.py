import pygame

from utils.animation import Animation
from utils.spritesheet import load_frames


class Hazard:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

        frames = load_frames("assets/images/hazards/frost.png", 5)
        self.anim = Animation(frames, fps=4)

    def update(self, dt):
        self.anim.update(dt)

    def draw(self, screen, camera):
        frame = self.anim.get_frame()
        screen_rect = camera.apply(self.rect)

        draw_rect = frame.get_rect(midbottom=screen_rect.midbottom)
        screen.blit(frame, draw_rect.topleft)