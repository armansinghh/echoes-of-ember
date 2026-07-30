import pygame
from utils.spritesheet import load_frames
from utils.animation import Animation

class Player:
    def __init__(self, x, y):
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # --- Animation setup ---
        ember_frames = load_frames("assets/images/ember.png", 4)
        fire_frames = load_frames("assets/images/fire.png", 4)
        self.ember_anim = Animation(ember_frames, fps=8)
        self.fire_anim = Animation(fire_frames, fps=8)

        # Fire's offset from Ember's center (slightly right and above)
        self.fire_offset_x_right = 21
        self.fire_offset_x_left = -21   # tuned independently, not just -34
        self.fire_offset_y = -34
        self.facing_right = True
        self.is_moving = False

        # --- Movement ---
        self.vel_x = 0
        self.vel_y = 0
        self.max_speed = 200
        self.acceleration = 1200
        self.friction = 1000
        self.gravity = 800
        self.jump_strength = -400
        self.on_ground = False

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x -= self.acceleration * dt
            moving = True
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x += self.acceleration * dt
            moving = True
            self.facing_right = True

        self.is_moving = moving

        if not moving:
            if self.vel_x > 0:
                self.vel_x = max(0, self.vel_x - self.friction * dt)
            elif self.vel_x < 0:
                self.vel_x = min(0, self.vel_x + self.friction * dt)

        self.vel_x = max(-self.max_speed, min(self.max_speed, self.vel_x))

        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def update(self, dt, platforms):
        self.handle_input(dt)
        self.vel_y += self.gravity * dt

        self.rect.x += self.vel_x * dt
        self._resolve_collisions(platforms, axis="x")

        self.rect.y += self.vel_y * dt
        self.on_ground = False
        self._resolve_collisions(platforms, axis="y")

        # Ember only animates while actually moving; otherwise hold frame 0
        if self.is_moving:
            self.ember_anim.update(dt)
        else:
            self.ember_anim.current_frame = 0
            self.ember_anim.timer = 0

        self.fire_anim.update(dt)  # fire always flickers, regardless of movement

    def _resolve_collisions(self, platforms, axis):
        for platform in platforms:
            if not self.rect.colliderect(platform):
                continue
            if axis == "x":
                if self.vel_x > 0:
                    self.rect.right = platform.left
                elif self.vel_x < 0:
                    self.rect.left = platform.right
                self.vel_x = 0
            elif axis == "y":
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0

    def draw(self, screen, camera):
        ember_frame = self.ember_anim.get_frame()
        fire_frame = self.fire_anim.get_frame()

        if not self.facing_right:
            ember_frame = pygame.transform.flip(ember_frame, True, False)

        screen_rect = camera.apply(self.rect)

        # Anchor Ember's sprite by bottom-center, not top-left,
        # so feet line up with the collision rect regardless of art size
        ember_draw_rect = ember_frame.get_rect(midbottom=screen_rect.midbottom)
        screen.blit(ember_frame, ember_draw_rect.topleft)

        # Fire position: Ember's center + offset, separate offsets per facing direction
        offset_x = self.fire_offset_x_right if self.facing_right else self.fire_offset_x_left
        fire_x = self.rect.centerx + offset_x - fire_frame.get_width() // 2
        fire_y = self.rect.centery + self.fire_offset_y - fire_frame.get_height() // 2
        fire_screen_pos = camera.apply(pygame.Rect(fire_x, fire_y, 0, 0)).topleft
        screen.blit(fire_frame, fire_screen_pos)