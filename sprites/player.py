import pygame

class Player:
    def __init__(self, x, y):
        self.width = 32
        self.height = 32
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = (255, 200, 80)

        # Movement
        self.vel_x = 0
        self.vel_y = 0
        self.max_speed = 200        # pixels per second, top horizontal speed
        self.acceleration = 1200    # how fast we ramp up to max_speed
        self.friction = 1000        # how fast we slow down when no input
        self.gravity = 800
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
            # Apply friction - push velocity toward 0 without overshooting
            if self.vel_x > 0:
                self.vel_x = max(0, self.vel_x - self.friction * dt)
            elif self.vel_x < 0:
                self.vel_x = min(0, self.vel_x + self.friction * dt)

        # Clamp to max speed so acceleration doesn't build forever
        self.vel_x = max(-self.max_speed, min(self.max_speed, self.vel_x))

        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def update(self, dt, ground_y):
        self.handle_input(dt)

        self.vel_y += self.gravity * dt

        self.rect.x += self.vel_x * dt
        self.rect.y += self.vel_y * dt

        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)