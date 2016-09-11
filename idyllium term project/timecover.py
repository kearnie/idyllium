# overall daytime,nighttime cycle 

import pygame
import math


class Time(pygame.sprite.Sprite):
    def __init__(self, world):
        super().__init__()
        self.world = world
        self.image = pygame.Surface((450, 620), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(0, 0, 450, 620)
        self.updateColor(world)

    def updateColor(self, world):
        time = world.time
        level = 250 * math.sin((2 * math.pi * time / 1000))
        if level > 200:
            level = 200
        elif level < 0:
            level = 0
        self.color = (0, 30, 51, level)

    def getRect(self):
        self.rect = pygame.Rect(0, 0, 450, 620)

    def update(self, screenWidth, screenHeight):
        self.getRect()
        self.updateColor(self.world)
        pygame.draw.rect(self.image, self.color, (0, 0, 450, 620), 0)
