# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.DistributedCannonDefenseEntrance
from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from direct.gui.OnscreenText import OnscreenText
from direct.interval.IntervalGlobal import *
from direct.distributed.GridChild import GridChild
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.minigame import CannonDefenseGlobals

class DistributedCannonDefenseEntrance(DistributedObject, GridChild):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractive')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        GridChild.__init__(self)
        self._gameFullTxt = None
        self._gameFullSeq = None
        return

    def generate(self):
        DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

    def teleport(self):
        base.loadingScreen.showTarget(cannonDefense=True)