import os
import pygame as pg
import sys
import random
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'

N_GRID = 81
WINDOWWIDTH = WINDOWHEIGHT = N_GRID * 12
TILESIZE = int(WINDOWWIDTH / N_GRID)
FPS = 25
GROWTHSPEED = 15

directions = {None: (0, 0), 'NORTH': (0, -1), 'EAST': (1, 0), 'SOUTH': (0, 1), 'WEST': (-1, 0)}


def main():

    clock, bg, snake, food = init()

    font = pg.font.Font(None, 30)

    direction = None
    growth = 0

    game_over = False
    paused = False

    while True:

        if game_over:
            pg.event.clear()

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

        if not paused:
            snake, food, growth, game_over = update_game_state(snake, food, direction, growth)

        if game_over:
            snake, food, direction, growth = reset()

        if len(snake) > int(N_GRID*N_GRID*0.8):
            print("Hey fatty, You filled 80% of the board!")
        elif len(snake) > int(N_GRID*N_GRID*0.6):
            print("Hey fatty, You filled 60% of the board!")
        elif len(snake) > int(N_GRID*N_GRID*0.4):
            print("Hey fatty, You filled 40% of the board!")
        elif len(snake) > int(N_GRID*N_GRID*0.2):
            print("Hey fatty, You filled 20% of the board!")

        draw_graphics(bg, snake, food)
        fps = font.render(str(int(clock.get_fps())), True, pg.Color('white'))
        surface.blit(fps, (50, 50))
        pg.display.update()
        clock.tick(FPS)


def init():
    pg.init()
    global surface
    clock = pg.time.Clock()
    surface = pg.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pg.display.set_caption('Snake')
    bg = generate_raster()
    print("Initialized")
    return clock, bg, [((N_GRID - 1) / 2, (N_GRID - 1) / 2)], [(random.randint(0, N_GRID - 1),
                                                                random.randint(0, N_GRID - 1),
                                                                random.randint(1, GROWTHSPEED))]


def generate_raster():
    bg = pg.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    bg.fill((66, 66, 66))
    for i in range(0, N_GRID, 2):
        for j in range(0, N_GRID):
            if i % 2 == 0:
                if j % 2 == 0:
                    pg.draw.rect(bg, (66, 66, 66), (i*TILESIZE, j*TILESIZE, TILESIZE, TILESIZE))
                else:
                    pg.draw.rect(bg, (66, 66, 66), ((i+1)*TILESIZE, j*TILESIZE, TILESIZE, TILESIZE))

    print("Background generated")
    return bg


def draw_graphics(bg, snake, food):
    surface.blit(bg, (0, 0))
    for i in snake:
        if snake.index(i) == 0:
            pg.draw.rect(surface, (180, 66, 66), (i[0]*TILESIZE-1, i[1]*TILESIZE-1, TILESIZE+2, TILESIZE+2))
        else:
            if snake.index(i) % 4 == 0:
                pg.draw.rect(surface, (120, 66, 66), (i[0]*TILESIZE+1, i[1]*TILESIZE+1, TILESIZE-2, TILESIZE-2))
            else:
                pg.draw.rect(surface, (140, 66, 66), (i[0]*TILESIZE, i[1]*TILESIZE, TILESIZE, TILESIZE))

    for i in food:
        if i[2] > int(GROWTHSPEED*3/4):
            pg.draw.rect(surface, (60, 60, 120), (i[0]*TILESIZE, i[1]*TILESIZE, TILESIZE, TILESIZE))
        elif i[2] > int(GROWTHSPEED/2):
            pg.draw.rect(surface, (60, 120, 120), (i[0]*TILESIZE, i[1]*TILESIZE, TILESIZE, TILESIZE))
        elif i[2] > int(GROWTHSPEED/4):
            pg.draw.rect(surface, (120, 60, 120), (i[0]*TILESIZE, i[1]*TILESIZE, TILESIZE, TILESIZE))
        else:
            pg.draw.rect(surface, (60, 60, 60), (i[0]*TILESIZE, i[1]*TILESIZE, TILESIZE, TILESIZE))


def update_game_state(snake, food, direction, growth):

    # advance snake and check if it ate itself
    updated_snake, game_over = update_snake(snake, direction)

    # check if food was eaten and generate new
    updated_food, growth = check_if_eaten(food, updated_snake, growth)

    # check field boundaries
    if not game_over:
        game_over = wrap_borders(updated_snake)

    # grow the snake
    if growth > 0:
        updated_snake.append(snake[-1])
        growth -= 1

    return updated_snake, updated_food, growth, game_over


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

    return updated_snake, game_over


def check_if_eaten(food, updated_snake, growth):
    updated_food = food
    for i in food:
        if updated_snake[0] == (i[0], i[1]):
            growth += i[2]
            food.remove(i)
            updated_food = generate_new_food(food)
    return updated_food, growth


def generate_new_food(food):
    if len(food) == 0:
        food.append((random.randint(1, N_GRID - 2),
                     random.randint(1, N_GRID - 2),
                     random.randint(1, GROWTHSPEED)))
    if len(food) < 3:
        for i in range(0, random.randint(0, 2)):
            food.append((random.randint(1, N_GRID - 2),
                         random.randint(1, N_GRID - 2),
                         random.randint(1, GROWTHSPEED)))
    return food


def wrap_borders(updated_snake):
    if updated_snake[0][0] > (N_GRID-1) or updated_snake[0][0] < 0 \
            or updated_snake[0][1] > (N_GRID-1) or updated_snake[0][1] < 0:
        return True
    return False


def reset():
    pg.time.wait(1000)
    snake = [((N_GRID - 1) / 2, (N_GRID - 1) / 2)]
    food = [(random.randint(0, N_GRID - 1), random.randint(0, N_GRID - 1), random.randint(1, GROWTHSPEED))]
    direction = None
    growth = 0
    return snake, food, direction, growth

if __name__ == '__main__':
    main()