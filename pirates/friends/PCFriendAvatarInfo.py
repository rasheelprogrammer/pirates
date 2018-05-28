# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.friends.PCFriendAvatarInfo
from otp.friends.FriendInfo import FriendInfo
from pirates.pirate.PAvatarHandle import PAvatarHandle

class PCFriendAvatarInfo(FriendInfo, PAvatarHandle):
    __module__ = __name__

    @classmethod
    def makeFromFriendInfo(cls, info):
        out = cls()
        out.avatarName = info.avatarName
        out.playerName = info.playerName
        out.onlineYesNo = info.onlineYesNo
        out.openChatEnabledYesNo = info.openChatEnabledYesNo
        out.openChatFriendshipYesNo = info.openChatFriendshipYesNo
        out.understandableYesNo = info.understandableYesNo
        out.playerId = info.playerId
        return out

    def __init__(self, *args, **kw):
        FriendInfo.__init__(self, *args, **kw)
        self.bandId = None
        return

    def setBandId(self, bandMgrId, bandId):
        if (
         bandMgrId, bandId) != (0, 0):
            self.bandId = (
             bandMgrId, bandId)
        else:
            self.bandId = None
        return

    def getBandId(self):
        return self.bandId

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        localAvatar.sendTeleportQuery(sendToId, localBandMgrId, localBandId, localGuildId, localShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        localAvatar.sendTeleportResponse(available, shardId, instanceDoId, areaDoId, sendToId)