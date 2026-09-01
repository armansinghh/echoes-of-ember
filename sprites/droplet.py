import pygame

from utils.animation import Animation
from utils.spritesheet import load_frames


class Droplet:
    FALL_SPEED = 100
    START_DURATION = 0.3
    FRAME3_DURATION = 0.15
    FRAME4_DURATION = 0.15
    FRAME5_DURATION = 0.15

    # collision box dimensions
    HITBOX_WIDTH = 18
    HITBOX_HEIGHT = 24

    def __init__(self, x, top_y, floor_y):
        self.spawn_x = x
        self.top_y = top_y
        self.floor_y = floor_y

        frames = load_frames("assets/images/hazards/droplet.png", 6)

        self.start_frame = frames[0]
        self.fall_anim = Animation([frames[1]], fps=1)
        self.splash_frames = frames[2:5]
        self.residue_frame = frames[5]
        self.splash_durations = [self.FRAME3_DURATION, self.FRAME4_DURATION, self.FRAME5_DURATION]
        self._splash_frame_index = 0

        self.width, self.height = self.start_frame.get_size()

        self.state = "idle"   # idle/start/falling/splashing
        self.timer = 0
        self.pos_y = top_y

        self.rect = pygame.Rect(0, 0, self.HITBOX_WIDTH, self.HITBOX_HEIGHT)
        self.rect.centerx = x
        self.rect.y = int(self.pos_y)

        self.residue_active = False

    def start_new_drop(self):
        if self.state != "idle":
            return
        self.state = "start"
        self.timer = 0
        self.pos_y = self.top_y
        self.rect.centerx = self.spawn_x
        self.rect.y = int(self.pos_y)

    def update(self, dt):
        if self.state == "start":
            self.timer += dt
            if self.timer >= self.START_DURATION:
                self.state = "falling"
                self.timer = 0

        elif self.state == "falling":
            self.timer += dt
            self.pos_y += self.FALL_SPEED * dt
            self.rect.centerx = self.spawn_x
            self.rect.y = int(self.pos_y)

            if self.pos_y >= self.floor_y:
                self.state = "splashing"
                self.timer = 0

        elif self.state == "splashing":
            self.timer += dt
            elapsed = 0
            for i, duration in enumerate(self.splash_durations):
                elapsed += duration
                if self.timer < elapsed:
                    self._splash_frame_index = i
                    break
            else:
                self._splash_frame_index = len(self.splash_durations) - 1

            if self.timer >= sum(self.splash_durations):
                self.residue_active = True
                self.state = "idle"
                self.timer = 0

    def is_hazardous(self):
        return self.state in ("start", "falling")

    def draw(self, screen, camera):
        if self.residue_active:
            splash_rect = pygame.Rect(self.spawn_x - self.width // 2, self.floor_y, self.width, self.height)
            screen.blit(self.residue_frame, camera.apply(splash_rect).topleft)

        if self.state == "start":
            draw_rect = self.start_frame.get_rect(center=camera.apply(self.rect).center)
            screen.blit(self.start_frame, draw_rect.topleft)
        elif self.state == "falling":
            frame = self.fall_anim.get_frame()
            draw_rect = frame.get_rect(center=camera.apply(self.rect).center)
            screen.blit(frame, draw_rect.topleft)
        elif self.state == "splashing":
            frame = self.splash_frames[self._splash_frame_index]
            splash_rect = pygame.Rect(self.spawn_x - self.width // 2, self.floor_y, self.width, self.height)
            screen.blit(frame, camera.apply(splash_rect).topleft)