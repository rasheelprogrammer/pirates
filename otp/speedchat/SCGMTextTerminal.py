# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.speedchat.SCGMTextTerminal
from SCTerminal import SCTerminal
from otp.speedchat import SpeedChatGMHandler
SCGMTextMsgEvent = 'SCGMTextMsg'

class SCGMTextTerminal(SCTerminal):
    __module__ = __name__

    def __init__(self, textId):
        SCTerminal.__init__(self)
        gmHandler = SpeedChatGMHandler.SpeedChatGMHandler()
        self.textId = textId
        self.text = gmHandler.getPhrase(textId)

    def handleSelect(self):
        SCTerminal.handleSelect(self)
        messenger.send(self.getEventName(SCGMTextMsgEvent), [self.textId])