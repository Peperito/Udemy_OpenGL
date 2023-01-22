from glapp.PyOGLApp import *
from glapp.GraphicsData import *
import numpy as np
from glapp.Utils import *
from glapp.Square import *
from glapp.WorldAxes import *
from glapp.ChristmasTriangle import *
from glapp.Cube import *

vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;
out vec3 color;
void main() 
{
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
    color = vertex_color;
}
'''

fragment_shader = r'''
#version 330 core
in vec3 color;
out vec4 frag_color;
void main()
{
    frag_color = vec4(color, 1);
}
'''


class Projections(PyOGLApp):

    def __init__(self):
        super().__init__(850, 200, 1000, 800)
        self.triangle = None
        self.square = None
        self.world_axes = None
        self.cube = None

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        self.triangle = ChristmasTriangle(self.program_id, location=pygame.Vector3(-1, 1, 0))
        self.square = Square(self.program_id, location=pygame.Vector3(0.5, -0.5, 0))
        glLineWidth(5)
        self.world_axes = WorldAxes(self.program_id, location=pygame.Vector3(0, 0, 0))
        self.cube = Cube(self.program_id)
        self.camera = Camera(self.program_id, self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.triangle.draw()
        self.square.draw()
        self.cube.draw()
        self.world_axes.draw()


Projections().mainloop()
