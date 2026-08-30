import pygame

from utils.animation import Animation
from utils.spritesheet import load_frames


class Player:
    """
    THE MAIN CHARACTER; handles input, platformer physics (with separate X/Y 
    collision resolution), and drawing the player sprite
    """
    def __init__(self, x, y):
        # collision box; separate from visual size
        self.width = 32
        self.height = 72
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.pos_x = float(x)
        self.pos_y = float(y)

        # visual sprite size
        sprite_size = (64, 64)
        fire_size = (32, 32)

        # load and scale animation
        ember_frames = load_frames("assets/images/player/ember.png", 4)
        ember_frames = [pygame.transform.scale(f, sprite_size) for f in ember_frames]
        
        fire_frames = load_frames("assets/images/player/fire.png", 4)
        fire_frames = [pygame.transform.scale(f, fire_size) for f in fire_frames]

        self.ember_anim = Animation(ember_frames, fps=8)
        self.fire_anim = Animation(fire_frames, fps=6)

        # offsets to keep the fire positioned exactly on ember's hand
        self.fire_offset_x_right = 20
        self.fire_offset_x_left = -19
        self.fire_offset_y = -12
        
        self.facing_right = True
        self.is_moving = False

        # physics constants
        self.vel_x = 0
        self.vel_y = 0
        self.max_speed = 200
        self.acceleration = 1200
        self.friction = 1000
        self.gravity = 800
        self.jump_strength = -300
        self.on_ground = False

    def reset(self, x, y):
        self.rect.topleft = (x, y)
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.is_moving = False
        self.ember_anim.current_frame = 0
        self.ember_anim.timer = 0
        self.fire_anim.current_frame = 0
        self.fire_anim.timer = 0

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

        # apply friction if the player lets go of the movement keys,
        # we use max/min against 0 to prevent the velocity from overshooting 
        # and causing the player to endlessly vibrate back and forth.
        if not moving:
            if self.vel_x > 0:
                self.vel_x = max(0, self.vel_x - self.friction * dt)
            elif self.vel_x < 0:
                self.vel_x = min(0, self.vel_x + self.friction * dt)

        # clamp horizontal speed so they don't accelerate infinitely
        self.vel_x = max(-self.max_speed, min(self.max_speed, self.vel_x))

        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    def update(self, dt, platforms):
        self.handle_input(dt)
        self.vel_y += self.gravity * dt

        # update X and resolve X collisions first
        # X-axis movement
        self.pos_x += self.vel_x * dt
        self.rect.x = int(self.pos_x)
        self._resolve_collisions(platforms, axis="x")
        self.pos_x = float(self.rect.x)  # sync back in case hitting a wall changed rect.x

        # Y-axis movement
        self.pos_y += self.vel_y * dt
        self.rect.y = int(self.pos_y)
        self.on_ground = False
        self._resolve_collisions(platforms, axis="y")
        self.pos_y = float(self.rect.y)  # sync back in case hitting the floor changed rect.y

        # ember only animates while actually walking; if idle, lock to the first frame
        if self.is_moving:
            self.ember_anim.update(dt)
        else:
            self.ember_anim.current_frame = 0
            self.ember_anim.timer = 0

        # the fire always flickers, even when standing still
        self.fire_anim.update(dt)

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

        # translate the player's world position into screen coordinates via the camera
        screen_rect = camera.apply(self.rect)

        # anchor ember's sprite by midbottom, not topleft
        # this ensures the feet always perfectly touch the floor of the collision box, 
        # even if the visual frame dimensions change.
        ember_draw_rect = ember_frame.get_rect(midbottom=screen_rect.midbottom)
        
        # using inflate(-6, -6) shrinks the rect by 3px on all sides,
        # since blit uses topleft, this acts as a +3px visual offset 
        # to fine-tune the art alignment without changing the physics rect.
        ember_draw_rect = ember_draw_rect.inflate(-6, -6)
        screen.blit(ember_frame, ember_draw_rect.topleft)

        # calculate fire position based on ember's center + directional offsets
        offset_x = self.fire_offset_x_right if self.facing_right else self.fire_offset_x_left
        fire_x = self.rect.centerx + offset_x - fire_frame.get_width() // 2
        fire_y = self.rect.centery + self.fire_offset_y - fire_frame.get_height() // 2
        
        fire_screen_pos = camera.apply(pygame.Rect(fire_x, fire_y, 0, 0)).topleft
        
        # similar inflate trick here (+2px offset) to lock the fire perfectly in place
        fire_draw_rect = fire_frame.get_rect(topleft=fire_screen_pos)
        fire_draw_rect = fire_draw_rect.inflate(-4, -4)
        
        screen.blit(fire_frame, fire_draw_rect.topleft)