from OpenGL import *
import pygame
from Engine2.glapp.GraphicsData import *
from Engine2.glapp.Uniform import *
from Engine2.glapp.Transformations import *
import numpy as np


class Mesh:
    def __init__(self, program_id, vertices, vertex_colors, draw_type, translation=pygame.Vector3(0, 0, 0)):
        # Handle vertices with Graphics Data
        self.vertices = vertices
        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)
        position = GraphicsData("vec3", self.vertices)
        position.create_variable(program_id, "position")

        # Handle colors with Graphics Data
        colors = GraphicsData("vec3", vertex_colors)
        colors.create_variable(program_id, "vertex_color")
        self.transformation_mat = identity_mat()
        self.transformation_mat = translate(self.transformation_mat, translation.x, translation.y, translation.z)
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(program_id, "model_mat")

    def draw(self):
        self.transformation.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
