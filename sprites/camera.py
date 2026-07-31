import pygame


class Camera:
    """
    2D camera that follows a Ember and keeps it centered
    Also handles translating world coordinates into screen coordinates for drawing
    """
    def __init__(self, screen_width, screen_height, world_width, world_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height
        
        # how far we shifted the viewport from the top left (0,0) of the world
        self.offset_x = 0
        self.offset_y = 0

    def update(self, target_rect):
        # calculate the ideal offset to keep the target center on the screen
        self.offset_x = target_rect.centerx - self.screen_width // 2
        self.offset_y = target_rect.centery - self.screen_height // 2

        # clamp the offsets so the camera never reveals the empty void outside the level boundaries.
        # max(0, ...) prevents panning too far left/up.
        # min(..., bounds) prevents panning too far right/down.
        self.offset_x = max(0, min(self.offset_x, self.world_width - self.screen_width))
        self.offset_y = max(0, min(self.offset_y, self.world_height - self.screen_height))

    def apply(self, rect):
        """
        shifts a world space rectangle into screen space
        call this on any sprite's rect right before blitting it to the screen
        """
        return pygame.Rect(
            rect.x - self.offset_x, 
            rect.y - self.offset_y, 
            rect.width, 
            rect.height
        )