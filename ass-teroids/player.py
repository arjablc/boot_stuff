from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOT_COOLDOWN_SECONDS,
    PLAYER_SHOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
import pygame

import constants
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0

        # in the Player class

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        points = self.triangle()
        # pygame.draw.circle(screen, "red", self.position, PLAYER_RADIUS, LINE_WIDTH)
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unitVector = pygame.Vector2(0, 1)
        rotated = unitVector.rotate(self.rotation)
        moved = rotated * PLAYER_SPEED * dt
        self.position += moved

    def shoot(self):
        if self.timer > 0:
            return
        self.timer = PLAYER_SHOT_COOLDOWN_SECONDS
        shot = Shot(position=self.position)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOT_SPEED

    def update(self, dt):
        self.timer -= dt
        # this is required to be done in arch and hyprland
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
