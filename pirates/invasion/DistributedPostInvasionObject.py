# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.invasion.DistributedPostInvasionObject
from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.distributed.GridChild import GridChild

class DistributedPostInvasionObject(DistributedObject.DistributedObject, GridChild):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedWreckedGovernorsMansion')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        GridChild.__init__(self)
        self.postInvasionObjs = []
        self.onFire = False

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.notify.debug('generate')

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)

    def disable(self):
        self.stopBurning()
        self.postInvasionObjs = []
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        GridChild.__init__(self)

    def setOnFire(self, onFire):
        self.onFire = onFire
        if self.onFire:
            self.startBurning()
        else:
            self.stopBurning()

    def startBurning(self):
        pass

    def stopBurning(self):
        pass