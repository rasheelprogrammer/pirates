# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.inventory.InventoryUITreasureItem
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.piratesbase import CollectionMap
from pirates.inventory import InventoryUINoTradeItem

class InventoryUITreasureItem(InventoryUINoTradeItem.InventoryUINoTradeItem):
    __module__ = __name__

    def __init__(self, manager, itemTuple, imageScaleFactor=1.0, showMax=1):
        InventoryUINoTradeItem.InventoryUINoTradeItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor, showMax=showMax)
        self.initialiseoptions(InventoryUITreasureItem)
        treasureGui = loader.loadModel('models/gui/treasure_gui')
        self['image'] = treasureGui.find('**/%s' % CollectionMap.Assets.get(itemTuple[1]))
        self['image_scale'] = 0.1 * imageScaleFactor
        self.imageScale = 3.0
        self.textScale = 1.1

    def destroy(self):
        InventoryUINoTradeItem.InventoryUINoTradeItem.destroy(self)

    def getName(self):
        return PLocalizer.Collections.get(self.itemTuple[1])