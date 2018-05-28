# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.kraken.HolderGameFSM
from direct.interval.IntervalGlobal import *
from pirates.pirate.BattleAvatarGameFSM import BattleAvatarGameFSM
import random

class HolderGameFSM(BattleAvatarGameFSM):
    __module__ = __name__

    def __init__(self, av):
        BattleAvatarGameFSM.__init__(self, av)
        self.submergeIval = None
        return

    def enterSubmerged(self, *args):
        self.submergeIval = Sequence(Wait(random.random()), self.av.actorInterval('emerge', playRate=-1, blendOutT=0), Func(self.av.creature.hide), Func(self.av.creature.stopUpdateTask), Func(self.av.creature.removeEffects))
        self.submergeIval.start()

    def exitSubmerged(self):
        if self.submergeIval:
            self.submergeIval.finish()
            self.submergeIval = None
        self.av.creature.startUpdateTask()
        return