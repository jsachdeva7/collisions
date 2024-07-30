import pygame
from Box import Box
from Particle import Particle
from Constants import BLACK
import time
from MemoryTracker import MemoryTracker
from CollisionsUtil import handle_particle_collision, ensure_within_bounds, calculate_average_detections

num_collision_detections = []
FONT = pygame.font.SysFont("calibri", 25)

def place_particles_in_cells(box: Box, particles: list[Particle]):
    for particle in particles:
        left_col = max(0, min(int((particle.s.x - particle.r - box.left) / box.cell_width), box.N - 1))
        right_col = max(0, min(int((particle.s.x + particle.r - box.left) / box.cell_width), box.N - 1))
        top_row = max(0, min(int((particle.s.y - particle.r - box.top) / box.cell_height), box.N - 1))
        bottom_row = max(0, min(int((particle.s.y + particle.r - box.top) / box.cell_height), box.N - 1))

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

quit = False

def main(num_particles, N):
    pygame.display.quit()
    pygame.display.init()
    WIDTH, HEIGHT = (800, 800)
    WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Collision Simulation")
    pygame.display.iconify()

    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    memory_tracker = MemoryTracker()

    box = Box()
    started = True

    particles: list[Particle] = []
    for i in range(num_particles):
        new_particle = Particle(box)
        new_particle.name = str(i)
        particles.append(new_particle)

    start_time = time.time()

    while run:
        clock.tick(fps)
        WINDOW.fill(BLACK)

        desc = FONT.render("N = " + str(N) + ", " + str(num_particles) + " particles", 1, (255, 255, 255))
        WINDOW.blit(desc, (WIDTH / 2 - desc.get_width() / 2, box.top - 30))

        box.draw(WINDOW)
        box.uniform_grid_partition(WINDOW, N)
        place_particles_in_cells(box, particles)

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
        collision_checks_text = FONT.render(str(num_collisions_detected_this_frame) + " collisions checked this frame.", 1, (255, 255, 255))
        WINDOW.blit(collision_checks_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                started = not started
        
        for p in particles:
            p.draw(WINDOW)
            if started:
                p.update(dt)
                ensure_within_bounds(p, box)

        box.clear_uniform_grid_cells()
        elapsed_time = time.time() - start_time
        if elapsed_time >= 60:
            run = False

        pygame.display.update()
    
    average_detections_str = calculate_average_detections(num_collision_detections)
    average_memory_usage_str = memory_tracker.calculate_average_memory_usage()
    result = f"{num_particles} particles: {average_detections_str}, {average_memory_usage_str}"
    return result

def run_tests(num_particles_array, num_grid_cuts):  
    for N in num_grid_cuts:
        results = []
        for num_particles in num_particles_array:
            result = main(num_particles, N)
            if result == False:
                return
            results.append(result)
            num_collision_detections.clear()
        print("----- " + str(N) + " cuts -----")
        for result in results:
            print(result)

num_particles_array = [2, 5, 20, 100, 200, 300, 500]
num_grid_cuts = [2, 4, 8, 16]
results = run_tests(num_particles_array, num_grid_cuts)
pygame.quit()
