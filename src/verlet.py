import pygame, math

BOUNCE = 0.9
FRICTION = 0.999
GRAVITY = 0.001

class VerletStrip:
    def __init__(self, points: list[dict] = [], sticks: list[dict] = []):
        self.points = points
        self.sticks = sticks
    
    def update_points(self):
        for point in self.points:
            if not point["pinned"]:
                vx = (point["x"] - point["prev_x"]) * FRICTION
                vy = (point["y"] - point["prev_y"]) * FRICTION
                point["prev_x"] = point["x"]
                point["prev_y"] = point["y"]
                point["x"] += vx
                point["y"] += vy + GRAVITY
    
    # collisions
    def constrain_points(self):
        pass
    
    def render(self, surf, scroll=[0, 0]):
        for point in self.points:
            pygame.draw.circle(surf, (255, 255, 255), (point["x"] - scroll[0], point["y"] - scroll[1]), 2)
        for stick in self.sticks:
            pygame.draw.line(surf, (255, 255, 255), (stick['p0']['x'] - scroll[0], stick['p0']['y'] - scroll[1]), (stick['p1']['x'] - scroll[0], stick['p1']['y'] - scroll[1]), width=2)
    
    def update_sticks(self):
        for _ in range(3):
            for stick in self.sticks:
                dx, dy = stick["p0"]["x"] - stick["p1"]["x"], stick["p0"]["y"] - stick["p1"]["y"]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance == 0:
                    distance = 0.1
                difference = stick["length"] - distance
                stiffness = stick.get('stiffness', 1.0)
                percentage = difference / distance / 2 * stiffness

                offset_x = dx * percentage
                offset_y = dy * percentage
                if not stick['p0']['pinned'] and not stick['p1']['pinned']:
                    stick['p0']['x'] += offset_x
                    stick['p0']['y'] += offset_y
                    stick['p1']['x'] -= offset_x
                    stick['p1']['y'] -= offset_y
                elif stick['p0']['pinned'] and not stick['p1']['pinned']:
                    stick['p1']['x'] -= offset_x * 2
                    stick['p1']['y'] -= offset_y * 2
                elif not stick['p0']['pinned'] and stick['p1']['pinned']:
                    stick['p0']['x'] += offset_x * 2
                    stick['p0']['y'] += offset_y * 2