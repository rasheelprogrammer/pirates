# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.band.CrewMatchHandle
from pirates.pirate.PAvatarHandle import PAvatarHandle

class CrewMatchHandle(PAvatarHandle):
    __module__ = __name__

    def __init__(self, avId, avName):
        self.avatarId = avId
        self.avatarName = avName
        self.accountId = None
        self.accountName = None
        return

    def getName(self):
        return self.avatarName

    def isUnderstandable(self):
        return False

    def isOnline(self):
        return False

    def getBandId(self):
        return (0, 0)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        base.cr.crewMatchManager.d_requestTeleportQuery(sendToId, localBandMgrId, localBandId, localGuildId, localShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        base.cr.crewMatchManager.d_requestTeleportResponse(sendToId, available, shardId, instanceDoId, areaDoId)