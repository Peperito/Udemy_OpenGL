f

class Square(Mesh):
    def __init__(self, program_id):
        vertices = [[0.5, 0.5, -1.0],
                    [0.5, -0.5, -1.0],
                    [-0.5, -0.5, -1.0],
                    [-0.5, 0.5, -1.0]]
        colors = [[1, 0, 0], [1, 0.5, 0], [1, 1, 0], [0, 1, 0]]
        super().init