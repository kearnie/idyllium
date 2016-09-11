# for atmosphere, light, weather
import pygame
import random

from pygame.mixer import Sound

from utility import almostEqual, drawAntiAliasedPolygon


class Atmosphere(pygame.sprite.Group):
    def __init__(self):
        super().__init__()


class Light(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lightLevel = 20
        self.image = pygame.Surface((450, 620), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = pygame.Rect(0, 0, 450, 620)
        self.updateColor()
        self.dirtyCounter = 10
        self.lastDrawnLightLevel = self.lightLevel
        self.redraw()

    def updateColor(self):
        self.color = (255, 255, 255, self.lightLevel)

    def getRect(self):
        self.rect = pygame.Rect(0, 0, 450, 620)

    def redraw(self):
        self.getRect()
        self.updateColor()
        drawAntiAliasedPolygon(self.image, self.color,
                               [(150, 0), (185, 0), (130, 620), (40, 620)])
        drawAntiAliasedPolygon(self.image, self.color,
                               [(190, 0), (290, 0), (360, 620), (140, 620)])
        drawAntiAliasedPolygon(self.image, self.color,
                               [(295, 0), (310, 0), (400, 620), (370, 620)])
        self.lastDrawnLightLevel = self.lightLevel

    def update(self, screenWidth, screenHeight):
        if self.lightLevel > 200:
            self.lightLevel = 200
        if self.lightLevel < 0:
            self.lightLevel = 0
        if (self.lightLevel != self.lastDrawnLightLevel):
            self.dirtyCounter -= 1
            if (self.dirtyCounter < 0):
                self.redraw()
                self.dirtyCounter = 5


class Storm(pygame.sprite.Group):  # handles precipitation
    def __init__(self):
        super().__init__()
        self.amount = 0
        self.temp = 70  # starting temperature
        self.isSoundPlaying = False
        self.volume = 0
        fadeTicks = 100
        self.dVolumePerTick = 1 / fadeTicks
        self.rainSound = Sound("assets/rain.ogg")
        self.rainSound.set_volume(.7)
        self.snowSound = Sound("assets/snow.ogg")
        self.sound = self.rainSound

    def adjust(self, n):
        diff = n - self.amount
        if (diff > 0):  # increase precip
            for i in range(diff):
                if self.temp > 32:  # warmer -> rain (above freezing)
                    drop = Rain(random.randint(1, 450), random.randint(1, 620))
                    self.add(drop)
                else:  # temp<32  # colder -> snow (below freezing)
                    flake = Snow(random.randint(1, 450), random.randint(1, 620))
                    self.add(flake)
        elif (diff < 0):  # decrease precip
            self.remove(self.sprites()[0:abs(diff)])
        self.amount = max(0, n)
        if (self.amount > 0 and not self.isSoundPlaying):
            self.sound.play(fade_ms=2500, loops=-1)
            self.isSoundPlaying = True

    def update(self, screenWidth, screenHeight):
        if (self.temp > 32):
            sound = self.rainSound
        else:
            sound = self.snowSound
        if (sound != self.sound):
            if (self.isSoundPlaying):
                self.sound.fadeout(2500)
                self.sound = sound
                self.sound.play(loops=-1, fade_ms=2000)
            else:
                self.sound = sound
        super().update(screenWidth, screenHeight)
        if self.amount <= 0 and self.isSoundPlaying:
            self.sound.fadeout(2500)
            self.isSoundPlaying = False

        if self.temp < 32:
            diff = 32 - self.temp
            prob = diff / 100  # set probability to change type of precip by temp
            toRemove = []
            for sprite in self.sprites():
                if (type(sprite) == Rain):
                    if random.random() < prob:
                        toRemove.append(sprite)  # move to an aux list to change
            for sprite in toRemove:
                self.remove(sprite)  # remove rain, then replace with snow
                self.add(Snow(random.randint(1, 450), random.randint(1, 620)))
        elif self.temp > 32:
            diff = self.temp - 32
            prob = diff / 100
            toRemove = []
            for sprite in self.sprites():
                if (type(sprite) == Snow):
                    if random.random() < prob:
                        toRemove.append(sprite)
            for sprite in toRemove:
                self.remove(sprite)  # remove snow, then replace with rain
                self.add(Rain(random.randint(1, 450), random.randint(1, 620)))


class Rain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Rain, self).__init__()
        self.length = random.randint(18, 26)  # lengths of raindrops
        self.x, self.y = x, y
        self.speed = random.randint(1, 4)  # possible falling speeds
        self.rect = pygame.Rect(x - self.length, y - self.length,
                                2 * self.length, 2 * self.length)
        self.image = pygame.Surface((2 * self.length, 2 * self.length),
                                    pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.color = [(139, 174, 199, random.randint(20, 100)),
                      (97, 122, 140, random.randint(20, 100))]  # color options
        x2 = self.x
        y2 = self.y + self.length
        pygame.draw.rect(self.image, random.choice(self.color),
                         (0, 0, 1, self.length))

    def getRect(self):
        self.rect = pygame.Rect(self.x - self.length, self.y - self.length,
                                2 * self.length, 2 * self.length)

    def update(self, screenWidth, screenHeight):
        self.y += self.speed  # rain falling
        if self.y < 0:
            self.y = screenHeight
        elif self.y > screenHeight:
            self.y = 0
        self.getRect()


class Snow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Snow, self).__init__()
        self.radius = random.randint(4, 6)  # sizes of snowflakes
        self.x, self.y = x, y
        self.speed = random.randint(1, 4)  # possible falling speeds
        self.rect = pygame.Rect(x - self.radius, y - self.radius,
                                2 * self.radius, 2 * self.radius)
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.color = [(235, 238, 240, random.randint(20, 100)),
                      (220, 236, 247, random.randint(20, 100))]  # color options
        pygame.draw.circle(self.image, random.choice(self.color),
                           (self.radius, self.radius), self.radius)

    def getRect(self):
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    def update(self, screenWidth, screenHeight):
        self.y += self.speed  # snow falling
        if self.y < 0:
            self.y = screenHeight
        elif self.y > screenHeight:
            self.y = 0
        self.getRect()
