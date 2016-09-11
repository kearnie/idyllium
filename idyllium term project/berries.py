# for spawning berries on tree
# can be clicked on to be collected -> inventory
# used to feed birds to have them fly off-screen

import pygame
import random

from interaction import *


class Berry(Interactable):
    def __init__(self, world, x, y):
        super().__init__()
        self.radius = 5
        self.world = world
        self.x, self.y = x, y
        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.color = [(28, 59, 163, 190),
                      (230, 57, 57, 190),
                      (255, 156, 207, 190),
                      (255, 145, 0, 190),
                      (0, 138, 145, 190),
                      (0, 148, 222, 190),
                      (191, 34, 134, 190)]  # color options
        pygame.draw.circle(self.image, random.choice(self.color),
                           (self.radius, self.radius), self.radius)
        self.click = True
        self.priority = -1
        world.interactionHandler.register(self)

    def onClick(self, x, y):
        self.world.inventory.berryAmount += 1
        self.kill()
        self.world.ui.inventoryView.updateAmounts()

    def getRect(self):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def update(self, screenWidth, screenHeight):
        self.getRect()
