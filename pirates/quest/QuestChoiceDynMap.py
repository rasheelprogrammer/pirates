# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestChoiceDynMap
from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestLadder
from pirates.quest import QuestLadderDB
from pirates.quest import QuestDB

class QuestChoiceDynMap:
    __module__ = __name__

    def __init__(self):
        self.QuestToChoiceSiblingMap = {}
        for ladderId, ladderDNA in QuestLadderDB.FortuneQuestLadderDict.items():
            ladderInt = ladderDNA.questInt
            for container in ladderDNA.getContainers():
                if container.isContainer():
                    if container.isChoice():
                        self.mapChoiceQuests(container.getContainers())
                    else:
                        self.getMappingFromContainer(container, ladderId, ladderInt)

        for ladderId, ladderDNA in QuestLadderDB.FameQuestLadderDict.items():
            ladderInt = ladderDNA.questInt
            for container in ladderDNA.getContainers():
                if container.isContainer():
                    if container.isChoice():
                        self.mapChoiceQuests(container.getContainers())
                    else:
                        self.getMappingFromContainer(container, ladderId, ladderInt)

    def getMappingFromContainer(self, container, ladderId, ladderInt):
        if container.isChoice():
            self.mapChoiceQuests(container.getContainers())
        for containerChild in container.getContainers():
            if containerChild.isContainer():
                self.getMappingFromContainer(containerChild, ladderId, ladderInt)

    def mapChoiceQuests(self, questTuple):
        idList = []
        for quest in questTuple:
            idList.append(quest.questId)

        for quest in questTuple:
            temp = list(idList)
            temp.remove(quest.questId)
            self.QuestToChoiceSiblingMap[quest.questId] = temp

    def getQuestSiblings(self, id):
        return self.QuestToChoiceSiblingMap.get(id, [])

    def getTrackableQuest(self, av, id):
        allSiblings = [
         id] + self.getQuestSiblings(id)
        trackableQuestId = None
        for questId in allSiblings:
            questObj = av.getQuestById(questId)
            if questObj:
                trackableQuestId = not questObj.isComplete() and questId
                break

        return trackableQuestId

    def printMapping(self):
        pass

    def findNewTrackableQuest(self, av):
        avQuests = av.getQuests()
        if avQuests:
            trackableQuestId = self.getTrackableQuest(av, avQuests[0].questId)
            if trackableQuestId:
                return trackableQuestId
            else:
                return avQuests[0].questId
        return