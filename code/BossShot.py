import pygame
from code.Const import ENTITY_SPEED
from code.Entity import Entity


class BossShot(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.surf = pygame.transform.scale(self.surf, (40, 40))
        self.rect = self.surf.get_rect(left=position[0], top=position[1])

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]