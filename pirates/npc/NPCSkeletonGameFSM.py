# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.NPCSkeletonGameFSM
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed import DistributedSmoothNode
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import BattleNPCGameFSM

class NPCSkeletonGameFSM(BattleNPCGameFSM.BattleNPCGameFSM):
    __module__ = __name__

    def __init__(self, av):
        BattleNPCGameFSM.BattleNPCGameFSM.__init__(self, av)

    def cleanup(self):
        BattleNPCGameFSM.BattleNPCGameFSM.cleanup(self)