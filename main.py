from Utilities.Grid import pygame
from Utilities.Constants import SIZE
from Utilities.Controller import Controller, os


def main():
    pygame.init()
    # window = pygame.display.set_mode(size=SIZE)
    window = pygame.display.set_mode(size=SIZE, flags=pygame.FULLSCREEN)
    icon = pygame.image.load(os.path.join('Resources', 'path-icon.png'))
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Pathfinding Visualizer", "Pathfinding Visualizer")
    Controller(window=window)
    pygame.quit()


if __name__ == '__main__':
    main()
