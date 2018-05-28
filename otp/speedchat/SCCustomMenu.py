# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.speedchat.SCCustomMenu
from SCMenu import SCMenu
from SCCustomTerminal import SCCustomTerminal
from otp.otpbase.OTPLocalizer import CustomSCStrings

class SCCustomMenu(SCMenu):
    __module__ = __name__

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('customMessagesChanged', self.__customMessagesChanged)
        self.__customMessagesChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __customMessagesChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return
        else:
            for msgIndex in lt.customMessages:
                if CustomSCStrings.has_key(msgIndex):
                    self.append(SCCustomTerminal(msgIndex))