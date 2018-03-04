import os
import pygame
import sys
import random
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

gridSize = 61
WINDOWWIDTH = WINDOWHEIGHT = gridSize*12
TILESIZE = int(WINDOWWIDTH/gridSize)
FPS = 20
GROWTHSPEED = 15

directions = {None: (0, 0), 'NORTH': (0, -1), 'EAST': (1, 0), 'SOUTH': (0, 1), 'WEST': (-1, 0)}


def main():

    clock, bg, snake, food = init()

    direction = None
    game_over = False
    growth = 0

    while True:

        if game_over:
            pygame.event.clear()

        t_direction = direction
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP and direction != 'SOUTH':
                    t_direction = 'NORTH'
                elif event.key == K_RIGHT and direction != 'WEST':
                    t_direction = 'EAST'
                elif event.key == K_LEFT and direction != 'EAST':
                    t_direction = 'WEST'
                elif event.key == K_DOWN and direction != 'NORTH':
                    t_direction = 'SOUTH'
        direction = t_direction

        snake, food, growth, game_over = update_game_state(snake, food, direction, growth)

        if game_over:
            snake, food, direction, growth = reset()

        draw_graphics(bg, snake, food)
        clock.tick(FPS)


def init():
    pygame.init()
    global surface
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Snake')
    bg = generate_raster()
    print("Initialized")
    return clock, bg, [((gridSize-1)/2, (gridSize-1)/2)], (random.randint(0, gridSize-1), random.randint(0, gridSize-1))


def generate_raster():
    bg = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    bg.fill((44, 100, 44))
    for i in range(0, gridSize, 2):
        for j in range(0, gridSize):
            if i % 2 == 0:
                if j % 2 == 0:
                    pygame.draw.rect(bg, (44, 90, 44), (i*TILESIZE, j*TILESIZE, TILESIZE, TILESIZE))
                else:
                    pygame.draw.rect(bg, (44, 90, 44), ((i+1)*TILESIZE, j*TILESIZE, TILESIZE, TILESIZE))

    print("Background generated")
    return bg


def draw_graphics(bg, snake, food):
    surface.blit(bg, (0, 0))
    for i in snake:
        if snake.index(i) == 0:
            pygame.draw.rect(surface, (180, 66, 66), (i[0]*TILESIZE, i[1]*TILESIZE, TILESIZE, TILESIZE))
        else:
            if snake.index(i) % 2 == 0:
                pygame.draw.rect(surface, (120, 66, 66), (i[0]*TILESIZE, i[1]*TILESIZE, TILESIZE, TILESIZE))
            else:
                pygame.draw.rect(surface, (140, 66, 66), (i[0]*TILESIZE, i[1]*TILESIZE, TILESIZE, TILESIZE))

    pygame.draw.rect(surface, (60, 60, 120), (food[0]*TILESIZE, food[1]*TILESIZE, TILESIZE, TILESIZE))
    pygame.display.update()


def update_game_state(snake, food, direction, growth):

    game_over = False

    updated_snake = []
    for i in snake:
        if i == snake[0]:
            updated_snake.append((i[0]+directions.get(direction)[0], i[1]+directions.get(direction)[1]))
        else:
            updated_snake.append(snake[snake.index(i)-1])

        if len(updated_snake) > 1:
            for j in updated_snake:
                if j == i:
                    game_over = True
                    print('Game over. Final score: ' + str(len(snake)))

    if updated_snake[0] == food:
        growth += GROWTHSPEED
        updated_food = (random.randint(1, gridSize-2), random.randint(1, gridSize-2))
    else:
        updated_food = food

    if updated_snake[0][0] > (gridSize-1) or updated_snake[0][0] < 0 \
            or updated_snake[0][1] > (gridSize-1) or updated_snake[0][1] < 0:
        game_over = True

    if growth > 0:
        updated_snake.append(snake[-1])
        growth -= 1

    return updated_snake, updated_food, growth, game_over


def reset():
    pygame.time.wait(2000)
    snake = [((gridSize - 1) / 2, (gridSize - 1) / 2)]
    food = (random.randint(0, gridSize-1), random.randint(0, gridSize-1))
    direction = None
    growth = 0
    return snake, food, direction, growth

if __name__ == '__main__':
    main()