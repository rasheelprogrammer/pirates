# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.PlayerPirateGameFSM
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.destructibles import ShatterableSkeleton
from pirates.pirate.BattleAvatarGameFSM import BattleAvatarGameFSM

class PlayerPirateGameFSM(BattleAvatarGameFSM):
    __module__ = __name__

    def __init__(self, av, fsmName='PlayerPirateGameFSM'):
        BattleAvatarGameFSM.__init__(self, av, fsmName)

    def enterDeath(self, extraArgs=[]):
        BattleAvatarGameFSM.enterDeath(self, extraArgs)

    def exitDeath(self):
        BattleAvatarGameFSM.exitDeath(self)