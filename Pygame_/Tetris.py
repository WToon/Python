import pygame, sys, random
from pygame.locals import *

# window variables
WINDOWHEIGHT = 800
WINDOWWIDTH = 600
FPS = 60

# colors
BGCOLOR = (35, 56, 79)
SIDECOLOR = (20, 50, 80)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY_1 = (112, 112, 112)
GREY_2 = (80, 80, 80)
RED = (255, 0, 0)

# block types
BLOCKS = {'I': [(0, -1), (0, 0), (0, 1)],
          'J': [(0, -1), (0, 0), (0, 1), (-1, 1)],
          'L': [(0, -1), (0, 0), (0, 1), (1, 1)],
          'O': [(0, 0), (-1, 0), (-1, 1), (0, 1)],
          'S': [(0, 0), (1, 0), (0, 1), (-1, 1)],
          'Z': [(0, 0), (-1, 0), (0, 1), (1, 1)],
          'T': [(0, 0), (-1, 1), (0, 1), (1, 1)]}

# functions and methods
def main():
    init()
    score = 0
    active_block = BLOCKS.get('J')
    block_center = (columnsize*4, columnsize*2)
    blocks = []
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    active_block = rotate(active_block)
                elif event.key == K_DOWN:
                    block_center = move_down(block_center)
                elif event.key == K_LEFT:
                    block_center = move_left(block_center)
                elif event.key == K_RIGHT:
                    block_center = move_right(block_center)
        score = random.randint(0, 100)
        BLOCKBAR = drawBlockBar(nbColumns=10)
        draw_active_block(block_center, active_block)
        drawScreen(score)
        FPSCLOCK.tick(FPS)
        pygame.display.update()


def rotate(block):
    newpos = (0, 0)
    for i in range(0, len(block)):
        pos = block[i]
        if pos == (-1, -1):
            newpos = (-1, 1)
        elif pos == (-1, 1):
            newpos = (1, 1)
        elif pos == (1, -1):
            newpos = (-1, -1)
        elif pos == (1, 1):
            newpos = (1, -1)
        elif pos == (-1, 0):
            newpos = (0, 1)
        elif pos == (0, 1):
            newpos = (1, 0)
        elif pos == (1, 0):
            newpos = (0, -1)
        elif pos == (0, -1):
            newpos = (-1, 0)
        block[i] = newpos
    return block


def move_down(center):
    res = (center[0], center[1]+columnsize)
    return res


def move_left(center):
    res = (center[0] - columnsize, center[1])
    return res


def move_right(center):
    res = (center[0]+columnsize, center[1])
    return res


def init():
    global FPSCLOCK, DISPLAYSURF, SIDEBAR, BLOCKBAR, myFont
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Tetris')

    myFont = pygame.font.SysFont("Arial", 20, True)

    # Surfaces init
    SIDEBAR = pygame.Surface((WINDOWWIDTH / 4, WINDOWHEIGHT))
    BLOCKBAR = drawBlockBar(nbColumns=10)


def updateSideBar(score):
    SIDEBAR.fill(SIDECOLOR)
    SIDEBAR.blit(myFont.render("Score: ", 1, BLACK), (25, 40))
    scoreDisplay = myFont.render(str(score), 1, BLACK)
    SIDEBAR.blit(scoreDisplay, (105, 40))


def drawScreen(score):
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(BLOCKBAR, (WINDOWWIDTH/8, WINDOWHEIGHT/20))
    updateSideBar(score)
    DISPLAYSURF.blit(SIDEBAR, (WINDOWWIDTH*3/4, 0))


def draw_active_block(center, block):
    for square in block:
        print(square)
        pygame.draw.rect(BLOCKBAR, RED, (center[0]+square[0]*columnsize, center[1]+square[1]*columnsize, columnsize, columnsize))


def drawBlockBar(nbColumns):
    global columnsize
    wWidth = WINDOWWIDTH/2
    wHeight = WINDOWHEIGHT*0.9
    surface = pygame.Surface((wWidth, wHeight))
    columnsize = wWidth/nbColumns
    surface.fill(GREY_1)
    for i in range(0, nbColumns, 2):
        pygame.draw.rect(surface, GREY_2, (columnsize*i, 0, columnsize, wHeight))
    return surface


if __name__ == '__main__':
    main()