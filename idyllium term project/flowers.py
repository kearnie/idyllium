# for sprouting on-click flowers
import pygame
import random
import copy


class Flower(pygame.sprite.Sprite):
    def __init__(self, x, y, completed, world):
        super(Flower, self).__init__()
        self.x, self.y = x, y  # event x, event y of mousepress
        self.speed = .3  # for when they fall
        self.completed = completed
        self.isFalling = False
        self.colors = [(255, 243, 204, random.randint(220, 230)),
                       (233, 204, 255, random.randint(220, 230)),
                       (255, 206, 163, random.randint(220, 230)),
                       (255, 209, 244, random.randint(220, 230)),
                       (250, 251, 255, random.randint(220, 230)),
                       (192, 204, 237, random.randint(220, 230))]
        self.color = random.choice(self.colors)
        self.angle = random.randint(0, 360)
        self.redraw()
        self.image = copy.deepcopy(self.baseImage)
        self.growTime = 1
        self.growRate = self.growTime / world.tickRate

    def update(self, screenWidth, screenHeight):
        if self.isFalling == True:
            self.y += self.speed
            self.angle = (self.angle + 1) % 360
        self.completed = min(1, self.completed + self.growRate)
        self.redraw()
        self.image = copy.copy(self.baseImage)
        self.getRect()

    def getRect(self):
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - self.length, self.y - self.length,
                                w, h)

    def redraw(self):
        x, y = self.x, self.y
        self.width = 8 * self.completed
        self.length = 14 * self.completed  # ???

        self.baseImage = pygame.Surface((2 * self.length, 2 * self.length),
                                        pygame.SRCALPHA)
        self.baseImage = self.baseImage.convert_alpha()
        petal1x1, petal1y1 = self.length - self.width / 2, 0  # up petal
        petal1x2, petal1y2 = self.width, self.length
        petal2x1, petal2y1 = self.length, self.length - self.width / 2  # right petal
        petal2x2, petal2y2 = self.length, self.width
        petal3x1, petal3y1 = self.length - self.width / 2, self.length  # down petal
        petal3x2, petal3y2 = self.width, self.length
        petal4x1, petal4y1 = 0, self.length - self.width / 2  # left petal
        petal4x2, petal4y2 = self.length, self.width
        pygame.draw.ellipse(self.baseImage, self.color,
                            (petal1x1, petal1y1, petal1x2, petal1y2), 0)
        pygame.draw.ellipse(self.baseImage, self.color,
                            (petal2x1, petal2y1, petal2x2, petal2y2), 0)
        pygame.draw.ellipse(self.baseImage, self.color,
                            (petal3x1, petal3y1, petal3x2, petal3y2), 0)
        pygame.draw.ellipse(self.baseImage, self.color,
                            (petal4x1, petal4y1, petal4x2, petal4y2), 0)
