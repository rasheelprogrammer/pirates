# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.FishingTutorialManager


class FishingTutorialManager:
    __module__ = __name__

    def __init__(self):
        self.currentPriority = 0

    def showTutorial(self, contextId, priority=0):
        if not base.localAvatar.guiMgr.contextTutPanel.isFilled():
            self.currentPriority = 0
        if self.currentPriority > priority:
            return
        self.currentPriority = priority
        base.localAvatar.sendRequestContext(contextId)