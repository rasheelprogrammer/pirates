# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.DistributedLockDoor
from pirates.minigame import DistributedLock
from direct.interval.IntervalGlobal import *

class DistributedLockDoor(DistributedLock.DistributedLock):
    __module__ = __name__

    def __init__(self, cr):
        DistributedLock.DistributedLock.__init__(self, cr)
        self.isDoor = 1

    def loadModel(self):
        self.table = loader.loadModel('models/props/jail_door_03')
        self.table.setScale(1.0, 1.0, 1.0)
        self.table.reparentTo(self)

    def finalOpen(self):
        colNode = self.table.find('**/collisions')
        colNode.stash()
        self.hinge = self.table.find('**/jail_door')
        lidopener = LerpHprInterval(self.hinge, 1, Vec3(-140, 0, 0))
        lidopener.start()
        self.setAllowInteract(False)