# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.CannonDefenseHUD
from pirates.piratesgui.CannonDefenseGoldRemaingUI import *
from pirates.piratesgui.CannonDefenseTimeRemainingUI import *

class CannonDefenseHUD:
    __module__ = __name__

    def __init__(self):
        self.goldRemainingUI = None
        self.timeRemainingUI = None
        return

    def create(self):
        self.goldRemainingUI = CannonDefenseGoldRemaingUI()
        self.timeRemainingUI = CannonDefenseTimeRemainingUI()
        self.timeRemainingUI.setWaveNumber(1)
        self.goldRemainingUI.mineCounter.setPos(0.025, 0, -0.035)
        self.timeRemainingUI.timeRemaining.setPos(-0.01, 0, 0)

    def destroy(self):
        if self.goldRemainingUI:
            self.goldRemainingUI.destroy()
            self.goldRemainingUI = None
        if self.timeRemainingUI:
            self.timeRemainingUI.destroy()
            self.timeRemainingUI = None
        return