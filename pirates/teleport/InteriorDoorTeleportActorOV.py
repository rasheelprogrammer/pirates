# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.teleport.InteriorDoorTeleportActorOV
from pirates.piratesbase import PiratesGlobals
from pirates.teleport.DoorTeleportActorOV import DoorTeleportActorOV

class InteriorDoorTeleportActorOV(DoorTeleportActorOV):
    __module__ = __name__

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name='InteriorDoorTeleportActorOV'):
        DoorTeleportActorOV.__init__(self, cr, name)
        self.doorRequest = None
        return

    def disable(self):
        if self.doorRequest:
            base.cr.relatedObjectMgr.abortRequest(self.doorRequest)
            self.doorRequest = None
        DoorTeleportActorOV.disable(self)
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenGame(self, areaDoId, doorId):
        self.areaDoId = areaDoId
        self.doorId = doorId
        world = self.cr.getDo(self.worldDoId)
        world.goOnStage()
        area = self.cr.getDo(areaDoId)
        area.goOnStage()

        def doorArrived(door):
            doorLocator = door.getDoorLocator()
            localAvatar.reparentTo(doorLocator)
            localAvatar.setPosHpr(0, 10, 0, 0, 0, 0)
            localAvatar.wrtReparentTo(area)
            localAvatar.setP(0)
            localAvatar.setR(0)
            localAvatar.setScale(1)
            area.parentObjectToArea(localAvatar)
            area.handleEnterGameArea(None)
            localAvatar.enableGridInterest()
            area.manageChild(localAvatar)
            self._requestWhenInterestComplete('GameOpen')
            return

        def doorNotArrived(doIdList):
            self.notify.error('InteriorDoorTeleportActorOV.enterOpenGame: door %s never arrived in area %s' % (self.doorId, area.uniqueId))

        self.doorRequest = base.cr.relatedObjectMgr.requestObjects([self.doorId], eachCallback=doorArrived, timeout=60, timeoutCallback=doorNotArrived)

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterStartShow(self, *args):
        DoorTeleportActorOV.enterStartShow(self, *args)
        door = self.cr.getDo(self.doorId)
        messenger.send('fadeInInteriorDoor', [door.getBuildingUid()])
        base.cr.loadingScreen.hide()