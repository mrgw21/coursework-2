import pygame
from levels.level1 import Level1

def main():
    pygame.init()
    # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Immune System Game")
    level1 = Level1(screen)
    level1.run()
    pygame.quit()

if __name__ == "__main__":
    main()