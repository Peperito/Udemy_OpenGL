import pygame

from glapp.PyOGLApp import *
from glapp.GraphicsData import *
import numpy as np
from glapp.Utils import *
from glapp.WorldAxes import *
from glapp.LoadMesh import *
from glapp.Light import *
from glapp.Material import *


class MultiShaders(PyOGLApp):

    def __init__(self):
        super().__init__(850, 200, 1000, 800)
        # self.world_axes = None
        self.lights = []
        self.plane = None
        self.cube = None
        self.cube_2 = None
        self.tabletop = None
        self.teapot = None
        self.axes = None
        self.table_legs = []
        glEnable(GL_CULL_FACE)

    def initialise(self):
        mat = Material("./shaders/texturedvert.vs", "./shaders/texturedfrag.vs")
        axes_mat = Material("./shaders/vertexcolvert.vs", "./shaders/vertexcolfrag.vs")
        self.axes = WorldAxes(pygame.Vector3(0, 0, 0), axes_mat)
        self.plane = LoadMesh("./models/plane.obj", "./images/tiles.png",
                              material=mat,
                              scale=pygame.Vector3(6, 6, 6),
                              location=pygame.Vector3(0, -2, 0))
        self.cube = LoadMesh("./models/cube.obj", "./images/crate.png",
                             location=pygame.Vector3(2.5, -1.5, 2.5),
                             material=mat)
        self.cube_2 = LoadMesh("./models/cube.obj", "./images/crate.png",
                             location=pygame.Vector3(1.5, -1.5, 2.5),
                             material=mat)
        self.tabletop = LoadMesh("./models/tabletop.obj", "./images/timber.png",
                               location=pygame.Vector3(-1, -1.2, 0.4),
                               scale=pygame.Vector3(1.5, 1.5, 2.5),
                               material=mat)
        self.teapot = LoadMesh("./models/teapot.obj", "./images/gold.png",
                                 location=pygame.Vector3(-1, -1.2, 0.4),
                                 scale=pygame.Vector3(0.2, 0.2, 0.2),
                                 material=mat)
        for i in range(1, 5):
            if i % 2 != 0:
                self.table_legs.append(LoadMesh("./models/tableleg.obj", "./images/timber.png",
                                location=pygame.Vector3(-0.3, -1.6, -1.7 + 1.1 * i),
                                scale=pygame.Vector3(0.80, 0.80, 0.80),
                                material=mat))
            else:
                self.table_legs.append(LoadMesh("./models/tableleg.obj", "./images/timber.png",
                                location=pygame.Vector3(-1.7, -1.6, -1.7 + 1.1 * (i-1)),
                                scale=pygame.Vector3(0.80, 0.80, 0.80),
                                material=mat))

        self.lights.append(Light(pygame.Vector3(1, 1, 1), pygame.Vector3(1, 1, 1), 0))
        self.camera = Camera(self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLineWidth(4)
        self.axes.draw(self.camera, None)
        self.cube.draw(self.camera, self.lights)
        self.cube_2.draw(self.camera, self.lights)
        self.plane.draw(self.camera, self.lights)
        self.tabletop.draw(self.camera, self.lights)
        self.teapot.draw(self.camera, self.lights)
        for leg in self.table_legs:
            leg.draw(self.camera, self.lights)


MultiShaders().mainloop()
