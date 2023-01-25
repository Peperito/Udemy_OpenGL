import time

import pygame

from glapp.PyOGLApp import *
from glapp.GraphicsData import *
import numpy as np
from glapp.Utils import *
from glapp.Square import *
from glapp.WorldAxes import *
from glapp.ChristmasTriangle import *
from glapp.Cube import *
from glapp.LoadMesh import *
from glapp.MovingCube import *

vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
in vec3 vertex_normal;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;
out vec3 color;
out vec3 normal;
out vec3 frag_pos;
out vec3 light_pos;
void main() 
{
    light_pos = vec3(inverse(model_mat) * 
                vec4(view_mat[3][0], view_mat[3][1], view_mat[3][2], 1));
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
    normal = vertex_normal;
    frag_pos = vec3(model_mat * vec4(position, 1));
    color = vertex_color;
}
'''

fragment_shader = r'''
#version 330 core
in vec3 color;
in vec3 normal;
in vec3 frag_pos;
in vec3 light_pos;
out vec4 frag_color;
void main()
{
    vec3 light_color = vec3(1, 1, 1);
    //ambient
    float a_strength = 0.1;
    vec3 ambient = a_strength * light_color;
    
    //diffuse
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - frag_pos);
    float diff = max(dot(norm, light_dir), 0);
    vec3 diffuse = diff * light_color;

    //specular 
    float s_strength = 0.8;
    vec3 view_dir = normalize(light_pos - frag_pos);
    vec3 reflect_dir = normalize(-light_dir - norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0), 32);
    vec3 specular = s_strength * spec * light_color; 
    
    frag_color = vec4(color * (ambient + diffuse + specular), 1);
}
'''


class ShadedObject(PyOGLApp):

    def __init__(self):
        super().__init__(850, 200, 1000, 800)
        #self.world_axes = None
        #self.moving_cube = None
        self.teapot = None

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        #self.world_axes = WorldAxes(self.program_id, location=pygame.Vector3(0, 0, 0))
        #self.moving_cube = LoadMesh("./objs/cube.obj", self.program_id,
                                    #move_translation=pygame.Vector3(0, 0.001, 0))
        self.teapot = LoadMesh("./objs/teapot.obj", self.program_id,
                               scale=pygame.Vector3(0.5, 0.5, 0.5),
                               move_rotation=Rotation(1, pygame.Vector3(0, 1, 0)))
        self.camera = Camera(self.program_id, self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        #self.world_axes.draw()
        self.teapot.draw()
        #self.moving_cube.draw()


ShadedObject().mainloop()
