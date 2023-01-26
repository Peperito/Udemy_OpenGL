import time

import pygame

from glapp.PyOGLApp import *
from glapp.GraphicsData import *
import numpy as np
from glapp.Utils import *
from glapp.LoadMesh import *
from glapp.MovingCube import *
from glapp.Light import *

vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
in vec3 vertex_normal;
in vec2 vertex_uv;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;
out vec3 color;
out vec3 normal;
out vec3 frag_pos;
out vec3 view_pos;
out vec2 UV;
void main() 
{
    view_pos = vec3(inverse(model_mat) * 
                vec4(view_mat[3][0], view_mat[3][1], view_mat[3][2], 1));
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
    normal = mat3(transpose(inverse(model_mat))) * vertex_normal;
    frag_pos = vec3(model_mat * vec4(position, 1));
    color = vertex_color;
    UV = vertex_uv;
}
'''

fragment_shader = r'''
#version 330 core
in vec3 color;
in vec3 normal;
in vec3 frag_pos;
in vec3 view_pos;
out vec4 frag_color;

in vec2 UV;
uniform sampler2D tex;

struct light {
    vec3 position;
    vec3 color;
};

#define NUM_LIGHTS 3
uniform light light_data[NUM_LIGHTS];

vec4 Create_Light(vec3 light_pos, vec3 light_color, vec3 normal, vec3 frag_pos, vec3 view_dir) 
{

    //ambient
    float a_strength = 0.2;
    vec3 ambient = a_strength * light_color;
    
    //diffuse
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - frag_pos);
    float diff = max(dot(norm, light_dir), 0);
    vec3 diffuse = diff * light_color;

    //specular 
    float s_strength = 0.8;
    vec3 reflect_dir = normalize(-light_dir - norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0), 32);
    vec3 specular = s_strength * spec * light_color; 
    
    return vec4(color * (ambient + diffuse + specular), 1);
}

void main()
{
    vec3 view_dir = normalize(view_pos - frag_pos);
    for(int i = 0; i < NUM_LIGHTS; i++){
        frag_color += Create_Light(light_data[i].position, light_data[i].color, normal, frag_pos, view_dir); 
    }
    frag_color = frag_color * texture(tex, UV);
}
'''


class ShadedObject(PyOGLApp):

    def __init__(self):
        super().__init__(850, 200, 1000, 800)
        # self.world_axes = None
        self.light = None
        self.plane = None
        self.cube = None
        glEnable(GL_CULL_FACE)

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.plane = LoadMesh("./objs/plane.obj", "./images/window.png", self.program_id)
        self.cube = LoadMesh("./objs/cube.obj", "./images/crate.png", self.program_id,
                             location=pygame.Vector3(0, -1, 0))
        self.light = Light(self.program_id, pygame.Vector3(0, 1, 0), pygame.Vector3(1, 1, 1), 0)
        self.camera = Camera(self.program_id, self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.light.update()
        self.cube.draw()
        self.plane.draw()


ShadedObject().mainloop()
