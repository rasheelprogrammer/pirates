# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.avatar.AvatarHandle


class AvatarHandle:
    __module__ = __name__
    dclassName = 'AvatarHandle'

    def getName(self):
        if __dev__:
            pass
        return ''

    def isOnline(self):
        if __dev__:
            pass
        return False

    def isUnderstandable(self):
        if __dev__:
            pass
        return True

    def setTalkWhisper(self, fromAV, fromAC, avatarName, chat, mods, flags):
        newText, scrubbed = localAvatar.scrubTalk(chat, mods)
        base.talkAssistant.receiveWhisperTalk(fromAV, avatarName, fromAC, None, self.avatarId, self.getName(), newText, scrubbed)
        return