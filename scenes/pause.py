import pygame
import config as cfg
from scenes.scene import Scene

class PauseScene(Scene):
    uses_virtual_canvas = False

    def __init__(self, manager):
        super().__init__(manager)
        font_path = "assets/fonts/MysteryQuest-Regular.ttf"
        self.title_font = pygame.font.Font(font_path, 48)
        self.option_font = pygame.font.Font(font_path, 32)

        self.game_surface = pygame.Surface((cfg.VIRTUAL_WIDTH, cfg.VIRTUAL_HEIGHT))

        # menu options as (label, action) pairs - selected_index tracks which is highlighted
        self.options = ["Resume", "Restart", "Quit", "Options", "Credits"]
        self.selected_index = 0

    def on_enter(self):
        self.selected_index = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self.manager.set_scene("game")  # ESC still quick-resumes, same as before

        elif event.key in (pygame.K_UP, pygame.K_w):
            self.selected_index = (self.selected_index - 1) % len(self.options)

        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index = (self.selected_index + 1) % len(self.options)

        elif event.key == pygame.K_RETURN:
            self._activate_selected()

    def _activate_selected(self):
        choice = self.options[self.selected_index]
        if choice == "Resume":
            self.manager.set_scene("game")
        elif choice == "Restart":
            game_scene = self.manager.scenes["game"]
            game_scene.respawn()
            game_scene.won = False
            self.manager.set_scene("game")
        elif choice == "Quit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif choice == "Options":
            self.manager.set_scene("options")
        elif choice == "Credits":
            self.manager.set_scene("credits")

    def update(self, dt):
        pass

    def draw(self, screen):
        screen_width, screen_height = screen.get_size()

        game_scene = self.manager.scenes["game"]
        game_scene.draw(self.game_surface)

        scale = max(screen_width / cfg.VIRTUAL_WIDTH, screen_height / cfg.VIRTUAL_HEIGHT)
        scaled_size = (int(cfg.VIRTUAL_WIDTH * scale), int(cfg.VIRTUAL_HEIGHT * scale))
        offset_x = (screen_width - scaled_size[0]) // 2
        offset_y = (screen_height - scaled_size[1]) // 2

        scaled_game = pygame.transform.scale(self.game_surface, scaled_size)

        blur_amount = 8
        small_size = (max(1, scaled_size[0] // blur_amount), max(1, scaled_size[1] // blur_amount))
        blurred = pygame.transform.smoothscale(scaled_game, small_size)
        blurred = pygame.transform.smoothscale(blurred, scaled_size)
        screen.blit(blurred, (offset_x, offset_y))

        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # --- render everything first, without drawing yet, so we can measure total height ---
        title_surf = self.title_font.render("PAUSED", True, (255, 230, 140))

        option_surfs = []
        for i, option in enumerate(self.options):
            is_selected = (i == self.selected_index)
            color = (255, 230, 140) if is_selected else (180, 180, 180)
            label = f"> {option}" if is_selected else option
            option_surfs.append(self.option_font.render(label, True, color))

        # spacing between elements - tune to taste
        title_to_options_gap = 30
        option_line_height = 50

        # total height of the whole "block": title + gap + (each option's own line height)
        total_height = title_surf.get_height() + title_to_options_gap + option_line_height * len(option_surfs)

        # top of the block, positioned so the WHOLE block is centered vertically
        block_top = screen_height // 2 - total_height // 2

        # draw title at the top of the block
        title_rect = title_surf.get_rect(centerx=screen_width // 2, top=block_top)
        screen.blit(title_surf, title_rect.topleft)

        # draw each option below it, stacking downward by option_line_height each time
        options_start_y = title_rect.bottom + title_to_options_gap
        for i, option_surf in enumerate(option_surfs):
            option_rect = option_surf.get_rect(
                centerx=screen_width // 2,
                top=options_start_y + i * option_line_height
            )
            screen.blit(option_surf, option_rect.topleft)