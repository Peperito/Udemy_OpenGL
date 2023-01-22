import math
import numpy as np

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils import *

pygame.init()

screen_width = 800
screen_height = 800
ortho_left = -400
ortho_right = 400
ortho_top = -400
ortho_bottom = 400

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Polygons in PyOpenGL')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)


def plot_polygon():
    for triangles in points:
        glBegin(GL_QUADS)
        glColor(0.2, 0.2, 0.2, 1)
        for cords in triangles:
            glVertex2f(cords[0], cords[1])
        glEnd()


def plot_border():
    for triangles in points:
        glBegin(GL_LINE_LOOP)
        glColor(0.8, 0.8, 0.8, 0.7)
        for cords in triangles:
            glVertex2f(cords[0], cords[1])
        glEnd()


def plot_points():
    for vertex in triangle:
        glBegin(GL_POINTS)
        glColor(1, 1, 1, 0.8)
        glVertex2f(vertex[0], vertex[1])
        glEnd()


done = False
init_ortho()
points = []
triangle = []
glLineWidth(5)
glPointSize(10)
while not done:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            triangle.append((map_value(0, screen_width, ortho_left, ortho_right, p[0]),
                             map_value(0, screen_height, ortho_bottom, ortho_top, p[1])))
            if len(triangle) == 4:
                points.append(triangle)
                triangle = []

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    plot_polygon()
    plot_border()
    plot_points()

    pygame.display.flip()
pygame.quit()
