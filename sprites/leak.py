import pygame

from utils.animation import Animation
from utils.spritesheet import load_frames


class LeakTile:
    ANIM_FPS = 4
    LOOP_DELAY = 1
    SPAWN_FRAME_INDEX = 2   # on 3rd frame droplet spawns

    def __init__(self, x, y):
        frames = load_frames("assets/images/environment/leak-tile.png", 4)
        self.anim = Animation(frames, fps=self.ANIM_FPS)

        self.waiting = False
        self.wait_timer = 0
        self._spawn_pending = False

        self.rect = pygame.Rect(x, y, frames[0].get_width(), frames[0].get_height())

    def update(self, dt):
        if self.waiting:
            self.wait_timer += dt
            if self.wait_timer >= self.LOOP_DELAY:
                self.waiting = False
                self.wait_timer = 0
                self.anim.current_frame = 0
                self.anim.timer = 0
            return

        previous_frame = self.anim.current_frame
        self.anim.update(dt)

        if self.anim.current_frame == self.SPAWN_FRAME_INDEX and previous_frame != self.SPAWN_FRAME_INDEX:
            self._spawn_pending = True

        if self.anim.current_frame == 0 and self.anim.timer < dt:
            self.waiting = True

    def consume_spawn_trigger(self):
        if self._spawn_pending:
            self._spawn_pending = False
            return True
        return False

    def draw(self, screen, camera):
        frame = self.anim.get_frame()
        screen.blit(frame, camera.apply(self.rect).topleft)