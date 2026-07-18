class SceneManager:
    
    def __init__(self):
        self.scenes = {}
        self.current = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
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