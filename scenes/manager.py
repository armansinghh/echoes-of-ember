class SceneManager:
    """
    manages the game states (scenes) and delegates core loop methods
    (events, updates, drawing) to the currently active scene.
    """
    def __init__(self):
        self.scenes = {}
        self.current = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        # we let this raise a KeyError if the name doesn't exist
        # so we catch typos in scene names immediately during development
        self.current = self.scenes[name]

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt):
        if self.current:
            self.current.update(dt)

    def draw(self, screen):
        if self.current:
            self.current.draw(screen)