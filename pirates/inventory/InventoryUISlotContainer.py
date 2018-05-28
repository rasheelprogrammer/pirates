# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.inventory.InventoryUISlotContainer
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIContainer
from pirates.inventory.InventoryUIGlobals import *

class InventoryUISlotContainer(InventoryUIContainer.InventoryUIContainer):
    __module__ = __name__
    ReferenceSlots = True

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=None, countZ=None, slotList=[]):
        self.slotCount = 0
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)

    def manageCells(self, slotList):
        self.slotList = slotList
        for index in range(len(self.slotList)):
            slot = self.slotList[index]
            cell = self.cellList[index]
            self.manager.assignCellSlot(cell, self.slotList[self.slotCount])
            self.slotCount += 1