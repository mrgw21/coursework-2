import pygame
from levels.level1 import Level1
from introductions.intro1 import Intro1
import os

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Immune System Game")

    pdf_images = load_pdf_images("assets/introduction-materials/")
    intro1 = Intro1(screen, pdf_images)
    intro1.run()

    level1 = Level1(screen)
    level1.run()

    pygame.quit()

def load_pdf_images(folder):
    images = []
    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".jpg"):
            image = pygame.image.load(os.path.join(folder, filename)).convert()
            images.append(image)
    return images

if __name__ == "__main__":
    main()