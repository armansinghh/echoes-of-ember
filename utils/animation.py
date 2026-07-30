class Animation:
    def __init__(self, frames, fps=8):
        self.frames = frames
        self.frame_duration = 1 / fps  # seconds per frame
        self.timer = 0
        self.current_frame = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_frame(self):
        return self.frames[self.current_frame]