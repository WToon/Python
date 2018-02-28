import pygame, sys, random, numpy
from pygame.locals import *

# window variables
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
FPS = 60
VEL = 3

# color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (102, 103, 41)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(GREEN)
    pygame.display.set_caption('Snake')

    # starting position, velocity, snake and apple
    x_position = int(WINDOWWIDTH/2)
    y_position = int(WINDOWHEIGHT/2)
    x_velocity = 0
    y_velocity = 0
    snake = [(x_position, y_position)]
    apples = [(random.randint(10, WINDOWWIDTH), random.randint(10, WINDOWHEIGHT))]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP and y_velocity == 0:
                    x_velocity = 0
                    y_velocity = -VEL
                elif event.key == K_DOWN and y_velocity == 0:
                    x_velocity = 0
                    y_velocity = VEL
                elif event.key == K_RIGHT and x_velocity == 0:
                    x_velocity = VEL
                    y_velocity = 0
                elif event.key == K_LEFT and x_velocity == 0:
                    x_velocity = -VEL
                    y_velocity = 0


        snake, apples = updateGameObjects(snake, apples, x_velocity, y_velocity)
        drawGameObjects(snake, apples)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawGameObjects(snake, apples):
    DISPLAYSURF.fill(GREEN)
    drawSnake(snake)
    drawApples(apples)


def drawSnake(snake):
    for limb in snake:
        pygame.draw.circle(DISPLAYSURF, DARK_GREEN, limb, 5)


def drawApples(apples):
    for apple in apples:
        pygame.draw.circle(DISPLAYSURF, RED, apple, 10)


def updateGameObjects(snake, apples, xvel, yvel):
    snake = updateSnake(snake, xvel, yvel)
    if touchesTail(snake):
        gameOver()
    if touchesApple(snake, apples[0]):
        del(apples[0])
        snake.append((snake[len(snake)-1][0]+numpy.sign(xvel)*3, snake[len(snake)-1][1]+numpy.sign(yvel)*3))
        apples.append((random.randint(10, WINDOWWIDTH), random.randint(10, WINDOWHEIGHT)))
    return snake, apples


def updateSnake(snake, xvel, yvel):
    evolvedSnake = []
    for i in range(len(snake)):
        if i == 0:
            evolvedSnake.append((snake[0][0]+xvel, snake[0][1]+yvel))
        else:
            evolvedSnake.append(snake[i-1])
    return evolvedSnake


def touchesTail(snake):
    for limb in snake:
        dist = distance(limb, snake[0])
        if limb == snake[0]:
            pass
        elif (dist < 2):
            return True
    return False


def touchesApple(snake, apple):
    for limb in snake:
        if (distance(limb, apple) < 10):
            return True
    return False


def gameOver():
    pygame.quit()
    sys.exit()

def distance(p0, p1):
    return numpy.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

if __name__ == '__main__':
    main()