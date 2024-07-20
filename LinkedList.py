from Particle import Particle
import random
import pygame

class Node:
    def __init__(self, data: Particle = None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = Node()

    def append(self, data: Particle):
        new_node = Node(data)
        cur = self.head
        while cur.next != None:
            cur = cur.next
        cur.next = new_node

    def length(self):
        cur = self.head
        count = 0
        while cur.next != None:
            count += 1
            cur = cur.next
        return count
    
    def display(self, axis: str):
        elems = []
        cur_node = self.head
        while cur_node.next != None:
            cur_node = cur_node.next
            elems.append(cur_node.data.name + ": " + str(int(round((cur_node.data.s.x if axis == 'x' else cur_node.data.s.y), 0))))
        print(elems)
    
    def get(self, index):
        if index >= self.length():
            print("Error w/ get(): Index out of bounds")
            return None
        i = 0
        cur_node = self.head
        while True:
            if i == index: return cur_node.data
            cur_node = cur_node.next
            i += 1

    def sort(self, axis):
        sorted_list = None
        cur_node = self.head.next  # Start from the first actual node

        while cur_node:
            next_node = cur_node.next  # Save the next node
            sorted_list = self.sorted_insert(sorted_list, cur_node, axis)
            cur_node = next_node  # Move to the next node

        # Attach sorted list to dummy head
        self.head.next = sorted_list

    def sorted_insert(self, head: Node, node: Node, axis: str):
        if not head or (node.data.s.x < head.data.s.x if axis == 'x' else node.data.s.y < head.data.s.y):  # Sort by x position
            node.next = head
            head = node
        else:
            current = head
            while current.next and ((current.next.data.s.x < node.data.s.x) if axis == 'x' else (current.next.data.s.y < node.data.s.y)):
                current = current.next
            node.next = current.next
            current.next = node
        return head
    
    def to_list(self):
        elements = []
        current = self.head.next
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    # def remove(self, index):
    #     if index >= self.length():
    #         print("Error w/ erase(): Index out of bounds")
    #         return
    #     i = 0
    #     cur_node = self.head
    #     while True:
    #         last_node = cur_node
    #         cur_node = cur_node.next
    #         if i == index:
    #             last_node.next = cur_node.next
    #         i += 1

