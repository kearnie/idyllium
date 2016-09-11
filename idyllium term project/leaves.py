# for growing leaves
from berries import *
import pygame
import random
import copy

from utility import *


class Leaf(pygame.sprite.Sprite):
    def __init__(self, world, x, y):
        super().__init__()
        self.world = world
        self.width = random.randint(15, 20)
        self.length = random.randint(25, 28)
        self.x, self.y = x, y
        self.x -= self.width / 4
        self.y -= self.length / 4
        self.isFalling = False
        self.speed = .3  # for when leaves fall
        self.rect = pygame.Rect(x, y, x + self.width, y + self.length)
        self.image = pygame.Surface((self.width, self.length),
                                    pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.baseImage = copy.copy(self.image)
        self.colors = [(138, 204, 116, random.randint(100, 200)),
                       (60, 186, 100, random.randint(100, 200)),
                       (3, 161, 87, random.randint(100, 200)),
                       (90, 199, 117, random.randint(100, 200))]
        self.colorInd = random.randint(0, len(self.colors) - 1)
        self.color = self.colors[self.colorInd]
        self.x2, self.y2 = self.width, self.length
        self.angle = random.randint(0, 360)
        self.dirty = True

    def updateColor(self, temp):
        (r, g, b, a) = self.colors[self.colorInd]
        newcolor = None
        if temp >= 70:
            newcolor = self.colors[self.colorInd]
        elif temp <= 20:
            newcolor = boundsColor((r - 3 * (20 - 70), g + (20 - 70), b + (20 - 70), a))
        else:
            newcolor = boundsColor((r - 3 * (temp - 70), g + (temp - 70), b + (temp - 70), a))
        if self.color != newcolor:
            self.color = newcolor
            self.dirty = True

    def getRect(self):
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x, self.y,
                                self.x + self.width, self.y + self.length)

    def update(self, screenWidth, screenHeight):
        if self.isFalling:
            self.y += self.speed
            magnitudeOfVariation = self.world.windSpeed / 2
            randomVariation = (random.random() * magnitudeOfVariation - 
                               (magnitudeOfVariation / 2))
            self.x += self.world.windSpeed + randomVariation
            self.angle += 1
            self.dirty = True
        if self.dirty:
            pygame.draw.ellipse(self.baseImage, self.color,
                                (0, 0, self.x2, self.y2), 0)
            self.image = pygame.transform.rotate(self.baseImage, self.angle)
            self.dirty = False
        self.getRect()

    def addBerry(self, world):
        berryProb = .03
        if random.random() < berryProb:
            berry = Berry(world, random.randint(int(self.x), int(self.x + self.width)),
                          random.randint(int(self.y), int(self.y + self.length)))
            world.flowers.add(berry)
