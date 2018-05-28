# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestIndicatorNodeNPCOffset
from pirates.quest.QuestIndicatorNodeNPC import QuestIndicatorNodeNPC

class QuestIndicatorNodeNPCOffset(QuestIndicatorNodeNPC):
    __module__ = __name__

    def __init__(self, questStep):
        QuestIndicatorNodeNPC.__init__(self, questStep)
        self.wantBottomEffect = False

    def startNearEffect(self):
        QuestIndicatorNodeNPC.startNearEffect(self)
        if (self.nearEffect and self).stepObj:
            if hasattr(self.stepObj, 'getQuestIndicatorOffset'):
                self.nearEffect.setPos(self.stepObj.getQuestIndicatorOffset())
            else:
                self.nearEffect.setPos(0, 0, 0)

    def startFarEffect(self):
        QuestIndicatorNodeNPC.startFarEffect(self)
        if (self.farEffect and self).stepObj:
            if hasattr(self.stepObj, 'getQuestIndicatorOffset'):
                self.farEffect.setPos(self.stepObj.getQuestIndicatorOffset())
            else:
                self.farEffect.setPos(0, 0, 0)