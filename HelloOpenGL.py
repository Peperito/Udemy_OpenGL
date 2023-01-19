import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

screen_width = 1000
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL in Python")


def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)


def draw_stars(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()


done = False
init_ortho()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_stars(800, 200, 10)
    draw_stars(700, 300, 16)
    draw_stars(550, 270, 10)
    draw_stars(400, 190, 20)
    draw_stars(300, 400, 10)
    draw_stars(400, 500, 12)
    draw_stars(700, 500, 14)
    draw_stars(850, 750, 16)

    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()

