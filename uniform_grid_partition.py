import pygame
from Box import Box
from Particle import Particle
from Constants import BLACK
import time
from MemoryTracker import MemoryTracker
from CollisionsUtil import handle_particle_collision, ensure_within_bounds

pygame.init()
WIDTH, HEIGHT = (800, 800)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Simulation")

num_collision_detections = list()

def calculate_average_detections():
    if not num_collision_detections:
        return
    
    total = sum(num_collision_detections)
    average = total / len(num_collision_detections)
    print(f"Average collision detections per frame: {average:.2f}")

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

        [left_col, right_col, top_row, bottom_row] = [(index if index <= box.N - 1 else box.N - 1) for index in [left_col, right_col, top_row, bottom_row]]

        for col in range(left_col, right_col + 1):
            for row in range(top_row, bottom_row + 1):
                # print(str(col) + str(row))
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

    memory_tracker = MemoryTracker()

    box = Box()
    started = True

    num_particles = 2
    particles: list[Particle] = []
    for i in range(num_particles):
        new_particle = Particle()
        new_particle.name = str(i)
        particles.append(new_particle)

    start_time = time.time()

    while run:
        clock.tick(30)
        WINDOW.fill(BLACK)

        box.draw(WINDOW)
        box.uniform_grid_partition(WINDOW, 4)
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
                        memory_tracker.update_memory_usage_array()
                        num_collisions_detected_this_frame += 1
        num_collision_detections.append(num_collisions_detected_this_frame)

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
    pygame.quit()
    print("N: " + str(box.N) + ", " + str(num_particles) + " particles")
    calculate_average_detections()
    memory_tracker.calculate_average_memory_usage()

main()



