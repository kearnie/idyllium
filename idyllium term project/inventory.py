# for inventory to store berries
import copy
import random

import pygame

# to store the berries
from animals import Bird
from interaction import Interactable


class Inventory(object):
    def __init__(self):
        self.selected = None
        self.berryAmount = 0


# to show the inventory
class InventoryView(Interactable):
    def __init__(self, ui, inventory):
        super().__init__()
        self.ui = ui
        self.height = 60
        self.width = 60
        self.x = 10
        self.y = ui.world.height - self.height - 10
        x, y = self.x, self.y
        self.rect = pygame.Rect(x, y, x + self.width, y + self.height)
        self.image = pygame.Surface((self.width, self.height),
                                    pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.color = (0, 0, 0, 30)
        self.inventory = inventory
        self.drawBox()
        self.hover = True
        self.visible = False
        self.berryIcon = CherryIcon(ui, inventory, x + 5, y + 5)
        self.priority = -1
        ui.world.interactionHandler.register(self)

    def updateAmounts(self):
        self.berryIcon.redraw()

    def onStopHover(self):
        self.ui.hideInventoryView()
        self.ui.showBackpackIcon()

    def hide(self):
        self.ui.remove(self)
        if not self.berryIcon.isSelected:
            self.ui.remove(self.berryIcon)
        self.visible = False

    def show(self):
        self.ui.add(self)
        self.ui.add(self.berryIcon)
        self.visible = True

    def drawBox(self):
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, self.height))


class CherryIcon(Interactable):
    def __init__(self, ui, inventory, x, y):
        super().__init__()
        self.radius = 15
        self.ui = ui
        self.inventory = inventory
        self.x, self.y = x, y
        self.baseImage = pygame.image.load("assets/berryicon.png").convert_alpha()
        w, h = self.baseImage.get_size()
        self.rect = pygame.Rect(x, y, w, h)
        self.redraw()
        self.click = True
        self.priority = -3
        ui.world.interactionHandler.register(self)
        self.isSelected = False
        self.use = True

    def setRect(self):
        if (self.ui.world.interactionHandler.onCursor == self):
            return
        self.rect = pygame.Rect(self.x, self.y, self.x + 2 * self.radius + 10, self.y + 2 * self.radius + 10)

    def update(self, width, height):
        if self.ui.world.interactionHandler.onCursor != self:
            self.isSelected = False
            if not self.ui.inventoryView.visible:
                self.kill()
        self.setRect()

    def onUse(self, otherSprite, mouseX, mouseY):
        from ui import Backpack
        if (isinstance(otherSprite, Bird)) and self.inventory.berryAmount > 0:
            if not otherSprite.deathFlag:
                otherSprite.deathFlag = True
                self.inventory.berryAmount -= 1
                self.redraw()
            else:
                self.ui.world.interactionHandler.onCursor = None
        else:
            self.ui.world.interactionHandler.onCursor = None

    def onClick(self, mouseX, mouseY):
        if (self.inventory.berryAmount <= 0):
            return
        self.ui.world.interactionHandler.onCursor = self
        self.isSelected = True

    def redraw(self):
        self.image = copy.copy(self.baseImage)
        label = self.ui.world.font.render("x%d" % (self.inventory.berryAmount), 1, (130, 197, 245, 200))
        self.image.blit(label, (30, 28))
