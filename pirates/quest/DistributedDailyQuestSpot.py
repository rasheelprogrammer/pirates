# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.DistributedDailyQuestSpot
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedNode
from pirates.world import DistributedLocatableObject
from direct.showbase.PythonUtil import report

class DistributedDailyQuestSpot(DistributedNode.DistributedNode):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDailyQuestSpot')

    def __init__(self, cr):
        NodePath.NodePath.__init__(self, 'QuestSpot')
        DistributedNode.DistributedNode.__init__(self, cr)
        print 'New Daily Quest Spot'
        base.dqs = self

    def delete(self):
        DistributedNode.DistributedNode.delete(self)

    def generate(self):
        DistributedNode.DistributedNode.generate(self)

    def disable(self):
        DistributedNode.DistributedNode.disable(self)

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)

    def isBattleable(self):
        return 0

    def isInvisibleGhost(self):
        return 0