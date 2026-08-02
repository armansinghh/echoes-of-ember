import pygame
import config as cfg
from scenes.scene import Scene

class CreditsScene(Scene):
    uses_virtual_canvas = False

    def __init__(self, manager):
        super().__init__(manager)
        font_path = "assets/fonts/MysteryQuest-Regular.ttf"
        self.title_font = pygame.font.Font(font_path, 48)
        self.hint_font = pygame.font.Font(font_path, 24)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.manager.set_scene("pause")

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((20, 20, 30))
        screen_width, screen_height = screen.get_size()

        title = self.title_font.render("Credits", True, (255, 230, 140))
        hint = self.hint_font.render("Coming soon - press ESC to go back", True, (180, 180, 180))

        title_rect = title.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
        hint_rect = hint.get_rect(center=(screen_width // 2, screen_height // 2 + 40))

        screen.blit(title, title_rect.topleft)
        screen.blit(hint, hint_rect.topleft)