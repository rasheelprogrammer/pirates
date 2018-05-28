# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.speedchat.SCCustomTerminal
from SCTerminal import SCTerminal
from otp.otpbase.OTPLocalizer import CustomSCStrings
SCCustomMsgEvent = 'SCCustomMsg'

def decodeSCCustomMsg(textId):
    return CustomSCStrings.get(textId, None)


class SCCustomTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, textId):
        SCTerminal.__init__(self)
        self.textId = textId
        self.text = CustomSCStrings[self.textId]

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(SCCustomMsgEvent), [
         self.textId])