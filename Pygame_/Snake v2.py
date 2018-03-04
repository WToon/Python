import os
import pygame as pg
import sys
import random
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

N_GRID = 41
window_width = window_height = N_GRID * 20
tile_size = int(window_width / N_GRID)
FPS = 25
SURFACE = None
FONT = None

growth_speed = 10
directions = {None: (0, 0), 'NORTH': (0, -1), 'EAST': (1, 0), 'SOUTH': (0, 1), 'WEST': (-1, 0)}


def main():

    clock, bg, snake, food = init()

    direction = None
    growth = 0
    game_speed = 1

    game_over = False
    paused = False
    restart = False

    while True:

        t_direction = direction
        for event in pg.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pg.quit()
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
                elif event.key == K_p:
                    paused = not paused
        direction = t_direction

        while paused:
            SURFACE.blit(generate_text(False, False, True, snake), (0, 0))
            pg.display.update()
            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_p:
                        paused = not paused

        while game_over:
            SURFACE.blit(generate_text(False, True, False, snake), (0, 0))
            pg.display.update()
            for event in pg.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pg.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        game_over = False
                        restart = True

        if restart:
            snake, food, direction, growth, game_speed = reset()
            bg = generate_raster()
            restart = False

        snake, food, growth, game_speed, game_over = update_game_state(snake, food, direction,
                                                                       growth, game_speed)
        draw_graphics(bg, snake, food)

        pg.display.update()
        clock.tick(FPS*game_speed)


def init():
    pg.init()
    global SURFACE, FPS, FONT
    FONT = pg.font.SysFont('Calibri', 30, True)

    clock = pg.time.Clock()
    SURFACE = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption('Snake')
    bg = generate_raster()
    return clock, bg, [((N_GRID - 1) / 2, (N_GRID - 1) / 2)], [(random.randint(0, N_GRID - 1),
                                                                random.randint(0, N_GRID - 1),
                                                                random.randint(1, growth_speed))]


def generate_raster(_color1_=(66, 66, 66), _color2_=None, checkers=False):
    bg = pg.Surface((window_width, window_height))
    bg.fill(_color1_)
    if checkers:
        for i in range(0, N_GRID, 2):
            for j in range(0, N_GRID):
                if i % 2 == 0:
                    if j % 2 == 0:
                        pg.draw.rect(bg, _color2_, (i * tile_size, j * tile_size, tile_size, tile_size))
                    else:
                        pg.draw.rect(bg, _color2_, ((i+1) * tile_size, j * tile_size, tile_size, tile_size))
    return bg


def generate_text(score, restart, pause, snake):
    ts = pg.Surface((window_width, window_height), pg.SRCALPHA, 32)
    ts = ts.convert_alpha()
    if restart:
        restart = FONT.render("Press 'R' to restart.", True, (144, 144, 144))
        ts.blit(restart, (window_width/3, window_height/4))
    elif pause:
        pause = FONT.render("Game paused. 'P' to continue", True, (144, 144, 144))
        ts.blit(pause, (window_width/3.5, window_height/4))
    return ts


def draw_graphics(bg, snake, food):
    SURFACE.blit(bg, (0, 0))
    score = FONT.render("Score: " + str(len(snake) - 1), True, (200, 200, 200))
    SURFACE.blit(score, (20, 20))
    for i in snake:
        if snake.index(i) == 0:
            pg.draw.rect(SURFACE, (180, 66, 66), (i[0] * tile_size - 1, i[1] * tile_size - 1, tile_size + 2, tile_size + 2))
        else:
            if snake.index(i) % 4 == 0:
                pg.draw.rect(SURFACE, (120, 66, 66), (i[0] * tile_size + 1, i[1] * tile_size + 1, tile_size - 2, tile_size - 2))
            else:
                pg.draw.rect(SURFACE, (140, 66, 66), (i[0] * tile_size, i[1] * tile_size, tile_size, tile_size))

    for i in food:
        if i[2] == growth_speed:
            pg.draw.rect(SURFACE, (255, 60, 120), (i[0] * tile_size, i[1] * tile_size, tile_size, tile_size))
        elif i[2] > int(growth_speed*3/4):
            pg.draw.rect(SURFACE, (60, 60, 120), (i[0] * tile_size, i[1] * tile_size, tile_size, tile_size))
        elif i[2] > int(growth_speed/2):
            pg.draw.rect(SURFACE, (60, 120, 120), (i[0] * tile_size, i[1] * tile_size, tile_size, tile_size))
        elif i[2] > int(growth_speed/4):
            pg.draw.rect(SURFACE, (120, 60, 120), (i[0] * tile_size, i[1] * tile_size, tile_size, tile_size))
        else:
            pg.draw.rect(SURFACE, (60, 60, 60), (i[0] * tile_size, i[1] * tile_size, tile_size, tile_size))


def update_game_state(snake, food, direction, growth, game_speed):

    # advance snake and check if it ate itself
    updated_snake, game_over = update_snake(snake, direction)

    # check if food was eaten and generate new
    updated_food, growth, game_speed = check_if_eaten(food, updated_snake, growth, game_speed)

    # grow the snake
    if growth > 0:
        updated_snake.append(snake[-1])
        growth -= 1

    return updated_snake, updated_food, growth, game_speed, game_over


def update_snake(snake, direction):
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

    if updated_snake[0][0] > (N_GRID-1) or updated_snake[0][0] < 0 \
            or updated_snake[0][1] > (N_GRID-1) or updated_snake[0][1] < 0:
        return snake, True
    return updated_snake, game_over


def check_if_eaten(food, updated_snake, growth, game_speed):
    updated_food = food
    for i in food:
        if updated_snake[0] == (i[0], i[1]):
            growth += i[2]
            if i[2] == growth_speed:
                game_speed = 1.2
            else:
                game_speed = 1
            food.remove(i)
            updated_food = generate_new_food(food)
    return updated_food, growth, game_speed


def generate_new_food(food):
    if len(food) == 0:
        food.append((random.randint(1, N_GRID - 2),
                     random.randint(1, N_GRID - 2),
                     random.randint(1, growth_speed)))
    if len(food) < 3:
        for i in range(0, random.randint(0, 2)):
            food.append((random.randint(1, N_GRID - 2),
                         random.randint(1, N_GRID - 2),
                         random.randint(1, growth_speed)))
    return food


def reset():
    snake = [((N_GRID - 1) / 2, (N_GRID - 1) / 2)]
    food = [(random.randint(0, N_GRID - 1), random.randint(0, N_GRID - 1), random.randint(1, growth_speed))]
    direction = None
    growth = 0
    game_speed = 1
    return snake, food, direction, growth, game_speed

if __name__ == '__main__':
    main()