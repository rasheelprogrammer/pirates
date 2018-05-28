# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.friends.FriendInfo
from otp.avatar.AvatarHandle import AvatarHandle

class FriendInfo(AvatarHandle):
    __module__ = __name__

    def __init__(self, avatarName='', playerName='', onlineYesNo=0, openChatEnabledYesNo=0, openChatFriendshipYesNo=0, wlChatEnabledYesNo=0, location='', sublocation='', timestamp=0, avatarId=0, friendPrivs=0, tokenPrivs=0):
        self.avatarName = avatarName
        self.playerName = playerName
        self.onlineYesNo = onlineYesNo
        self.openChatEnabledYesNo = openChatEnabledYesNo
        self.openChatFriendshipYesNo = openChatFriendshipYesNo
        self.wlChatEnabledYesNo = wlChatEnabledYesNo
        self.location = location
        self.sublocation = sublocation
        self.timestamp = timestamp
        self.avatarId = avatarId
        self.friendPrivs = friendPrivs
        self.tokenPrivs = tokenPrivs
        self.understandableYesNo = self.isUnderstandable()

    def calcUnderstandableYesNo(self):
        self.understandableYesNo = self.isUnderstandable()

    def getName(self):
        if self.avatarName:
            return self.avatarName
        else:
            if self.playerName:
                return self.playerName
            else:
                return ''

    def isUnderstandable(self):
        result = False
        try:
            if self.openChatFriendshipYesNo:
                result = True
            else:
                if self.openChatEnabledYesNo:
                    result = base.cr.openChatEnabled and True
                else:
                    if (self.wlChatEnabledYesNo and base).cr.whiteListChatEnabled:
                        result = True
        except:
            pass

        return result

    def isOnline(self):
        return self.onlineYesNo