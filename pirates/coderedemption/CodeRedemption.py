# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.coderedemption.CodeRedemption
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PLocalizer
from pirates.coderedemption import CodeRedemptionGlobals

class CodeRedemption(DistributedObjectGlobal):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)

    def redeemCode(self, code):
        if code:
            userName = ''
            accountId = 0
            self.sendUpdate('sendCodeForRedemption', [
             code, userName, accountId])

    def notifyClientCodeRedeemStatus(self, status, type, uid):
        if status == CodeRedemptionGlobals.ERROR_ID_GOOD:
            base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionGood)
        else:
            if status == CodeRedemptionGlobals.ERROR_ID_OVERFLOW:
                base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionFull)
            else:
                if status == CodeRedemptionGlobals.ERROR_ID_TIMEOUT:
                    base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionTimeout)
                else:
                    base.talkAssistant.receiveGameMessage(PLocalizer.CodeRedemptionBad)
        if type == -1:
            pass
        else:
            if type == CodeRedemptionGlobals.CLOTHING:
                localAvatar.guiMgr.messageStack.showLoot([], cloth=uid)
            else:
                if type == CodeRedemptionGlobals.JEWELRY:
                    localAvatar.guiMgr.messageStack.showLoot([], jewel=uid)
                else:
                    if type == CodeRedemptionGlobals.TATTOO:
                        localAvatar.guiMgr.messageStack.showLoot([], tattoo=uid)
        messenger.send('codeRedeemed', [status])