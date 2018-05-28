# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.PAvatarHandle
from otp.avatar.AvatarHandle import AvatarHandle

class PAvatarHandle(AvatarHandle):
    __module__ = __name__
    dclassName = 'PAvatarHandle'

    def getBandId(self):
        if __dev__:
            pass
        return (0, 0)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        if __dev__:
            pass

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        if __dev__:
            pass