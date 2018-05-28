# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.DistributedBossNavySailor
from pandac.PandaModules import Vec4
from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCNavySailor import DistributedNPCNavySailor
from pirates.pirate import AvatarTypes
from pirates.npc.Boss import Boss

class DistributedBossNavySailor(DistributedNPCNavySailor, Boss):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossNavySailor')

    def __init__(self, cr):
        DistributedNPCNavySailor.__init__(self, cr)
        Boss.__init__(self, cr)

    def announceGenerate(self):
        DistributedNPCNavySailor.announceGenerate(self)
        self.addBossEffect(AvatarTypes.Navy)

    def disable(self):
        self.removeBossEffect()
        DistributedNPCNavySailor.disable(self)

    def setAvatarType(self, avatarType):
        DistributedNPCNavySailor.setAvatarType(self, avatarType)
        self.loadBossData(self.getUniqueId(), avatarType)

    def getEnemyScale(self):
        return Boss.getEnemyScale(self)

    def getBossEffect(self):
        return Boss.getBossEffect(self)

    def getBossHighlightColor(self):
        return Boss.getBossHighlightColor(self)

    def getShortName(self):
        return Boss.getShortName(self)

    def skipBossEffect(self):
        return self.isGhost