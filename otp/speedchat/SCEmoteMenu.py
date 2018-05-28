# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.speedchat.SCEmoteMenu
from SCMenu import SCMenu
from SCEmoteTerminal import SCEmoteTerminal

class SCEmoteMenu(SCMenu):
    __module__ = __name__

    def __init__(self):
        SCMenu.__init__(self)
        self.accept('emotesChanged', self.__emoteAccessChanged)
        self.__emoteAccessChanged()

    def destroy(self):
        SCMenu.destroy(self)

    def __emoteAccessChanged(self):
        self.clearMenu()
        try:
            lt = base.localAvatar
        except:
            return
        else:
            for i in range(len(lt.emoteAccess)):
                if lt.emoteAccess[i]:
                    self.append(SCEmoteTerminal(i))