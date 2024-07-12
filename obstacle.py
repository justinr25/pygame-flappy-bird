import pygame

class Obstacle():
    def __init__(self, position, velocity, size, color):
        self.position = position
        self.velocity = velocity
        self.size = size
        self.color = color
        self.passed = False

        self.rect = pygame.Rect(position, size)

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

    def update(self, surf):
        # draw obstacle
        self.draw(surf)

        # update kinematics values
        self.rect.move_ip(self.velocity)
        # self.position += self.velocity
        # self.rect.bottomleft = self.position