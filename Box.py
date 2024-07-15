import pygame
import numpy as np
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

    def uniform_grid_partition(self, window: pygame.Surface, N: int):
        if not hasattr(self, "row_bounds") or not hasattr(self, "col_bounds"):
            self.N = N
            self.row_bounds = []
            self.col_bounds = []
            self.cell_width = self.w / N
            self.cell_height = self.h / N
            x = self.left
            y = self.top
            for i in range(N + 1):
                self.col_bounds.append(x)
                self.row_bounds.append(y)
                x += self.cell_width
                y += self.cell_height
            self.cells = [[[] for _ in range(N)] for _ in range(N)]
        self.draw_uniform_grid_partition(window)

    def draw_uniform_grid_partition(self, window: pygame.Surface):
        for i in range(len(self.col_bounds)):
            pygame.draw.line(window, (255, 255, 255), (self.col_bounds[i], self.top), (self.col_bounds[i], self.bottom))
            pygame.draw.line(window, (255, 255, 255), (self.left, self.row_bounds[i]), (self.right, self.row_bounds[i]))

    def clear_uniform_grid_cells(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j] = []
