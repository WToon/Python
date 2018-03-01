import pygame, sys, random, numpy
from pygame.locals import *

# window variables
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
TILESIZE = int(WINDOWWIDTH/16)
FPS = 60
VEL = 6

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
    GROWTHSPEED = 50
    snake = [(x_position, y_position)]
    apple = (random.randint(10, WINDOWWIDTH), random.randint(10, WINDOWHEIGHT))

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


        snake, apple, x_velocity, y_velocity = updateGameObjects(snake, apple, x_velocity, y_velocity, GROWTHSPEED)
        drawFloor()
        drawGameObjects(snake, apple)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawGameObjects(snake, apple):
#    DISPLAYSURF.fill(GREEN)
    drawSnake(snake)
    drawApple(apple)


def drawSnake(snake):
    i = 0
    for limb in snake:
        if limb == snake[0]:
            pygame.draw.circle(DISPLAYSURF, BLUE, limb, 7)
        else:
            if (i%2 == 0):
                i+=1
                pygame.draw.circle(DISPLAYSURF, DARK_GREEN, limb, 5)
            else:
                i+=1
                pygame.draw.circle(DISPLAYSURF, WHITE, limb, 5)


def drawApple(apple):
    pygame.draw.circle(DISPLAYSURF, RED, apple, 10)


def updateGameObjects(snake, apple, xvel, yvel, GROWTHSPEED):
    snake = updateSnake(snake, xvel, yvel)
    if touchesTail(snake):
        xvel = 0
        yvel = 0
        print('Game over, final score: ' + str(len(snake)) + ', ' + str(GROWTHSPEED))
        snake = [snake[0]]
    elif touchesApple(snake, apple):
        for i in range(1, GROWTHSPEED):
            snake.append((-100, -100))
        apple = (random.randint(10, WINDOWWIDTH-10), random.randint(10, WINDOWHEIGHT-10))
    return snake, apple, xvel, yvel


def drawFloor():
    DISPLAYSURF.fill(GREEN)


def updateSnake(snake, xvel, yvel):
    evolvedSnake = []
    for i in range(len(snake)):
        if i == 0:
            evolvedSnake.append((snake[0][0]+xvel, snake[0][1]+yvel))
        else:
            evolvedSnake.append(snake[i-1])
    return evolvedSnake


def touchesTail(snake):
    for i in range(1, len(snake)-1):
        if (distance(snake[i], snake[0]) < 5):
            return True
    return False


def touchesApple(snake, apple):
    for limb in snake:
        if (distance(limb, apple) < 10):
            return True
    return False






def distance(p0, p1):
    return numpy.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

if __name__ == '__main__':
    main()