import pygame
from Box import Box
from Particle import Particle
from Constants import BLACK

pygame.init()
WIDTH, HEIGHT = (1244, 700)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Simulation")

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

num_collision_detections = list()

def calculate_average_detections():
    if not num_collision_detections:
        print("No collision detections recorded.")
        return
    
    total = sum(num_collision_detections)
    average = total / len(num_collision_detections)
    print(f"Average collision detections per frame: {average:.2f}")
    

def main():
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    box = Box()
    started = False

    particles: list[Particle] = []
    for i in range(200):
        new_particle = Particle(box)
        new_particle.name = str(i)
        particles.append(new_particle)

    while run:
        clock.tick(30)
        WINDOW.fill(BLACK)

        box.draw(WINDOW)

        num_collisions_detected_this_frame = 0
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                handle_particle_collision(particles[i], particles[j])
                num_collisions_detected_this_frame += 1
        num_collision_detections.append(num_collisions_detected_this_frame)
        calculate_average_detections()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                started = not started
        
        for p in particles:
            p.draw(WINDOW)
            if started:
                p.update(dt)
                ensure_within_bounds(p, box)

        pygame.display.update()
    pygame.quit()

main()



