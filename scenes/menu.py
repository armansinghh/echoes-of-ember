import pygame
import config as cfg
from scenes.scene import Scene

class MenuScene(Scene):
    # draws straight to the real fullscreen display, not the small pixel canvas -
    # keeps the Mystery Quest title text crisp instead of blocky/scaled
    uses_virtual_canvas = False

    def __init__(self, manager):
        super().__init__(manager)
        font_path = "assets/fonts/MysteryQuest-Regular.ttf"
        self.title_font = pygame.font.Font(font_path, 72)
        self.hint_font = pygame.font.Font(font_path, 28)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.manager.set_scene("game")

    def update(self, dt):
        pass  # nothing to animate yet

    def draw(self, screen):
        screen.fill((20, 20, 30))

        # since this scene draws at real screen size now (not VIRTUAL_WIDTH/HEIGHT),
        # get the actual screen dimensions directly from the surface we were given
        screen_width, screen_height = screen.get_size()

        title = self.title_font.render("Echoes of the Ember", True, (255, 200, 100))
        hint = self.hint_font.render("Press ENTER to start", True, (200, 200, 200))

        title_rect = title.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        hint_rect = hint.get_rect(center=(screen_width // 2, screen_height // 2 + 40))

        screen.blit(title, title_rect.topleft)
        screen.blit(hint, hint_rect.topleft)