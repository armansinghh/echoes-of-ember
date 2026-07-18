import pygame
import config as cfg

def main():
    pygame.init()

    screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
    pygame.display.set_caption("Echoes of Ember")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        screen.fill((0, 255, 255))
        pygame.display.flip()
        clock.tick(cfg.FPS)

    pygame.quit()

if __name__ == "__main__": main()
