import pygame
import random
from pygame.locals import *
from camera import *
from atmosphere import *
from interaction import InteractionHandler
from inventory import Inventory
from tree import *
from leaves import *
from timecover import *
from animals import *
from flowers import *
from berries import *
from buttons import *
from splash import *
import numpy as np

# pygame framework by lukas peraza
# http://blog.lukasperaza.com/getting-started-with-pygame/
from ui import UI, Backpack


class World(object):
    def __init__(self, tickRate, interactionHandler, screen):
        self.font = pygame.font.SysFont("corbel", 18)
        self.height = 620
        self.width = 450
        self.screen = screen
        World.instance = self
        self.time = 450
        self.windSpeed = .01
        self.interactionHandler = interactionHandler
        self.camera = Camera()
        self.atmosphere = Atmosphere()
        self.tree = Tree()
        self.trunk = Tree()
        self.storm = Storm()
        self.controls = Controls(self)
        self.light = Light()
        self.inventory = Inventory()
        self.ui = UI(self)
        self.atmosphere.add(self.light)
        self.timeCover = Time(self)
        self.atmosphere.add(self.timeCover)
        self.storm.adjust(0)  # no precipitation at first
        self.birds = Birds(self)
        self.flowers = pygame.sprite.Group()
        self.scrollingList = [self.tree, self.flowers]  # list of attributes to undergo scrolling
        self.generator = Generator()
        self.tickRate = tickRate
        self.skyImg = pygame.image.load('assets/gradient1.png')

    def clearOld(self):
        for group in self.scrollingList:
            for sprite in group.sprites():
                if sprite.y > self.camera.winY + 670:  # replace 620 as var
                    group.remove(sprite)

    def drawSky(self):
        self.screen.blit(self.skyImg, (0, 0))

    def updateWind(self):
        changeProb = 1 / (self.tickRate * 2)
        if random.random() < changeProb:
            changeMagnitude = .4
            change = random.random() * changeMagnitude - (changeMagnitude / 2)
            self.windSpeed += change
        drasticChangeProb = 1 / (self.tickRate * 15)
        if random.random() < drasticChangeProb:
            magnitude = .6
            self.windSpeed = random.random() * magnitude - (magnitude / 2)

    def onTick(self, screen):
        self.updateWind()
        self.birds.onTick()
        self.camera.winY -= 1
        self.time = (self.time + .5) % 1000
        self.generator.check(self)
        self.tree.update(self.width, self.height)
        self.storm.update(self.width, self.height)
        self.birds.update(self.width, self.height)
        self.atmosphere.update(self.width, self.height)
        self.flowers.update(self.width, self.height)
        self.controls.update(self.width, self.height)
        self.trunk.update(self.width, self.height)
        self.ui.update(self.width, self.height)
        # self.controls.update(450,620) # !!!!
        for group in self.scrollingList:
            self.camera.applyGroup(group)
        screen.fill((172, 202, 232))
        self.drawSky()
        self.tree.draw(screen)
        self.trunk.draw(screen)
        self.flowers.draw(screen)
        self.birds.draw(screen)
        self.storm.draw(screen)
        self.atmosphere.draw(screen)
        self.ui.draw(screen)
        self.controls.draw(screen)
        for sprite in self.tree.sprites():
            if isinstance(sprite, Leaf):
                if not sprite.isFalling:
                    sprite.updateColor(self.storm.temp)
                if random.random() < self.fallingProb():
                    sprite.isFalling = True

    def fallingProb(self):
        temp = self.storm.temp
        if temp == 0:
            return 1
        return .001 / temp


class Generator(object):
    def __init__(self):
        self.maxGenY = 620  # maximum boundary of image generated

    def check(self, world):
        genBuffer = -250  # threshold difference needed to generate new things
        cameraY = world.camera.winY
        while self.maxGenY - cameraY > genBuffer:
            self.generate(world)

    def generate(self, world):
        sizeToGen = 200  # amount to generate each time
        oldMax = self.maxGenY
        newMax = oldMax - sizeToGen  # reconfigure higher (neg val)
        y1 = oldMax
        y2 = newMax
        x1 = 225
        x2 = 225
        branchSegment = Trunksegment(world, x1, y1, x2, y2, 20)
        world.trunk.add(branchSegment)
        self.maxGenY = newMax
        branchNum = random.randint(6, 8)
        for i in range(branchNum):
            initAngle = random.choice([0, math.pi])
            y = random.randint(y2, y1)
            makeBranch(world, x1, y, initAngle)
            y += random.randint(-15, 15)
            initAngle += math.pi
            makeBranch(world, x1, y, initAngle)
        world.clearOld()


def run():
    pygame.init()
    font = pygame.font.SysFont("corbel", 16)
    flags = DOUBLEBUF
    screen = pygame.display.set_mode((450, 620), flags)  # (screenWidth,screenHeight)
    pygame.mixer.music.load("assets/bg.ogg")
    pygame.mixer.music.set_volume(.7)
    pygame.mixer.music.play(loops=-1)
    pygame.display.set_caption('Idyllium')
    clock = pygame.time.Clock()
    tickRate = 30
    interactionHandler = None
    world = None
    splash = Splash()
    splash.add(TitleBG())
    debug = False
    hasClickedPastTitle = False
    hasClickedPastHelp = False
    playing = True

    def start():
        nonlocal interactionHandler
        interactionHandler = InteractionHandler()
        nonlocal world
        world = World(tickRate, interactionHandler, screen)

    while playing:
        dt = clock.tick(tickRate)
        if world != None:
            world.onTick(screen)
        wasClick = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                wasClick = True
            elif event.type == pygame.KEYDOWN:
                if world != None:
                    if event.key == pygame.K_UP:  # UP key to increase precip
                        world.controls.onUp()
                    elif event.key == pygame.K_DOWN:  # DOWN key to decrase precip
                        world.controls.onDown()  # The rest of these cases are for debugging purposes
                if event.key == pygame.K_ESCAPE:
                    playing = False

                    # temporary keypresses from earlier deliverables:
                    # elif event.key == pygame.K_a:  # A to increase temperature
                    #    world.storm.temp += 5
                    # elif event.key == pygame.K_z:  # Z to decrease temperature
                    #    world.storm.temp -= 5
                    # elif event.key == pygame.K_h:
                    #    debug = not debug
                    # elif event.key == pygame.K_s:  # S to increase light strength
                    #    if world.light.lightLevel < 170:
                    #        world.light.lightLevel += 5
                    # elif event.key == pygame.K_x:  # X to decrease light strength
                    #    if world.light.lightLevel > 0:
                    #        world.light.lightLevel -= 5
                    # elif event.key == pygame.K_d:  # spawn birds at random locations
                    #    world.birds.add(Bird(world,random.randint(1, 450), 610))
                    # elif event.key == pygame.K_c:  # temp removal of birds
                    #    # recode this so it looks more natural later
                    #    if len(world.birds.sprites()) > 0:
                    #        world.birds.remove(world.birds.sprites()[0])

            elif event.type == pygame.QUIT:
                playing = False
        if not hasClickedPastHelp or not hasClickedPastTitle:
            splash.update(620, 450)
            splash.draw(screen)
        if not hasClickedPastTitle:
            if (wasClick):
                hasClickedPastTitle = True
                splash.empty()
                splash.add(HelpBG())
        elif not hasClickedPastHelp:
            if (wasClick):
                hasClickedPastHelp = True
                splash.empty()
                start()
        elif interactionHandler != None:
            interactionHandler.onTick(pygame.mouse.get_pos(), wasClick)
        if world != None:
            label = font.render("temp: %d°F" % (world.storm.temp), 1, (255, 255, 255))
            screen.blit(label, (10, 10))
            windDirection = "E"
            if world.windSpeed < 0:
                windDirection = "W"
            label5 = font.render("wind: %d mph %s" % (abs(world.windSpeed * 75),
                                windDirection), 1, (255, 255, 255))
            screen.blit(label5, (10, 25))
        if debug and world != None:
            label2 = font.render("time: %d" % (world.time), 1, (255, 255, 255))
            label3 = font.render("scrolling sprites: %d" % (sum([len(x) for x 
                in world.scrollingList])), 1,(255, 255, 255))
            label4 = font.render("fps: %d" % (clock.get_fps()), 1, (255, 255, 255))
            screen.blit(label2, (10, 70))
            screen.blit(label3, (10, 40))
            screen.blit(label4, (10, 55))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    run()
