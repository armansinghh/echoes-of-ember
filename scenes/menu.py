import pygame
import config as cfg
from scenes.scene import Scene
from sprites.background import Background, ParallaxLayer


class _MenuCamera:
    def __init__(self):
        self.offset_x = 0


class MenuScene(Scene):
    uses_virtual_canvas = False

    def __init__(self, manager):
        super().__init__(manager)
        font_path = "assets/fonts/MysteryQuest-Regular.ttf"
        self.title_font = pygame.font.Font(font_path, 72)
        self.option_font = pygame.font.Font(font_path, 32)

        self.options = ["Start", "Options", "Credits", "Quit"]
        self.selected_index = 0

        # slow auto-drifting background, since there's no player/camera on this screen
        self.camera = _MenuCamera()
        self.drift_speed = 35

        self.background = Background([
            ParallaxLayer("assets/images/background/sky.png", scroll_factor=0.0),
            ParallaxLayer("assets/images/background/distant-ruins.png", scroll_factor=0.3),
            ParallaxLayer("assets/images/background/mid-ruins.png", scroll_factor=0.6),
        ])

    def on_enter(self):
        self.selected_index = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_UP, pygame.K_w):
            self.selected_index = (self.selected_index - 1) % len(self.options)

        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.selected_index = (self.selected_index + 1) % len(self.options)

        elif event.key == pygame.K_RETURN:
            self._activate_selected()

    def _activate_selected(self):
        choice = self.options[self.selected_index]
        if choice == "Start":
            self.manager.transition_to("level_select")
        elif choice == "Options":
            self.manager.set_scene("options")
        elif choice == "Credits":
            self.manager.set_scene("credits")
        elif choice == "Quit":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt):
        self.camera.offset_x += self.drift_speed * dt

    def draw(self, screen):
            screen_width, screen_height = screen.get_size()

            # render background to its own surface first, so we can blur it
            # before drawing title/options crisply on top
            bg_surface = pygame.Surface((screen_width, screen_height))
            self.background.draw(bg_surface, self.camera)

            blur_amount = 10
            small_size = (max(1, screen_width // blur_amount), max(1, screen_height // blur_amount))
            blurred = pygame.transform.smoothscale(bg_surface, small_size)
            blurred = pygame.transform.smoothscale(blurred, (screen_width, screen_height))

            screen.blit(blurred, (0, 0))

            # dim so the title/options pop against the background
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            title_surf = self.title_font.render("Echoes of Ember", True, (255, 200, 100))

            option_surfs = []
            for i, option in enumerate(self.options):
                is_selected = (i == self.selected_index)
                color = (255, 230, 140) if is_selected else (180, 180, 180)
                label = f"> {option}" if is_selected else option
                option_surfs.append(self.option_font.render(label, True, color))

            title_to_options_gap = 50
            option_line_height = 48

            total_height = title_surf.get_height() + title_to_options_gap + option_line_height * len(option_surfs)
            block_top = screen_height // 2 - total_height // 2

            title_rect = title_surf.get_rect(centerx=screen_width // 2, top=block_top)
            screen.blit(title_surf, title_rect.topleft)

            options_start_y = title_rect.bottom + title_to_options_gap
            for i, option_surf in enumerate(option_surfs):
                option_rect = option_surf.get_rect(
                    centerx=screen_width // 2,
                    top=options_start_y + i * option_line_height
                )
                screen.blit(option_surf, option_rect.topleft)