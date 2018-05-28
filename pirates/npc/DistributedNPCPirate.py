# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.DistributedNPCPirate
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from pirates.pirate import DistributedPirateBase
from pirates.piratesbase import PiratesGlobals
from pirates.battle import DistributedBattleNPC

class DistributedNPCPirate(DistributedBattleNPC.DistributedBattleNPC, DistributedPirateBase.DistributedPirateBase):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCPirate')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        DistributedPirateBase.DistributedPirateBase.__init__(self, cr)

    def disable(self):
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        DistributedPirateBase.DistributedPirateBase.disable(self)
        self.stopBlink()
        self.ignoreAll()

    def delete(self):
        try:
            self.DistributedNPCPirate_deleted
        except:
            self.DistributedNPCPirate_deleted = 1
            DistributedBattleNPC.DistributedBattleNPC.delete(self)
            DistributedPirateBase.DistributedPirateBase.delete(self)

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        DistributedPirateBase.DistributedPirateBase.generate(self)
        self.setInteractOptions(proximityText=None, allowInteract=False)
        return

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        DistributedPirateBase.DistributedPirateBase.announceGenerate(self)

    def setDNAString(self, dnaString):
        DistributedPirateBase.DistributedPirateBase.setDefaultDNA(self)
        self.style.makeNPCPirate()

    def isBattleable(self):
        return 0

    def play(self, *args, **kwArgs):
        Pirate.Pirate.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        Pirate.Pirate.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        Pirate.Pirate.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Pirate.Pirate.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        Pirate.Pirate.stop(self, *args, **kwArgs)