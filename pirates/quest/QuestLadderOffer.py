# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestLadderOffer
from direct.showbase.PythonUtil import POD, makeTuple
from pirates.quest import QuestReward, QuestLadderDB

class QuestLadderOffer(POD):
    __module__ = __name__
    DataSet = {'questId': None, 'title': '', 'rewardStructs': tuple()}

    def __init__(self, questId=None, title=None, rewards=None):
        POD.__init__(self)
        if None not in (questId, title, rewards):
            self.setQuestId(questId)
            self.setTitle(title)
            self.setRewards(rewards)
        return

    def getRewards(self):
        rewards = []
        for rewardStruct in self.getRewardStructs():
            rewards.append(QuestReward.QuestReward.makeFromStruct(rewardStruct))

        return rewards

    def setRewards(self, rewards):
        rewardStructs = []
        for reward in makeTuple(rewards):
            rewardStructs.append(reward.getQuestRewardStruct())

        self.setRewardStructs(rewardStructs)

    def getQuestDNA(self):
        return QuestLadderDB.getContainer(self.questId)

    def isLadder(self):
        return True