import pygame
import random
import math
from Constants import WIDTH, HEIGHT, RED
from Box import Box

pygame.init()
FONT = pygame.font.SysFont("comicsans", 15)

class Particle:
    def __init__(self, r: int = 5, m: int = 10):
        self.r = r
        self.s: pygame.math.Vector2 = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)
        self.v: pygame.math.Vector2 = self.get_starting_v()
        self.a: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.m = m
        self.leftmost = self.s.x - self.r
        # self.points = []

    def get_starting_v(self):
        starting_angle = random.randrange(360)
        return 200 * pygame.math.Vector2(math.cos(starting_angle * math.pi / 180), math.sin(starting_angle * math.pi / 180))
    
    def update(self, dt, box):
        self.v = self.v + self.a * dt
        self.s = self.s + self.v * dt
        self.handle_box_collision(box, dt)
        self.leftmost = self.s.x - self.r
        

        # self.points.append((self.s.x, self.s.y))
        # if len(self.points) >= 2:
        #     pygame.draw.lines(self.window, RED, False, self.points)

    def handle_box_collision(self, box: Box, dt: float):
        # if self.s.x - self.r < box.left:
        #     self.v.x = abs(self.v.x)
        # elif self.s.x + self.r > box.right:
        #     self.v.x = -abs(self.v.x)
        # if self.s.y - self.r < box.top:
        #     self.v.y = abs(self.v.y)
        # elif self.s.y + self.r > box.bottom:
        #     self.v.y = -abs(self.v.y)

        y0 = self.s.y
        y1 = self.s.y + self.v.y * dt
        x0 = self.s.x
        x1 = self.s.x + self.v.x * dt

        if y1 != y0: 
            tc_bottom = abs((box.bottom - self.r - y0) / (y1 - y0))
            tc_top = abs((box.top + self.r - y0) / (y1 - y0))
        if x1 != x0:
            tc_right = abs((box.right - self.r - x0) / (x1 - x0))
            tc_left = abs((box.left + self.r - x0) / (x1 - x0))

        if 'tc_right' in locals() and tc_right <= 1:
            self.s.x = box.right - self.r - 1
            self.s.y = tc_right * y1 + (1 - tc_right) * y0
            self.v.x = -abs(self.v.x)
        elif 'tc_left' in locals() and tc_left <= 1:
            self.s.x = box.left + self.r + 1
            self.s.y = tc_left * y1 + (1 - tc_left) * y0
            self.v.x = abs(self.v.x)

        if 'tc_top' in locals() and tc_top <= 1:
            self.s.y = box.top + self.r + 1
            self.s.x = tc_top * x1 + (1 - tc_top) * x0
            self.v.y = abs(self.v.y)
        elif 'tc_bottom' in locals() and tc_bottom <= 1:
            self.s.y = box.bottom - self.r - 1
            self.s.x = tc_bottom * x1 + (1 - tc_bottom) * x0
            self.v.y = -abs(self.v.y)

    def draw(self, window: pygame.Surface, box: Box):
        pygame.draw.circle(window, RED, (self.s.x, self.s.y), self.r)
        particle_text = FONT.render(self.name, 1, (255, 255, 255))
        window.blit(particle_text, (self.s.x - particle_text.get_width() / 2, self.s.y - 32))
        pygame.draw.line(window, (255, 255, 255), (self.s.x, self.s.y + self.r), (self.s.x, box.bottom))

    def __lt__(self, other_p: 'Particle') -> bool:
        return self.s.x < other_p.s.x