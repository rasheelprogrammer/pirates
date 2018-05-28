# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.inventory.InventoryUIAmmoBagItem
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.economy import EconomyGlobals
from pirates.inventory import InventoryUIItem

class InventoryUIAmmoBagItem(InventoryUIItem.InventoryUIItem):
    __module__ = __name__

    def __init__(self, manager, skillId, itemTuple, imageScaleFactor=1.0):
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor)
        self.initialiseoptions(InventoryUIAmmoBagItem)
        weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        fishingIcons = loader.loadModel('models/textureCards/fishing_icons')
        if self.itemTuple[1]:
            self['image'] = weaponIcons.find('**/%s' % EconomyGlobals.getItemIcons(self.itemTuple[1]))
        else:
            if skillId == EconomyGlobals.ItemType.FISHING_POUCH:
                self['image'] = fishingIcons.find('**/%s' % EconomyGlobals.getItemTypeIcon(skillId))
            else:
                self['image'] = weaponIcons.find('**/%s' % EconomyGlobals.getItemTypeIcon(skillId))
        self.skillId = skillId