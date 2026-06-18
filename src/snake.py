import pygame, math, numpy

from .verlet import VerletStrip

SEGMENT_SIZE = 32
SEGMENT_DENSITY = 4
STIFFNESS = 0.9

class Snake:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0)
        self.length = 10
        self.verlet = VerletStrip([], [])
        self.points = []
        self.sticks = []
        self.generate_strip()

    @staticmethod
    def distance(p0, p1):
        return math.sqrt((p0['x'] - p1['x'])**2 + (p0['y'] - p1['y'])**2)
    
    def generate_strip(self):
        head_pos = list(self.pos)
        self.points = []
        self.points.append({"x": head_pos[0], "y": head_pos[1], "prev_x": head_pos[0], "prev_y": head_pos[1], "pinned": False})
        for x in range(math.ceil(SEGMENT_DENSITY * self.length)):
            p = [head_pos[0] - (x + 1) * (SEGMENT_SIZE / SEGMENT_DENSITY), head_pos[1]]
            self.points.append({"x": p[0], "y": p[1], "prev_x": p[0], "prev_y": p[1], "pinned": False})
        
        self.sticks = []
        for i in range(len(self.points) - 1):
            self.sticks.append({"p0": self.points[i], "p1": self.points[i + 1], "length": self.distance(self.points[i], self.points[i + 1])})
            if i + 2 < len(self.points) - 1:
                self.sticks.append({"p0": self.points[i], "p1": self.points[i + 2], "length": self.distance(self.points[i], self.points[i + 2]), "stiffness": STIFFNESS})
        self.verlet = VerletStrip(self.points, self.sticks)
    
    def get_quad_mesh(self):
        vertices = []
        points = self.verlet.points
        for i, p in enumerate(points):
            pos = pygame.Vector2(p['x'], p['y'])
            direction = pygame.Vector2(0, 0)
            if i == 0:
                direction = pygame.Vector2(points[i + 1]["x"], points[i + 1]["y"]) - pos
            elif i == len(points) - 1:
                direction = pos - pygame.Vector2(points[i - 1]["x"], points[i - 1]["y"])
            else:
                direction = pygame.Vector2(points[i + 1]["x"], points[i + 1]["y"]) - pygame.Vector2(points[i - 1]["x"], points[i - 1]["y"])
            if direction.length_squared() > 0:
                direction = direction.normalize()
            else:
                direction = pygame.Vector2(1, 0)
            norm = pygame.Vector2(-direction.y, direction.x)

            left = pos + norm * SEGMENT_SIZE * 0.5
            right = pos - norm * SEGMENT_SIZE * 0.5

            u = 0.0
            if i < SEGMENT_DENSITY * 2:
                u = 1.0 - (i / (SEGMENT_DENSITY * 2)) * 0.5
            elif len(points) - 1 - i < SEGMENT_DENSITY:
                u = (len(points) - 1 - i) / SEGMENT_DENSITY * 0.25
            else:
                body_index = i - SEGMENT_DENSITY * 2
                t = (body_index % SEGMENT_DENSITY) / SEGMENT_DENSITY
                u = 0.25 + t * 0.25

            vertices.extend([left.x, left.y, u, 0.0])
            vertices.extend([right.x, right.y, u, 1.0])
        return numpy.array(vertices, dtype='f4')

    
    def update(self):
        self.verlet.points[len(self.points) // 2]["x"], self.verlet.points[len(self.points) // 2]["y"] = pygame.mouse.get_pos()
        self.verlet.points[len(self.points) // 2]["prev_x"], self.verlet.points[len(self.points) // 2]["prev_y"] = pygame.mouse.get_pos()
        self.verlet.update_points()
        for _ in range(10):
            self.verlet.update_sticks()
            self.verlet.constrain_points()
    
    def draw(self, surf, scroll):
        self.verlet.render(surf, scroll)



