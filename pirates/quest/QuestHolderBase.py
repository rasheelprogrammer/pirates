# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestHolderBase


class QuestHolderBase:
    __module__ = __name__

    def __init__(self):
        self._rewardCollectors = {}

    def getQuests(self):
        raise 'derived must implement'

    def _addQuestRewardCollector(self, collector):
        cId = collector._serialNum
        self._rewardCollectors[cId] = collector

    def _removeQuestRewardCollector(self, collector):
        cId = collector._serialNum
        del self._rewardCollectors[cId]

    def _trackRewards(self, trade):
        for collector in self._rewardCollectors.itervalues():
            collector.collect(trade)