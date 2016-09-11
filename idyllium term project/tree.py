# for tree / branch segments
from flowers import Flower
from gameobject import *

from main import World
from leaves import *
import pygame
import random
import perlin
import math


class Tree(pygame.sprite.RenderUpdates):
    def __init__(self):
        super().__init__()


class Branchsegment(GameObject):
    def __init__(self, world, x1, y1, x2, y2, thickness=30):
        self.thickness = thickness
        self.world = world
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        tlx = min(self.x1, self.x2)  # top left x val
        tly = min(self.y1, self.y2)  # top left y val
        self.width = abs(self.x2 - self.x1) + self.thickness + 2
        self.height = abs(self.y2 - self.y1) + self.thickness
        super().__init__(tlx - self.thickness / 2, tly - self.thickness / 2, self.width,
                         self.height)
        x1 += self.thickness / 2
        x2 += self.thickness / 2
        y1 += self.thickness / 2
        y2 += self.thickness / 2
        firstPoint = (x1 - tlx, y1 - tly)
        secondPoint = (x2 - tlx, y2 - tly)
        self.color = (105, 87, 71)
        drawAntiAliasedLine(self.baseImage, self.color,
                            firstPoint, secondPoint, self.thickness)
        self.click = True
        world.interactionHandler.register(self)

    def update(self, screenWidth, screenHeight):
        super().update(screenWidth, screenHeight)

    def onClick(self, mouseX, mouseY):
        flower = Flower(mouseX + self.world.camera.winX, mouseY + 
            self.world.camera.winY,.001, self.world)
        self.world.instance.flowers.add(flower)

    def addLeaf(self, amount, world):
        x1, y1 = self.x1, self.y1
        x2, y2 = self.x2, self.y2
        slope = (y2 - y1) / (x2 - x1)
        constant = y1 - (slope * x1)
        for i in range(amount):
            rx = (x2 - x1) * random.random() + x2
            ry = slope * rx + constant
            spreadFactor = 0
            rx += (random.random() * spreadFactor) - (spreadFactor / 2)
            ry += (random.random() * spreadFactor) - (spreadFactor / 2)
            leaf = Leaf(world, rx, ry)
            leaf.addBerry(world)
            world.tree.add(leaf)


class Trunksegment(Branchsegment):
    def __init__(self, world, x1, y1, x2, y2, thickness=30):
        super().__init__(world, x1, y1, x2, y2, thickness)
        tlx = min(self.x1, self.x2)  # top left x val
        tly = min(self.y1, self.y2)  # top left y val
        points = [(-20, -20), (0, 50), (55, 50), (-20, -20)]

        for y in range(0, self.height):
            noise = perlin.smooth1(0, y)
            noise = abs(noise) * 22
            intn = int(noise)
            noiseFrac = noise - intn
            lastA = noiseFrac * 255


# tree fractal structure by lingdong
# https://github.com/LingDong-/Hermit/blob/master/src/lib/tree.py
def dthickness(thickness, depth):
    return -(thickness / 4)


def dangle(depth):
    return -(random.random() - 0.5) * math.pi / 3


def dlength(length, depth):
    return -(length / 3) * (random.random() + 0.5)


def makeBranch(world, x1, y1, initAngle):
    if initAngle != 0:
        initAngle += (abs(dangle(1)) + math.pi / 14)
    else:
        initAngle -= abs(dangle(1) + math.pi / 14)
    branch(world, initAngle, 30 * random.random() + 75, x1, y1, 10, 0)


def splitProb(depth):
    return .55 + .65 * (1 / (depth + 1))


def contProb(depth):
    if depth < 2:
        return 1
    return .35 + .15 * (1 / depth)


def branch(world, angle, length, x1, y1, thickness, depth):
    # base case
    if random.random() >= contProb(depth) or thickness == 1: return
    # recursive case
    angle = angle + dangle(depth)
    thickness = max(1, thickness + dthickness(thickness, depth))
    length = length + dlength(length, depth)
    x2, y2 = x1 + math.cos(angle) * length, y1 + math.sin(angle) * length
    branchSegment = Branchsegment(world, x1, y1, x2, y2, thickness)
    world.tree.add(branchSegment)
    branchSegment.addLeaf(leafAmount(world), world)
    if random.random() < splitProb(depth):
        branch(world, angle, length, x2, y2, thickness, depth + 1)
    branch(world, angle, length, x2, y2, thickness, depth + 1)


def leafAmount(world):
    return int(0.08 * world.storm.temp)
