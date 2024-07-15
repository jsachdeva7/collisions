import pygame
from Box import Box
from Particle import Particle
from Constants import BLACK
import time
import psutil
import os

pygame.init()
WIDTH, HEIGHT = (800, 800)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Simulation")

num_collision_detections = list()
memory_usage_array = list()

def handle_particle_collision(p1: Particle, p2: Particle):
    distance = (p1.s - p2.s).magnitude()
    
    if distance < (p1.r + p2.r) and distance > (p1.r + p2.r) / 2:
        x1, y1 = (p1.s.x, p1.s.y)
        x2, y2 = (p2.s.x, p2.s.y)
        v1 = p1.v
        v2 = p2.v
        m1 = p1.m
        m2 = p2.m

        n = pygame.math.Vector2(x2 - x1, y2 - y1)
        un = n.normalize()
        ut = pygame.math.Vector2(-un.y, un.x)

        v1n_i = un.dot(v1)
        v1t_i = ut.dot(v1)
        v2n_i = un.dot(v2)
        v2t_i = ut.dot(v2)
        
        v1n_f = (v1n_i * (m1 - m2) + 2 * m2 * v2n_i) / (m1 + m2)
        v1t_f = v1t_i
        v2n_f = (v2n_i * (m2 - m1) + 2 * m1 * v1n_i) / (m1 + m2)
        v2t_f = v2t_i

        v1n_f = v1n_f * un
        v1t_f = v1t_f * ut
        v2n_f = v2n_f * un
        v2t_f = v2t_f * ut

        p1.v = v1n_f + v1t_f
        p2.v = v2n_f + v2t_f

        overlap = p1.r + p2.r - distance
        p1.s -= un * (overlap / 2)
        p2.s += un * (overlap / 2)

        while (p1.s - p2.s).magnitude() < p1.r + p2.r:
            p1.s -= un * 0.01
            p2.s += un * 0.01
        p1.s -= un * 0.01
        p2.s += un * 0.01

def ensure_within_bounds(particle: Particle, box: Box):
    if particle.s.x - particle.r < box.left:
        particle.s.x = box.left + particle.r
    elif particle.s.x + particle.r > box.right:
        particle.s.x = box.right - particle.r

    if particle.s.y - particle.r < box.top:
        particle.s.y = box.top + particle.r
    elif particle.s.y + particle.r > box.bottom:
        particle.s.y = box.bottom - particle.r

def calculate_average_detections():
    if not num_collision_detections:
        return
    
    total = sum(num_collision_detections)
    average = total / len(num_collision_detections)
    print(f"Average collision detections per frame: {average:.2f}")

def get_memory_usage():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_usage_in_mb = memory_info.rss / (1024 * 1024)
    return memory_usage_in_mb

def calculate_average_memory_usage():
    if not memory_usage_array:
        return
    
    total = sum(memory_usage_array)
    average = total / len(memory_usage_array)
    print(f"Average memory used: {average:.2f} MB")

def place_particles_in_cells(box: Box, particles: list[Particle]):
    for particle in particles:
        left_col = abs(int((particle.s.x - particle.r - box.left) / box.cell_width))
        right_col = abs(int((particle.s.x + particle.r - box.left) / box.cell_width))
        top_row = abs(int((particle.s.y - particle.r - box.top) / box.cell_height))
        bottom_row = abs(int((particle.s.y + particle.r - box.top) / box.cell_height))

        max(0, min(left_col, box.N - 1))
        max(0, min(right_col, box.N - 1))
        max(0, min(top_row, box.N - 1))
        max(0, min(bottom_row, box.N - 1))

        for col in range(left_col, right_col + 1):
            for row in range(top_row, bottom_row + 1):
                box.cells[col][row].append(particle)

def visualize_cells(cells):
    lines = []
    for row in range(len(cells)):
        line = ""
        for col in range(len(cells[row])):
            line += "[" + ", ".join([particle.name for particle in cells[col][row]]) + "] "
        lines.append(line)
    return "\n".join(lines)

def main():
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    box = Box()
    started = True

    particles: list[Particle] = []
    for i in range(10):
        new_particle = Particle()
        new_particle.name = str(i)
        particles.append(new_particle)

    start_time = time.time()

    while run:
        clock.tick(30)
        WINDOW.fill(BLACK)

        box.draw(WINDOW)
        box.uniform_grid_partition(WINDOW, 3)
        place_particles_in_cells(box, particles)
        # if started:
        #     print("--------------")
        #     print(visualize_cells(box.cells))

        num_collisions_detected_this_frame = 0
        for i in range(len(box.cells)):
            for j in range(len(box.cells[i])):
                cell_particles = box.cells[i][j]
                for k in range(len(cell_particles)):
                    for l in range(k + 1, len(cell_particles)):
                        handle_particle_collision(cell_particles[k], cell_particles[l])
                        num_collisions_detected_this_frame += 1
        num_collision_detections.append(num_collisions_detected_this_frame)
        # calculate_average_detections()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                started = not started
        
        for p in particles:
            p.draw(WINDOW, box)
            if started:
                p.update(dt, box)
                ensure_within_bounds(p, box)

        box.clear_uniform_grid_cells()
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 60:
            run = False

        pygame.display.update()
        memory_usage_array.append(get_memory_usage())
    pygame.quit()
    calculate_average_detections()
    calculate_average_memory_usage()

main()



