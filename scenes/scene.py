class Scene:
    """
    base class for all game scenes
    child classes should override these methods as needed.
    """
    uses_virtual_canvas = True

    def __init__(self, manager):
        # keep a reference to the manager so scenes can trigger state changes
        # (e.g, calling self.manager.set_scene("pause"))
        self.manager = manager
    def on_enter(self):
        # called every time this scene becomes the active scene; override as needed        
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):
        pass