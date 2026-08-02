import pygame
from scenes.scene import Scene


class FadeScene(Scene):
    """
    reusable black fade transition; wraps around any scene-to-scene swap.
    fades the outgoing scene to black, switches the real current scene
    under da hood, then fades the incoming scene back in.
    trigger with manager.transition_to("some_scene") instead of set_scene().
    """
    uses_virtual_canvas = False
    def __init__(self, manager):
        super().__init__(manager)
        self.from_scene = None
        self.target_name = None
        self.duration = 0.4
        self.timer = 0
        self.state = "idle"  # "idle" | "out" | "in"

    def start(self, from_scene, target_name, duration=0.4):
        self.from_scene = from_scene
        self.target_name = target_name
        self.duration = duration
        self.timer = 0
        self.state = "out"

    def handle_event(self, event):
        pass  # swallow input mid-transition so it can't leak to either scene

    def update(self, dt):
        if self.state == "idle":
            return

        self.timer += dt

        if self.state == "out" and self.timer >= self.duration:
            # fully black now - swap the real scene underneath us
            self.manager.set_scene(self.target_name)
            self.timer = 0
            self.state = "in"

        elif self.state == "in" and self.timer >= self.duration:
            # done - hand control back to the target scene for good
            self.state = "idle"
            self.manager.current = self.manager.scenes[self.target_name]

    def draw(self, screen):
        # draw whichever scene belongs to this half of the transition,
        # frozen (not updated) underneath the fade overlay
        if self.state == "out" and self.from_scene:
            self.from_scene.draw(screen)
        elif self.state == "in":
            self.manager.scenes[self.target_name].draw(screen)

        alpha = self._current_alpha()
        if alpha > 0:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            screen.blit(overlay, (0, 0))

    def _current_alpha(self):
        progress = min(1.0, self.timer / self.duration) if self.duration > 0 else 1.0
        if self.state == "out":
            return int(progress * 255)
        elif self.state == "in":
            return int((1 - progress) * 255)
        return 0