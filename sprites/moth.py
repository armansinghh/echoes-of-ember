# sprites/moth.py
import math
import random
import pygame

from utils.animation import Animation
from utils.spritesheet import load_frames


class Moth:
    DETECTION_RANGE = 200
    GIVE_UP_RANGE = 280

    def __init__(self, spawn_x, spawn_y):
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

        frames = load_frames("assets/images/hazards/moth.png", 4)
        self.anim = Animation(frames, fps=6)

        self.width, self.height = frames[0].get_size()
        self.pos_x = float(spawn_x)
        self.pos_y = float(spawn_y)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (int(self.pos_x), int(self.pos_y))

        self.state = "idle"
        self.bob_timer = random.uniform(0, 10)   # random phase so they don't bob in sync
        self.facing_right = True

        # randomized per-moth so a group doesn't move identically
        self.chase_speed = random.uniform(110, 170)
        self.bob_amplitude = random.uniform(4, 9)
        self.bob_frequency = random.uniform(4, 8)

    def update(self, dt, player_rect):
        dx = player_rect.centerx - self.pos_x
        dy = player_rect.centery - self.pos_y
        distance = math.hypot(dx, dy)

        if self.state == "idle" and distance <= self.DETECTION_RANGE:
            self.state = "chasing"
        elif self.state == "chasing" and distance >= self.GIVE_UP_RANGE:
            self.state = "idle"
            self.pos_x, self.pos_y = float(self.spawn_x), float(self.spawn_y)
            self.rect.center = (int(self.pos_x), int(self.pos_y))
            return

        if self.state == "chasing":
            if distance > 0:
                self.pos_x += (dx / distance) * self.chase_speed * dt
                self.pos_y += (dy / distance) * self.chase_speed * dt
                self.facing_right = dx >= 0

            self.bob_timer += dt
            bob_offset = math.sin(self.bob_timer * self.bob_frequency) * self.bob_amplitude

            self.rect.centerx = int(self.pos_x)
            self.rect.centery = int(self.pos_y + bob_offset)

            self.anim.update(dt)

    def is_active(self):
        return self.state == "chasing"

    def draw(self, screen, camera):
        if not self.is_active():
            return

        frame = self.anim.get_frame()
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)

        draw_rect = frame.get_rect(center=camera.apply(self.rect).center)
        screen.blit(frame, draw_rect.topleft)