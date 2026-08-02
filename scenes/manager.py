class SceneManager:
    """
    manages the game states (scenes) and delegates core loop methods
    (events, updates, drawing) to the currently active scene.
    """
    def __init__(self):
        self.scenes = {}
        self.current = None
        self.current_name = None
        self.previous_name = None

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        # remember where we're coming FROM, before switching, so scenes like
        # Options/Credits can send the player back to whichever screen opened them
        if self.current_name is not None:
            self.previous_name = self.current_name

        self.current_name = name
        self.current = self.scenes[name]  # raise KeyError on typos, same as before
        self.current.on_enter()

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt):
        if self.current:
            self.current.update(dt)

    def draw(self, screen):
        if self.current:
            self.current.draw(screen)