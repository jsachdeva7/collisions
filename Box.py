import pygame
from Constants import WIDTH, HEIGHT, CENTER, YELLOW

class Box:
    def __init__(self, w: int = 500, h: int = 500):
        self.w = w
        self.h = h
        self.left = CENTER[0] - w / 2
        self.right = CENTER[0] + w / 2
        self.top = CENTER[1] - h / 2
        self.bottom = CENTER[1] + h /2

    def draw(self, window):
        rect = pygame.Rect((WIDTH - self.w) / 2, (HEIGHT - self.h) / 2, self.w, self.h)
        pygame.draw.rect(window, YELLOW, rect, 3)