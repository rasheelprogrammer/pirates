# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.chat.PChatInputWhiteList
from otp.chat.ChatInputWhiteList import ChatInputWhiteList
from pirates.chat.PWhiteList import PWhiteList

class PChatInputWhiteList(ChatInputWhiteList):
    __module__ = __name__

    def __init__(self, parent=None, **kw):
        ChatInputWhiteList.__init__(self, parent, **kw)
        self.initialiseoptions(PChatInputWhiteList)
        self.whiteList = PWhiteList()
        self.accept('SetChatBoxPercentage', self.textBoxScale)
        self.setDefaultWidth()

    def delete(self):
        ChatInputWhiteList.delete()

    def textBoxScale(self, percentage):
        iPercentage = 1.0 / percentage
        self['text_scale'] = (self.origTextScale[0] * iPercentage, self.origTextScale[1] * 1.0)
        self['frameSize'] = (self.origFrameSize[0] * iPercentage, self.origFrameSize[1] * iPercentage, self.origFrameSize[2], self.origFrameSize[3])
        self.setDefaultWidth()
        self['width'] = self.defaultWidth
        self.set('')

    def setDefaultWidth(self, size=None):
        if size != None:
            self.defaultWidth = size
        else:
            entrySize = self['frameSize'][1]
            textWidth = entrySize / self['text_scale'][0]
            self.defaultWidth = textWidth
        return

    def sendChatByMode(self, text):
        state = self.getCurrentOrNextState()
        messenger.send('sentRegularChat')
        if state == 'PlayerWhisper':
            base.talkAssistant.sendAccountTalk(text, self.whisperId)
        else:
            if state == 'AvatarWhisper':
                base.talkAssistant.sendWhisperTalk(text, self.whisperId)
            else:
                if state == 'GuildChat':
                    base.talkAssistant.sendGuildTalk(text)
                else:
                    if state == 'CrewChat':
                        base.talkAssistant.sendPartyTalk(text)
                    else:
                        if state == 'ShipPVPChat':
                            base.talkAssistant.sendShipPVPCrewTalk(text)
                        else:
                            base.talkAssistant.sendOpenTalk(text)