# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.PiratesSpeedchatRelay
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.uberdog.SpeedchatRelay import SpeedchatRelay
from otp.uberdog import SpeedchatRelayGlobals

class PiratesSpeedchatRelay(SpeedchatRelay):
    __module__ = __name__

    def __init__(self, cr):
        SpeedchatRelay.__init__(self, cr)

    def sendQuestSpeedchat(self, receiverId, questInt, msgType, taskNum):
        self.sendSpeedchatToRelay(receiverId, SpeedchatRelayGlobals.PIRATES_QUEST, [questInt, msgType, taskNum])