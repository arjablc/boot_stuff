import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position.x, position.y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 0)

    def update(self, dt):
        self.position += self.velocity * dt
