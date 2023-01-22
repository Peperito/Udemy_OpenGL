from OpenGL import *
import pygame
from Engine2.glapp.GraphicsData import *
import numpy as np


class Mesh:
    def __init__(self, program_id, vertices, vertex_colors, draw_type):
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

    def draw(self):
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
