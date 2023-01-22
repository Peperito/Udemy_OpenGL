import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
from Utils import *

pygame.init()

screen_width = 1000
screen_height = 800
ortho_left = 0
ortho_right = 640
ortho_top = 480
ortho_bottom = 0

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Graphs in PyOpenGL')


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(ortho_left, ortho_right, ortho_top, ortho_bottom)


def plot_point():
    glBegin(GL_POINTS)
    for point in line:
        glVertex2f(point[0], point[1])
    glEnd()


def plot_lines():
    for lines in points:
        glBegin(GL_LINE_STRIP)
        for cords in lines:
            glVertex2f(cords[0], cords[1])
        glEnd()


def save_drawing():
    f = open("drawing.txt", "w")
    f.write(str(len(points)) + "\n")
    for l in points:
        f.write(str(len(l)) + "\n")
        for cords in l:
            x_cord = round(cords[0], 2)
            y_cord = round(cords[1], 2)
            f.write(str(x_cord) + " " + str(y_cord) + "\n")
    f.close()
    print("Drawing cords saved")


def load_drawing():
    f = open("drawing.txt", "r")
    num_of_lines = int(f.readline())
    global points
    global line
    points = []

    for l in range(num_of_lines):
        line = []
        points.append(line)
        num_of_cords = int(f.readline())
        for coord_number in range(num_of_cords):
            px, py = [float(value) for value in next(f).split()]
            line.append((px, py))

def plot_graph():
    glBegin(GL_LINE_STRIP)
    px: GL_DOUBLE
    py: GL_DOUBLE

    for px in np.arange(0, 10, 0.05):
        py = math.exp(-px) * math.cos(2 * math.pi * px)
        glVertex2f(px, py)
    glEnd()


done = False
init_ortho()
glPointSize(4)
points = []
line = []
current_arr = 0
mouse_down = False
while not done:
    p = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == K_s:
                save_drawing()
            elif event.key == K_l:
                load_drawing()
            elif event.key == K_SPACE:
                points = []
        elif event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            line = []
            points.append(line)
        elif event.type == MOUSEBUTTONUP:
            mouse_down = False
        elif event.type == MOUSEMOTION and mouse_down:
            p = pygame.mouse.get_pos()
            line.append((
                map_value(0, screen_width, ortho_left, ortho_right, p[0]),
                map_value(0, screen_height, ortho_bottom, ortho_top, p[1])
            ))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    plot_lines()

    pygame.display.flip()
    pygame.time.wait(0)
pygame.quit()
