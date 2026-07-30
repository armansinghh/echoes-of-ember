import pygame

class ParallaxLayer:
    def __init__(self, image_path, scroll_factor, y=0):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width, self.height = self.image.get_size()
        self.scroll_factor = scroll_factor  # 0 = locked to camera, 1 = moves with world
        self.y = y
        self.cached_surface = None
        self.cached_size = None

    def _get_surface(self, screen):
        size = screen.get_size()
        if self.cached_surface is None or self.cached_size != size:
            self.cached_surface = pygame.transform.scale(self.image, size)
            self.cached_size = size
        return self.cached_surface

    def draw(self, screen, camera):
        layer_image = self._get_surface(screen)
        offset_x = camera.offset_x * self.scroll_factor
        start_x = -(offset_x % layer_image.get_width())

        x = start_x
        while x < screen.get_width():
            screen.blit(layer_image, (x, self.y))
            x += layer_image.get_width()


class Background:
    def __init__(self, layers):
        """layers: list of ParallaxLayer, ordered back-to-front"""
        self.layers = layers

    def draw(self, screen, camera):
        for layer in self.layers:
            layer.draw(screen, camera)
