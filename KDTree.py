import pygame
from Particle import Particle
from LinkedList import LinkedList
from CollisionsUtil import handle_particle_collision

FONT = pygame.font.SysFont("comicsans", 15)

class KDNode():
    def __init__(self, point: tuple[float], particles: list[Particle], top_left = tuple[float], bot_right = tuple[float], axis: int = 0, left: 'KDNode' = None, right: 'KDNode' = None):
        self.point = point
        self.particles = particles
        self.top_left = top_left
        self.bot_right = bot_right
        self.axis = axis
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

class KDTree():
    def __init__(self, window: pygame.Surface):
        self.root = None
        self.window = window
        self.leaf_count = 0

    def build(self, particles_linked: LinkedList, top_left: tuple[float], bot_right: tuple[float]):
        particles = particles_linked.to_list()
        self.root = self._build_recursive(particles, top_left, bot_right, 5)
        
    def _build_recursive(self, particles: list[Particle], top_left: tuple[float], bot_right: tuple[float], max_num_divisions: int, depth: int = 0):
        if not particles or depth > max_num_divisions:
            return None
    
        axis = depth % 2
        vertical_split = axis == 0
        horizontal_split = axis == 1

        # Sort particles by the axis being split
        particles.sort(key=lambda particle: particle.s[axis])
        if len(particles) % 2 == 1:
            median_point = particles[len(particles) // 2].s
        else:
            particle_1_s = particles[int(len(particles) / 2) - 1].s
            particle_2_s = particles[int(len(particles) / 2)].s
            median_point = (particle_1_s + particle_2_s) / 2
        median_index = len(particles) // 2
        
        # Define new boundaries (different for left and right subtrees)
        if vertical_split:  
            new_top_left_left = top_left
            new_bot_right_left = (median_point[0], bot_right[1])
            
            new_top_left_right = (median_point[0], top_left[1])
            new_bot_right_right = bot_right
        elif horizontal_split:  
            new_top_left_left = top_left
            new_bot_right_left = (bot_right[0], median_point[1])
            
            new_top_left_right = (top_left[0], median_point[1])
            new_bot_right_right = bot_right

        node = KDNode(
            particles[median_index],
            particles,
            top_left,
            bot_right,
            axis
        )

        node.left = self._build_recursive(
            particles[:median_index], 
            new_top_left_left, 
            new_bot_right_left, 
            max_num_divisions, 
            depth + 1
        )
        
        node.right = self._build_recursive(
            particles[median_index:], 
            new_top_left_right, 
            new_bot_right_right, 
            max_num_divisions, 
            depth + 1
        )
        return node
    
    def traverse_tree(self, node: KDNode, started: bool):
        if node is None:
            return
        self.traverse_tree(node.left, started)
        if node.is_leaf():
            rect = pygame.Rect(node.top_left[0], node.top_left[1], abs(node.bot_right[0] - node.top_left[0]), abs(node.bot_right[1] - node.top_left[1]))
            pygame.draw.rect(self.window, (255, 255, 255), rect, 1)
            self.leaf_count += 1
            number = FONT.render(str(self.leaf_count), 1, (255, 255, 255))
            self.window.blit(number, (node.top_left[0] + 5, node.top_left[1] + 5))
            if started: print("Region " + str(self.leaf_count) + ": " + str(len(node.particles)))
            for i in range(len(node.particles)):
                for j in range(i + 1, len(node.particles)):
                    handle_particle_collision(node.particles[i], node.particles[j])
        self.traverse_tree(node.right, started)
    
