# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.chat.PTalkHandle
from pirates.pirate.PAvatarHandle import PAvatarHandle

class PTalkHandle(PAvatarHandle):
    __module__ = __name__

    def __init__(self, doId, message):
        self.avatarId = doId
        self.avatarName = None
        self.accountId = None
        self.accountName = None
        self.addMessageInfo(message)
        self.bandId = (0, 0)
        return

    def getName(self):
        return self.avatarName

    def isUnderstandable(self):
        return False

    def isOnline(self):
        return False

    def addMessageInfo(self, message):
        if self.avatarId == message.getSenderAvatarId():
            if not self.avatarName:
                if message.getSenderAvatarName():
                    self.avatarName = message.getSenderAvatarName()
                if not self.accountId and message.getSenderAccountId():
                    self.accountId = message.getSenderAccountId()
                self.accountName = not self.accountName and message.getSenderAccountName() and message.getSenderAccountName()
        else:
            if self.avatarId == message.getReceiverAvatarId():
                if not self.avatarName and message.getReceiverAvatarName():
                    self.avatarName = message.getReceiverAvatarName()
                if not self.accountId and message.getReceiverAccountId():
                    self.accountId = message.getReceiverAccountId()
                if not self.accountName and message.getReceiverAccountName():
                    self.accountName = message.getReceiverAccountName()

    def setBandId(self, bandMgrId, bandId):
        self.bandId = (
         bandMgrId, bandId)

    def getBandId(self):
        return self.bandId

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        localAvatar.sendTeleportQuery(sendToId, localBandMgrId, localBandId, localGuildId, localShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        localAvatar.sendTeleportResponse(available, shardId, instanceDoId, areaDoId, sendToId)