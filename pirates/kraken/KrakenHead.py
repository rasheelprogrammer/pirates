# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.kraken.KrakenHead
from pirates.creature.DistributedCreature import DistributedCreature

class bp:
    __module__ = __name__
    kraken = bpdb.bpPreset(cfg='kraken', static=1)


class KrakenHead(DistributedCreature):
    __module__ = __name__

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr)
        self.krakenId = 0

    def setupCreature(self, avatarType):
        DistributedCreature.setupCreature(self, avatarType)

    def announceGenerate(self):
        DistributedCreature.announceGenerate(self)
        getBase().khead = self

    def delete(self):
        if getBase().khead == self:
            getBase().khead = None
        DistributedCreature.delete(self)
        return

    def setKrakenId(self, krackenId):
        self.krakenId = krackenId

    def getKrakenId(self):
        return self.krakenId

    def getKraken(self):
        return self.cr.getDo(self.krakenId)