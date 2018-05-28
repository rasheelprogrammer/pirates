# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestAvatarBase
from direct.directnotify.DirectNotifyGlobal import directNotify

class QuestAvatarBase:
    __module__ = __name__
    notify = directNotify.newCategory('QuestAvatarBase')

    def __init__(self):
        self.questNPCInterest = {}

    def getQuests(self):
        inventory = self.getInventory()
        if inventory is None:
            err = 'could not get inventory'
            if hasattr(self, 'doId'):
                err += ' for %s' % self.doId
            return []
        else:
            return inventory.getQuestList()
        return

    def getQuestById(self, questId):
        quests = self.getQuests()
        for currQuest in quests:
            if currQuest.questId == questId:
                return currQuest

        return

    def addQuestNPCInterest(self, npcId, questId):
        self.questNPCInterest[npcId] = questId
        messenger.send('questInterestChange-%s' % npcId, [])

    def removeQuestNPCInterest(self, npcId):
        self.questNPCInterest.pop(npcId, None)
        messenger.send('questInterestChange-%s' % npcId, [])
        return

    def hasQuestNPCInterest(self, npcId):
        return self.questNPCInterest.get(npcId)