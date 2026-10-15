import random
import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += dt * self.velocity

    def split(self):
        self.kill()
        if self.radius < ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        rand_angle = random.uniform(20, 50)
        vel1 = self.velocity.rotate(rand_angle)
        vel2 = self.velocity.rotate(-rand_angle)

        c_as1 = Asteroid(
            self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS
        )
        c_as2 = Asteroid(
            self.position.x, self.position.y, self.radius - ASTEROID_MIN_RADIUS
        )
        c_as1.velocity = vel1 * 1.2
        c_as2.velocity = vel2 * 1.2
