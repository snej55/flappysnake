import pygame, math

from .verlet import VerletStrip

SEGMENT_SIZE = 160
SEGMENT_DENSITY = 4
STIFFNESS = 0.9

class Snake:
    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0)
        self.length = 3
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
    
    def update(self):
        self.verlet.points[len(self.points) // 2]["x"], self.verlet.points[len(self.points) // 2]["y"] = pygame.mouse.get_pos()
        self.verlet.points[len(self.points) // 2]["prev_x"], self.verlet.points[len(self.points) // 2]["prev_y"] = pygame.mouse.get_pos()
        self.verlet.update_points()
        for _ in range(10):
            self.verlet.update_sticks()
            self.verlet.constrain_points()

    
    def draw(self, surf, scroll):
        self.verlet.render(surf, scroll)



