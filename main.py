import pygame
import config as cfg
from scenes.manager import SceneManager
from scenes.menu import MenuScene
from scenes.game import GameScene
from scenes.pause import PauseScene

def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT = screen.get_size()

    pygame.display.set_caption("Echoes of Ember")
    clock = pygame.time.Clock()

    # Everything draws to this fixed 320x180 canvas first
    game_surface = pygame.Surface((cfg.VIRTUAL_WIDTH, cfg.VIRTUAL_HEIGHT))

    # Scale to fill the entire viewport without leaving black bars
    scale_x = cfg.SCREEN_WIDTH / cfg.VIRTUAL_WIDTH
    scale_y = cfg.SCREEN_HEIGHT / cfg.VIRTUAL_HEIGHT
    scale = max(scale_x, scale_y)
    scaled_size = (int(cfg.VIRTUAL_WIDTH * scale), int(cfg.VIRTUAL_HEIGHT * scale))
    offset_x = (cfg.SCREEN_WIDTH - scaled_size[0]) // 2
    offset_y = (cfg.SCREEN_HEIGHT - scaled_size[1]) // 2

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            manager.handle_event(event)

        manager.update(dt)

        manager.draw(game_surface)

        # scale up with no smoothing -> keeps the crisp pixel-art look
        scaled = pygame.transform.scale(game_surface, scaled_size)
        screen.blit(scaled, (offset_x, offset_y))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()