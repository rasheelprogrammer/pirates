# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ShipItemList
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemList
from pirates.piratesgui import ShipItemGUI
from pirates.piratesbase import PiratesGlobals

class ShipItemList(InventoryItemList.InventoryItemList):
    __module__ = __name__

    def __init__(self, inventory, height, trade=0, buy=0, sell=0, use=0):
        InventoryItemList.InventoryItemList.__init__(self, inventory, height, trade, buy, sell, use)
        self.initialiseoptions(ShipItemList)

    def loadInventoryPanels(self):
        for item in self.inventory:
            data = [
             item, 1]
            self.addPanel(data, repack=0)

        self.repackPanels()

    def addPanel(self, data, repack=1):
        panel = ShipItemGUI.ShipItemGUI(data, trade=self.trade, buy=self.buy, sell=self.sell, use=self.use)
        panel.reparentTo(self.getCanvas())
        self.panels.append(panel)
        if repack:
            self.repackPanels()

    def repackPanels(self):
        invHeight = len(self.inventory)
        z = 0.01 + PiratesGuiGlobals.ShipItemGuiHeight
        i = 0
        for i in range(len(self.panels)):
            self.panels[i].setPos(0.01, 0, -z * (i + 1))
            self.panels[i].origionalPos = self.panels[i].getPos(render2d)

        self['canvasSize'] = (
         0, PiratesGuiGlobals.ShipItemGuiWidth - 0.09, -z * (i + 1), 0)