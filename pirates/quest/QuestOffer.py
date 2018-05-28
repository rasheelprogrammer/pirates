# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestOffer
from direct.showbase.PythonUtil import POD, makeTuple
from pirates.quest import QuestReward, QuestDB, QuestLadderDB

class QuestOffer(POD):
    __module__ = __name__
    DataSet = {'questId': None, 'title': '', 'initialTaskStates': tuple(), 'rewardStructs': tuple()}

    @staticmethod
    def create(questId, holder, timerReset=False, branchReset=False):
        if QuestDB.QuestDict.has_key(questId):
            questDNA = QuestDB.QuestDict[questId]
            initialTaskStates = questDNA.getInitialTaskStates(holder)
            rewards = questDNA.getRewards()
            if len(rewards) == 0:
                rewards = questDNA.computeRewards(initialTaskStates, holder)
        else:
            questDNA = QuestLadderDB.getContainer(questId)
            initialTaskStates = []
            rewards = []
        if timerReset:
            return QuestTimerResetOffer(questId, questId, initialTaskStates, rewards)
        if branchReset:
            return QuestBranchResetOffer(questId, questId, initialTaskStates, rewards)
        return QuestOffer(questId, questId, initialTaskStates, rewards)

    def __init__(self, questId=None, title=None, initialTaskStates=None, rewards=None):
        POD.__init__(self)
        if questId is not None:
            self.setQuestId(questId)
            self.setTitle(title)
            self.setInitialTaskStates(initialTaskStates)
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
            if reward:
                rewardStructs.append(reward.getQuestRewardStruct())

        self.setRewardStructs(rewardStructs)

    def getQuestDNA(self):
        if QuestDB.QuestDict.has_key(self.questId):
            return QuestDB.QuestDict[self.questId]
        else:
            return QuestLadderDB.getContainer(self.questId)

    def isLadder(self):
        if not QuestDB.QuestDict.has_key(self.questId):
            return True
        return False


class QuestTimerResetOffer(QuestOffer):
    __module__ = __name__


class QuestBranchResetOffer(QuestOffer):
    __module__ = __name__