# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.teleport.TutorialTeleportActorOV
from pirates.teleport.DistributedTeleportActorOV import DistributedTeleportActorOV
from pirates.cutscene import CutsceneData

class TutorialTeleportActorOV(DistributedTeleportActorOV):
    __module__ = __name__

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name='TutorialTeleportActorOV', doEffect=True):
        DistributedTeleportActorOV.__init__(self, cr, name, doEffect=doEffect)

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenWorld(self, worldLocations, worldDoId):
        self.worldDoId = worldDoId
        self._requestWhenInterestComplete('WorldOpen')
        self.cr.setWorldStack(worldLocations, event='WorldOpen')

    @report(types=['args'], dConfigParam=['dteleport'])
    def exitOpenWorld(self):
        self._cancelInterestCompleteRequest()

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenGame(self, tutorialDoId, areaDoId, spawnPt):
        self.tutorialDoId = tutorialDoId
        self.areaDoId = areaDoId
        self.spawnPt = spawnPt
        world = self.cr.getDo(self.worldDoId)
        world.goOnStage()
        if localAvatar.style.getTutorial() == 0:
            tutorial = self.cr.getDo(self.tutorialDoId)
            tutorial.preloadCutscene(CutsceneData.PRELOADED_CUTSCENE_STAGE1)
        area = self.cr.getDo(areaDoId)
        area.goOnStage()
        self._requestWhenInterestComplete('GameOpen')
        area = self.cr.getDo(self.areaDoId)
        localAvatar.reparentTo(area)
        localAvatar.setPosHpr(area, *self.spawnPt)
        area.parentObjectToArea(localAvatar)
        localAvatar.enableGridInterest()
        area.manageChild(localAvatar)

    @report(types=['args'], dConfigParam=['dteleport'])
    def exitOpenGame(self):
        self._cancelInterestCompleteRequest()

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterStartShow(self, *args):
        self.cr.loadingScreen.hide()
        base.transitions.fadeIn()
        localAvatar.b_setGameState('LandRoam')
        self._requestWhenInterestComplete('Done')