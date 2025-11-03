import pygame

class Player():
    def __init__(self, game, position, velocity, acceleration, size, color):
        self.game = game
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.size = size
        self.color = color
        self.isJumpButtonReleased = True

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = position

    def jump(self):
        self.velocity.y = -10

    def draw(self, surf):
        pygame.draw.ellipse(surf, self.color, self.rect)

    def update(self, surf):
        # draw player
        self.draw(surf)

        # handle jumping
        keys = pygame.key.get_pressed()
        is_space_pressed = keys[pygame.K_SPACE]
        is_mouse_pressed = pygame.mouse.get_pressed()[0]
        if self.isJumpButtonReleased and (is_space_pressed or is_mouse_pressed):
            self.jump()
            self.isJumpButtonReleased = False
        if not is_space_pressed and not is_mouse_pressed:
            self.isJumpButtonReleased = True

        # update kinematics values
        # self.rect.move_ip(self.velocity * self.game.delta_time)
        self.velocity += self.acceleration * self.game.delta_time
        self.position += self.velocity
        self.rect.center = self.position
        