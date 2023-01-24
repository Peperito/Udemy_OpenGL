from OpenGL import *
import pygame
from Engine2.glapp.GraphicsData import *
from Engine2.glapp.Uniform import *
from Engine2.glapp.Transformations import *
import numpy as np
import time


class Mesh:
    def __init__(self, program_id, vertices, vertex_normals, vertex_uvs, vertex_colors, draw_type,
                 translation=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 scale=pygame.Vector3(1, 1, 1),
                 move_rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 move_translation=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1)):
        # Handle vertices with Graphics Data
        self.vertices = vertices
        self.vertex_normals = vertex_normals
        self.vertex_uvs = vertex_uvs
        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)
        position = GraphicsData("vec3", self.vertices)
        position.create_variable(program_id, "position")
        normals = GraphicsData("vec3", vertex_normals)
        normals.create_variable(program_id, "vertex_normal")

        # Handle colors with Graphics Data
        colors = GraphicsData("vec3", vertex_colors)
        colors.create_variable(program_id, "vertex_color")
        self.transformation_mat = identity_mat()
        self.transformation_mat = rotateA(self.transformation_mat, rotation.angle, rotation.axis)
        self.transformation_mat = translate(self.transformation_mat, translation.x, translation.y, translation.z)
        self.transformation_mat = scale3(self.transformation_mat, scale.x, scale.y, scale.z)
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(program_id, "model_mat")

        self.program_id = program_id
        self.move_rotation = move_rotation
        self.move_translation = move_translation
        self.move_scale = move_scale

    def draw(self):
        self.transformation_mat = rotateA(self.transformation_mat, self.move_rotation.angle, self.move_rotation.axis)
        self.transformation_mat = translate(self.transformation_mat,
                                            self.move_translation.x,
                                            self.move_translation.y,
                                            self.move_translation.z)
        self.transformation_mat = scale3(self.transformation_mat,
                                         self.move_scale.x,
                                         self.move_scale.y,
                                         self.move_scale.z)
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.program_id, "model_mat")
        self.transformation.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
