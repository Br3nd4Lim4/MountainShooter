import math
import pygame
from code.Entity import Entity
from code.BossShot import BossShot


class Boss(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = 60
        self.init_y = position[1]

    def move(self):
        self.rect.centery = self.init_y + math.sin(pygame.time.get_ticks() * 0.005) * 50

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay <= 0:
            self.shot_delay = 60
            return BossShot(name='BossShot', position=(self.rect.left, self.rect.centery))
