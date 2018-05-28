# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.inventory.InventoryUINoTradeItem
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory import InventoryUIItem

class InventoryUINoTradeItem(InventoryUIItem.InventoryUIItem):
    __module__ = __name__

    def __init__(self, manager, itemTuple, imageScaleFactor=1.0, showMax=1):
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor)
        self.initialiseoptions(InventoryUINoTradeItem)
        self['relief'] = None
        self.textScale = 0.9
        self.itemType = ITEM_NOTRADE
        return