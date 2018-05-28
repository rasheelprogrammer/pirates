# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.InventoryPage
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.uberdog import InventoryRequestBase

class InventoryPage(DirectFrame, InventoryRequestBase.InventoryRequestBase):
    __module__ = __name__

    def __init__(self):
        DirectFrame.__init__(self, parent=NodePath(), relief=None, state=DGG.DISABLED, frameColor=PiratesGuiGlobals.FrameColor, borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0.0, PiratesGuiGlobals.InventoryPageWidth, 0.0, PiratesGuiGlobals.InventoryPageHeight), pos=(-0.54, 0, -0.72))
        InventoryRequestBase.InventoryRequestBase.__init__(self)
        self.initialiseoptions(InventoryPage)
        return

    def show(self):
        DirectFrame.show(self)

    def hide(self):
        DirectFrame.hide(self)

    def slideOpenCallback(self):
        pass

    def slideCloseCallback(self):
        pass

    def slideOpenPrecall(self):
        pass