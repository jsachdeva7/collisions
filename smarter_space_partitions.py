import pygame
from Box import Box
from Particle import Particle
from Constants import BLACK
import time
from MemoryTracker import MemoryTracker
from CollisionsUtil import handle_particle_collision, ensure_within_bounds, calculate_average_detections
from LinkedList import LinkedList, Node

pygame.init()
WIDTH, HEIGHT = (800, 800)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Simulation")

num_collision_detections = list()

def main():
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    memory_tracker = MemoryTracker()

    box = Box()
    started = True

    num_particles = 5
    particles_linked_x = LinkedList()
    for i in range(num_particles):
        new_particle = Particle()
        new_particle.name = str(i)
        particles_linked_x.append(new_particle)

    cur_node: Node = particles_linked_x.head.next
    particles_linked_y = LinkedList()
    while cur_node and cur_node.next:
        particles_linked_y.append(cur_node.data)
        cur_node = cur_node.next
    particles_linked_y.append(cur_node.data)

    start_time = time.time()

    while run:
        clock.tick(30)
        WINDOW.fill(BLACK)

        box.draw(WINDOW)

        if started:
            print("-------")
            particles_linked_x.sort('x')
            print("x:")
            particles_linked_x.display('x')
            particles_linked_y.sort('y')
            print("y:")
            particles_linked_y.display('y')

        cur_node: Node = particles_linked_x.head.next
        while cur_node and cur_node.next:
            cur_node.data.draw(WINDOW, box)
            if started:
                cur_node.data.update(dt, box)
                ensure_within_bounds(cur_node.data, box)
            cur_node = cur_node.next

        if cur_node:
            cur_node.data.draw(WINDOW, box)
            if started:
                cur_node.data.update(dt, box)
                ensure_within_bounds(cur_node.data, box)

        num_collisions_detected_this_frame = 0

        # collision detection framework

        num_collision_detections.append(num_collisions_detected_this_frame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                started = not started

        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= 60:
            run = False

        pygame.display.update()
    pygame.quit()
    print("N: " + str(box.N) + ", " + str(num_particles) + " particles")
    calculate_average_detections(num_collision_detections)
    memory_tracker.calculate_average_memory_usage()

main()



