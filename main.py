# importujemy biblioteki i funkcje, które będą potrzebne
import sys
import pygame
from display import menu

# pygame initialization
pygame.init()

# loop of game
if __name__ == '__main__':
    menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
