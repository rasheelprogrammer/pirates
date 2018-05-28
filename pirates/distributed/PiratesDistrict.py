# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.distributed.PiratesDistrict
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from otp.distributed.DistributedDistrict import DistributedDistrict
from pirates.world import WorldGlobals
from pirates.world import WorldCreator
from pirates.piratesbase import PiratesGlobals

class PiratesDistrict(DistributedDistrict):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesDistrict')

    def __init__(self, cr):
        DistributedDistrict.__init__(self, cr)
        self.mainWorldFile = None
        self.shardType = 0
        return

    def generate(self):
        DistributedDistrict.generate(self)

    def announceGenerate(self):
        DistributedDistrict.announceGenerate(self)
        self.worldCreator = base.worldCreator
        self.worldCreator.district = self
        if self.shardType == PiratesGlobals.SHARD_MAIN:
            self.worldCreator.makeMainWorld(self.mainWorldFile)

    def setShardType(self, shardType):
        self.shardType = shardType

    def setMainWorld(self, world):
        self.mainWorldFile = world

    def delete(self):
        DistributedDistrict.delete(self)
        if self.worldCreator:
            self.worldCreator.destroy()

    def setAvatarCount(self, avatarCount):
        self.avatarCount = avatarCount
        messenger.send('PiratesDistrict-updateAvCounts', sentArgs=[self.doId, self.name, self.avatarCount, self.newAvatarCount])

    def getAvatarCount(self):
        return self.avatarCount

    def setNewAvatarCount(self, newAvatarCount):
        self.newAvatarCount = newAvatarCount

    def getNewAvatarCount(self):
        return self.newAvatarCount

    def setStats(self, avatarCount, newAvatarCount):
        self.setAvatarCount(avatarCount)
        self.setNewAvatarCount(newAvatarCount)

    def getName(self):
        return self.name

    def handleChildArrive(self, child, zoneId):
        if hasattr(base, 'localAvatar') and child is base.localAvatar:
            base.cr.setShardId(self.getDoId())

    def getUniqueId(self):
        return