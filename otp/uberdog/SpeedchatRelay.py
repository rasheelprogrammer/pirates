# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.uberdog.SpeedchatRelay
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.uberdog import SpeedchatRelayGlobals

class SpeedchatRelay(DistributedObjectGlobal):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)

    def sendSpeedchat(self, receiverId, messageIndex):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.NORMAL, [messageIndex])

    def sendSpeedchatCustom(self, receiverId, messageIndex):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.CUSTOM, [messageIndex])

    def sendSpeedchatEmote(self, receiverId, messageIndex):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.EMOTE, [messageIndex])

    def sendSpeedchatToRelay(self, receiverId, speedchatType, parameters):
        self.sendUpdate('forwardSpeedchat', [receiverId, speedchatType, parameters, base.cr.accountDetailRecord.playerAccountId, base.cr.accountDetailRecord.playerName + ' RHFM', 0])