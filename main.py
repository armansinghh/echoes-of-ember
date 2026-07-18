import pygame
import config as cfg
from scenes.manager import SceneManager
from scenes.menu import MenuScene
from scenes.game import GameScene
from scenes.pause import PauseScene

def main():
    pygame.init()

    screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
    pygame.display.set_caption("Echoes of Ember")
    clock = pygame.time.Clock()

    manager = SceneManager()
    manager.add_scene("menu", MenuScene(manager))
    manager.add_scene("game", GameScene(manager))
    manager.add_scene("pause", PauseScene(manager))
    manager.set_scene("menu")

    running = True
    while running:
        dt = clock.tick(cfg.FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.handle_event(event)

        manager.update(dt)

        manager.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()