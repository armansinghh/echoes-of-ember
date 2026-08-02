import pygame


class ParallaxLayer:
    """
    scrolling background layer; 
    scales to match the screen height and tiles horizontally to create an infinite loop
    """
    def __init__(self, image_path, scroll_factor, y=0, repeats=None, world_width=None):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width, self.height = self.image.get_size()
        
        # 0 = locked to camera (like the sky), 1 = moves 1:1 with world (foreground)
        self.scroll_factor = scroll_factor  
        self.y = y

        # optional explicit control: how many times this layer's image should
        # tile across the full level width, instead of just using its native aspect ratio.
        # if not given, falls back to the old aspect-ratio-based sizing.
        self.repeats = repeats
        self.world_width = world_width
        
        # cache variables to prevent rescaling the image every single frame
        self.cached_surface = None
        self.cached_height = None

    def _get_surface(self, screen):
        target_height = screen.get_height()
        
        # only recalculate and scale the image if its the first frame OR if the screen size changed
        if self.cached_surface is None or self.cached_height != target_height:

            if self.repeats and self.world_width:
                # explicit mode: fit exactly `repeats` copies across the level width,
                # regardless of the image's native aspect ratio
                new_width = int(self.world_width / self.repeats)
            else:
                # fallback: old behavior, scale width to match height, keep native aspect ratio
                scale_factor = target_height / self.height
                new_width = int(self.width * scale_factor)

            self.cached_surface = pygame.transform.scale(self.image, (new_width, target_height))
            self.cached_height = target_height
            
        return self.cached_surface

    def draw(self, screen, camera):
        layer_image = self._get_surface(screen)
        
        # calculate how far this specific layer should move based on the cameras true position
        offset_x = camera.offset_x * self.scroll_factor
        
        # The modulo operator (%) creates the endless wrap-around effect
        # The negative sign shifts the starting point off-screen to the left so as it moves, the tile seamlessly scrolls into view.
        start_x = -(offset_x % layer_image.get_width())

        x = start_x
        while x < screen.get_width():
            screen.blit(layer_image, (x, self.y))
            x += layer_image.get_width()


class Background:
    """
    container for multiple parallax layers; draws them in order (back to front)
    """
    def __init__(self, layers):
        self.layers = layers

    def draw(self, screen, camera):
        for layer in self.layers:
            layer.draw(screen, camera)