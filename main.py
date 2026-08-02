import pygame

import config as cfg
from scenes.manager import SceneManager
from scenes.menu import MenuScene
from scenes.game import GameScene
from scenes.pause import PauseScene
from scenes.options import OptionsScene
from scenes.credits import CreditsScene


def main():
    pygame.init()

    # initialize display and get the monitor res
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT = screen.get_size()
    pygame.display.set_caption("Echoes of Ember")

    clock = pygame.time.Clock()

    # all stuff draws to this virtual canvas first before getting scaled up to the monitor
    game_surface = pygame.Surface((cfg.VIRTUAL_WIDTH, cfg.VIRTUAL_HEIGHT))

    # calculate scaling to fill the entire viewport without black bars
    # we use max() so it covers the whole screen (this crops edges if aspect ratios differ)
    scale_x = cfg.SCREEN_WIDTH / cfg.VIRTUAL_WIDTH
    scale_y = cfg.SCREEN_HEIGHT / cfg.VIRTUAL_HEIGHT
    scale = max(scale_x, scale_y)
    
    scaled_size = (int(cfg.VIRTUAL_WIDTH * scale), int(cfg.VIRTUAL_HEIGHT * scale))
    
    # calculate centering offsets so the cropped areas are split evenly on both sides (no crop on 16:9 monitors btw)
    offset_x = (cfg.SCREEN_WIDTH - scaled_size[0]) // 2
    offset_y = (cfg.SCREEN_HEIGHT - scaled_size[1]) // 2

    # set up scene state
    manager = SceneManager()
    manager.add_scene("menu", MenuScene(manager))
    manager.add_scene("game", GameScene(manager))
    manager.add_scene("pause", PauseScene(manager))
    manager.add_scene("options", OptionsScene(manager))
    manager.add_scene("credits", CreditsScene(manager))
    
    manager.set_scene("menu")

    running = True
    while running:
        dt = clock.tick(cfg.FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            manager.handle_event(event)

        manager.update(dt)

        # scenes flagged uses_virtual_canvas=False (menu/pause) skip the pixel-art
        # canvas entirely and draw straight onto the real fullscreen display,
        # so their text renders crisp at native resolution instead of blocky/scaled
        if manager.current.uses_virtual_canvas:
            manager.draw(game_surface)

            # scale up with no smoothing
            scaled = pygame.transform.scale(game_surface, scaled_size)
            screen.blit(scaled, (offset_x, offset_y))
        else:
            screen.fill((0, 0, 0))
            manager.draw(screen)
        
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()