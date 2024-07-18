import pygame
from Particle import Particle
from Box import Box

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