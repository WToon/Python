import pygame, sys
from pygame.locals import *

# init
pygame.init()
FPS = 30
FPSCLOCK = pygame.time.Clock()


# window setup
DISPLAYSURF = pygame.display.set_mode((400, 400), 0, 32)
pygame.display.set_caption("Study")

# color setup
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DISPLAYSURF.fill(WHITE)
pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
pygame.draw.rect(DISPLAYSURF, RED, (10, 20, 30, 5))


# game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    FPSCLOCK.tick(FPS)