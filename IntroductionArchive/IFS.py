import math

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *
import numpy as np

pygame.init()

screen_width = 800
screen_height = 800
ortho_left = -400
ortho_right = 400
ortho_top = 0
ortho_bottom = 800

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Turtle Graphics')

current_position = (0, 0)
direction = np.array([0, 1, 0])

points = []
x = 0
y = 0


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)


def draw_points():
    glBegin(GL_POINTS)
    for p in points:
        glVertex2f(p[0], p[1])
    glEnd()


def reset_turtle():
    global current_position, direction
    current_position = (0, 0)
    direction = np.array([0, 1, 0])


# Modified from original to leptosporangiate fern
def draw_turtle():
    global x, y
    points.append((x, y))
    r = np.random.rand()
    if r < 0.02:
        x, y = 0.00 * x + 0.00 * y + 0.0, 0.00 * x + 0.25 * y - 0.4
    elif r < 0.86:
        x, y = 0.95 * x + 0.005 * y - 0.002, -0.005 * x + 0.93 * y + 0.5
    elif r < 0.93:
        x, y = 0.035 * x - 0.2 * y - 0.09, 0.16 * x + 0.04 * y + 0.02
    else:
        x, y = -0.04 * x + 0.2 * y + 0.083, 0.16 * x + 0.04 * y + 0.12


def draw_turtle_2():
    global x, y
    points.append((x, y))
    r = np.random.rand()
    if r < 0.33:
        x, y = 0.5 * x + 0.00 * y + 0.0, 0.0 * x + 0.5 * y + 0.5
    elif r < 0.66:
        x, y = 0.5 * x + 0.00 * y + 0.5, 0.0 * x + 0.5 * y + 0.0
    else:
        x, y = 0.5 * x + 0.00 * y + 0.0, 0.0 * x + 0.5 * y + 0.0


init_ortho()
done = False
glPointSize(1)
glColor3f(0, 1, 0)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glScaled(200, 120, 1)
    reset_turtle()
    draw_turtle()
    draw_points()

    pygame.display.flip()
    pygame.time.wait(1)
pygame.quit()
