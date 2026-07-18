import pygame

class Player:
    def __init__(self, x, y):
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (255, 200, 80)

        self.vel_x = 0
        self.vel_y = 0
        self.max_speed = 200
        self.acceleration = 1200
        self.friction = 1000
        self.gravity = 900
        self.jump_strength = -400
        self.on_ground = False

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x -= self.acceleration * dt
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x += self.acceleration * dt
            moving = True

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

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)