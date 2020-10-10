from Utilities.Grid import pygame
from Utilities.Constants import SIZE
from Utilities.Controller import Controller


def main():
    pygame.init()
    window = pygame.display.set_mode(size=SIZE, flags=pygame.FULLSCREEN)
    Controller(window=window)
    pygame.quit()


if __name__ == '__main__':
    main()
