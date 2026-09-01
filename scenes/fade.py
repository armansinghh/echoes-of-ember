import pygame

import config as cfg
from scenes.scene import Scene


class FadeScene(Scene):
    """
    reusable black fade transition; usable around any scene to scene swap
    fades the outgoing scene to black, switches the real current scene
    then fades the incoming scene back in
    trigger with manager.transition_to("some_scene") instead of set_scene().
    """
    uses_virtual_canvas = False

    def __init__(self, manager):
        super().__init__(manager)
        self.from_scene = None
        self.target_name = None
        self.duration = 0.4
        self.timer = 0
        self.state = "idle"  # idle/out/in
        
        self.game_surface = pygame.Surface((cfg.VIRTUAL_WIDTH, cfg.VIRTUAL_HEIGHT))

    def start(self, from_scene, target_name, duration=0.4):
        self.from_scene = from_scene
        self.target_name = target_name
        self.duration = duration
        self.timer = 0
        self.state = "out"

    def handle_event(self, event):
        pass

    def update(self, dt):
        if self.state == "idle":
            return

        self.timer += dt

        if self.state == "out" and self.timer >= self.duration:
            self.manager.set_scene(self.target_name)
            self.timer = 0
            self.state = "in"

        elif self.state == "in" and self.timer >= self.duration:
            self.state = "idle"
            self.manager.current = self.manager.scenes[self.target_name]

    def _draw_scene(self, scene, screen):
        if getattr(scene, "uses_virtual_canvas", True):
            scene.draw(self.game_surface)

            screen_width, screen_height = screen.get_size()
            scale = max(screen_width / cfg.VIRTUAL_WIDTH, screen_height / cfg.VIRTUAL_HEIGHT)
            scaled_size = (int(cfg.VIRTUAL_WIDTH * scale), int(cfg.VIRTUAL_HEIGHT * scale))
            offset_x = (screen_width - scaled_size[0]) // 2
            offset_y = (screen_height - scaled_size[1]) // 2

            scaled = pygame.transform.scale(self.game_surface, scaled_size)
            screen.blit(scaled, (offset_x, offset_y))
        else:
            scene.draw(screen)

    def draw(self, screen):
        if self.state == "out" and self.from_scene:
            self._draw_scene(self.from_scene, screen)
        elif self.state == "in":
            self._draw_scene(self.manager.scenes[self.target_name], screen)

        alpha = self._current_alpha()
        if alpha > 0:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            screen.blit(overlay, (0, 0))

    def _current_alpha(self):
        progress = min(1.0, self.timer / self.duration) if self.duration > 0 else 1.0
        eased = progress * progress * (3 - 2 * progress)

        if self.state == "out":
            return int(eased * 255)
        elif self.state == "in":
            return int((1 - eased) * 255)
        return 0