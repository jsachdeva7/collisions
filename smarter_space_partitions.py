import pygame
from Box import Box
from Particle import Particle
from Constants import BLACK
import time
from MemoryTracker import MemoryTracker
from CollisionsUtil import handle_particle_collision, ensure_within_bounds, calculate_average_detections
from LinkedList import LinkedList, Node
from KDTree import KDTree

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

    num_particles = 50
    particles_linked = LinkedList()
    for i in range(num_particles):
        new_particle = Particle()
        new_particle.name = str(i)
        particles_linked.append(new_particle)

    kd_tree = KDTree(WINDOW)

    start_time = time.time()

    while run:
        clock.tick(30)
        WINDOW.fill(BLACK)

        box.draw(WINDOW)

        if started:
            kd_tree.build(particles_linked, (box.left, box.top), (box.right, box.bottom))
        kd_tree.leaf_count = 0
        kd_tree.traverse_tree(kd_tree.root, started)
        if started: print("-------------")

        cur_node: Node = particles_linked.head.next
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
        # if elapsed_time >= 60:
        #     run = False

        pygame.display.update()
    pygame.quit()
    # print("N: " + str(box.N) + ", " + str(num_particles) + " particles")
    # calculate_average_detections(num_collision_detections)
    # memory_tracker.calculate_average_memory_usage()

main()



