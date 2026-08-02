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
        # options/credits can send the player back to whichever screen opened them
        if self.current_name is not None:
            self.previous_name = self.current_name

        self.current_name = name
        self.current = self.scenes[name]  # raise KeyError on typos, same as before
        self.current.on_enter()

    def transition_to(self, name, duration=0.6):
        # fades from the current scene into the named scene. requires a
        # "fade" scene to have been registered via add_scene.
        fade_scene = self.scenes["fade"]
        fade_scene.start(self.current, name, duration)
        self.current = fade_scene

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt):
        if self.current:
            self.current.update(dt)

    def draw(self, screen):
        if self.current:
            self.current.draw(screen)