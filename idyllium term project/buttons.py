# for all utility buttons
import copy

import pygame

from interaction import Interactable


class Controls(pygame.sprite.Group):
    def __init__(self, world):
        super().__init__()
        x = 410
        spacing = 10
        self.world = world
        y = spacing
        self.temp = TempToggle(self, x, y)
        y += self.temp.height + spacing
        self.add(self.temp)
        self.rain = RainToggle(self, x, y)
        self.add(self.rain)
        y += self.rain.height + spacing
        self.lux = LuxToggle(self, x, y)
        self.add(self.lux)
        y += self.lux.height + spacing
        self.time = TimeToggle(self, x, y)
        self.add(self.time)
        self.controlType = None
        self.currentToggle = None

    def removeAllTogglesExcept(self, ignore):
        for sprite in self.sprites():
            if sprite != ignore:
                sprite.toggled = False
                sprite.redraw()

    def onUp(self):
        if (self.currentToggle != None):
            self.currentToggle.onUp()

    def onDown(self):
        if (self.currentToggle != None):
            self.currentToggle.onDown()


class ToggleButton(Interactable):
    def __init__(self, controls, x, y, imageName, defaultValue=False):
        super().__init__()
        self.click = True
        self.x, self.y = (x, y)
        self.baseImage = pygame.image.load(imageName).convert_alpha()
        self.controls = controls
        self.click = True
        controls.world.interactionHandler.register(self)
        self.toggled = defaultValue
        self.redraw()

    def redraw(self):
        w, h = self.baseImage.get_size()
        self.image = pygame.transform.smoothscale(self.baseImage, (int(w // 1.5), int(h // 1.5)))
        w, h = self.image.get_size()
        self.width = w
        self.height = h
        self.rect = pygame.Rect(self.x, self.y, w, h)
        if self.toggled:
            pygame.draw.lines(self.image, (255, 255, 255), False,
                              [(0, 0), (0, h - 1), (w - 1, h - 1), (w - 1, 0), (0, 0)])

    def onPress(self):
        pass

    def onUp(self):
        pass

    def onDown(self):
        pass

    def on(self):
        pass

    def off(self):
        pass

    def onClick(self, mouseX, mouseY):
        self.onPress()
        self.toggled = not self.toggled
        if self.toggled:
            self.controls.removeAllTogglesExcept(self)
            self.on()
            self.controls.currentToggle = self
        else:
            self.off()
            self.controls.currentToggle = None
        self.redraw()


class TempToggle(ToggleButton):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, "assets/button-temp.png")

    def on(self):
        self.controls.controlType = "temp"

    def onUp(self):
        self.controls.world.storm.temp += 5

    def onDown(self):
        self.controls.world.storm.temp -= 5


class LuxToggle(ToggleButton):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, "assets/button-lux.png")

    def on(self):
        self.controls.controlType = "lux"

    def onUp(self):
        self.controls.world.light.lightLevel += 5

    def onDown(self):
        self.controls.world.light.lightLevel -= 5


class TimeToggle(ToggleButton):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, "assets/button-time.png")

    def on(self):
        self.controls.controlType = "time"

    def onUp(self):
        self.controls.world.time += 25

    def onDown(self):
        self.controls.world.time -= 25


class RainToggle(ToggleButton):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, "assets/button-rain.png")

    def on(self):
        self.controls.controlType = "rain"

    def onUp(self):
        self.controls.world.storm.adjust(self.controls.world.storm.amount + 100)

    def onDown(self):
        self.controls.world.storm.adjust(self.controls.world.storm.amount - 100)
