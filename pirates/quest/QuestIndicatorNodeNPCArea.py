# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestIndicatorNodeNPCArea
from pirates.piratesgui.RadarGui import *
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode
from direct.showbase.PythonUtil import report, StackTrace

class QuestIndicatorNodeNPCArea(QuestIndicatorGridNode):
    __module__ = __name__

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorGridNode.__init__(self, 'NPCAreaIndicator', [
         350, 400], questStep)
        self.wantBottomEffect = False
        return

    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        QuestIndicatorGridNode.delete(self)
        return

    def loadZoneLevel(self, level):
        QuestIndicatorGridNode.loadZoneLevel(self, level)

    def unloadZoneLevel(self, level):
        QuestIndicatorGridNode.unloadZoneLevel(self, level)

    def enterFar(self):
        QuestIndicatorGridNode.enterFar(self)
        self.updateGuiHints(localAvatar.activeQuestId)

    def enterNear(self):
        QuestIndicatorGridNode.enterNear(self)
        self.updateGuiHints(localAvatar.activeQuestId)

    def enterAt(self):
        QuestIndicatorGridNode.enterAt(self)

    def exitAt(self):
        pass

    def updateGuiHints(self, questId):
        if not hasattr(localAvatar, 'guiMgr') or not localAvatar.guiMgr:
            return
        hintText = ''
        quest = localAvatar.getQuestById(questId)
        if quest:
            if not quest.isComplete():
                state = self.state
                if hasattr(self, 'newState'):
                    state = self.newState
                state in ['At', 'Near'] and localAvatar.guiMgr.radarGui.showGlowRing()
                hintText = PLocalizer.TargetsCloseBy
            else:
                localAvatar.guiMgr.radarGui.hideGlowRing()
                hintText = PLocalizer.TargetsInHere
        else:
            localAvatar.guiMgr.radarGui.hideGlowRing()
        if self.minimapObject:
            self.minimapObject.mapGeom.stash()
        localAvatar.guiMgr.setQuestHintText(hintText)