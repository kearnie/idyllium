# for spawning animals
import pygame
import random

from interaction import Interactable
from utility import almostEqual, randfloat


class Birds(pygame.sprite.Group):
    def __init__(self, world):
        super().__init__()
        self.maxBirds = 7
        self.world = world
        self.prob = 1 / (30 * 23)

    def onTick(self):
        if (random.random() < self.prob and len(self.sprites()) < self.maxBirds):
            self.add(Bird(self.world, random.randint(1, 450), 610))


class Bird(Interactable):
    def __init__(self, world, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.xSpeed = randfloat(-2, 2)
        self.ySpeed = randfloat(-2, 2)
        self.desiredYSpeed = self.ySpeed
        self.desiredXSpeed = self.xSpeed
        self.maxSpeedChancePerTick = .12
        self.rect = pygame.Rect(self.x, self.y, 55, 31)
        self.loadImages()
        self.imageIndex = 0
        self.image = self.images[self.imageIndex]
        self.color = [(135, 145, 156, random.randint(40, 100)),
                      (127, 144, 161, random.randint(40, 100))]  # color options
        self.deathFlag = False
        self.click = True
        self.priority = -10
        world.interactionHandler.register(self)

    def loadImages(self):
        self.images = []
        amount = 8
        for i in range(1, amount + 1):
            name = "assets/bird0" + str(i) + ".png"
            self.images.append(pygame.image.load(name).convert_alpha())

    def onClick(self, mouseX, mouseY):
        print("wwhy")

    def getRect(self):
        self.rect = pygame.Rect(self.x, self.y, 55, 31)

    def update(self, screenWidth, screenHeight):
        prob = .006

        self.imageIndex = (self.imageIndex + 1) % (len(self.images) * 2)
        self.image = self.images[self.imageIndex // 2]
        if random.random() < prob and not self.deathFlag:  # have birds change flight direction at random
            self.desiredXSpeed = randfloat(-2, 2)
            self.desiredYSpeed = randfloat(-2, 2)
        if not almostEqual(self.xSpeed, self.desiredXSpeed) or not almostEqual(self.desiredYSpeed, self.ySpeed):
            dx = self.desiredXSpeed - self.xSpeed
            dy = self.desiredYSpeed - self.ySpeed
            # bound the max change in speed per tick for more natural look
            if abs(dx) > self.maxSpeedChancePerTick:
                dx = (dx / abs(dx)) * self.maxSpeedChancePerTick  # Get sign of change and times by max change
            if abs(dy) > self.maxSpeedChancePerTick:
                dy = (dy / abs(dy)) * self.maxSpeedChancePerTick
            self.xSpeed += dx
            self.ySpeed += dy

        self.x += self.xSpeed
        self.y += self.ySpeed
        if (self.x < 0 or self.x > screenWidth or self.y < 0 or self.y > screenHeight) and self.deathFlag:
            self.kill()
            print("bird killed")

        if self.x < 0:
            self.x = screenWidth
        elif self.x > screenWidth:
            self.x = 0
        if self.y < 0:
            self.y = screenHeight
        elif self.y > screenHeight:
            self.y = 0
        self.getRect()
