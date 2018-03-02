import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import random

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6),
)

ground_vertices = (
    (-20, -0.1, 5),
    (20, -0.1, 5),
    (20, -0.1, -60),
    (-20, -0.1, -60),
)


def update_ground_vertices(cur_x, cur_z):
    uground_vertices = []
    cur_x = -1*int(cur_x)
    x_value_change = cur_x
    z_value_change = cur_z

    for vertex in ground_vertices:
        new_vertex = [vertex[0]+x_value_change, vertex[1], vertex[2]+z_value_change]
        uground_vertices.append(new_vertex)
    print(uground_vertices)
    return uground_vertices


def ground(cur_x, cur_z):
    uground_vertices = update_ground_vertices(cur_x, cur_z)
    glBegin(GL_QUADS)
    for vertex in uground_vertices:
        glColor3fv((0, 0.5, 0.1))
        glVertex3fv(vertex)
    glEnd()


def set_vertices(max_distance, min_distance=-20, camera_x=0):
    camera_x = -1*int(camera_x)
    x_value_change = random.randrange(camera_x-20, camera_x+20)
    y_value_change = 0
    z_value_change = random.randrange(-1*max_distance, min_distance)
    new_vertices = []

    for vertex in vertices:
        new_vertex = [vertex[0]+x_value_change, vertex[1]+y_value_change, vertex[2]+z_value_change]
        new_vertices.append(new_vertex)
    return new_vertices


def cube(vertices_):
    glBegin(GL_QUADS)
    for surface in surfaces:
        x=0
        for vertex in surface:
            x+=1
            glColor3fv((1, 0.3, 0))
            glVertex3fv(vertices_[vertex])
    glEnd()


def main():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    FPS = 30
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    max_distance = 60
    gamespeed = 0.2

    score = 0

    gluPerspective(90, display[0]/display[1], 0.1, max_distance)
    glTranslatef(0, 0, -40)

    cur_x = 0
    cur_y = 0
    x_move = 0
    y_move = 0

    cube_dict = dict()

    for x in range(10):
        cube_dict[x] = set_vertices(max_distance)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            x_move = gamespeed
        elif keys[K_RIGHT]:
            x_move = -gamespeed
        else:
            x_move = y_move = 0
        x = glGetDoublev(GL_MODELVIEW_MATRIX)

        camera_x = x[3][0]
        camera_z = x[3][2]

        cur_x = camera_x

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glTranslatef(x_move, y_move, gamespeed)

        ground(cur_x, camera_z)

        for each_cube in cube_dict:
            cube(cube_dict[each_cube])

        for each_cube in cube_dict:
            if camera_z <= cube_dict[each_cube][0][2]:
                score += 1
                new_max = int(-1*(camera_z-(max_distance*1.5)))
                cube_dict[each_cube] = set_vertices(new_max, int(camera_z) - max_distance, cur_x)

        glTranslatef(0, 0, 0.6)
        pygame.display.flip()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
    pygame.quit()
    quit()