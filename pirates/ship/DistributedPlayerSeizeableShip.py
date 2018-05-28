# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.DistributedPlayerSeizeableShip
from direct.directnotify import DirectNotifyGlobal
from pirates.ship.DistributedPlayerSimpleShip import DistributedPlayerSimpleShip
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from direct.distributed.ClockDelta import *
from pirates.piratesgui import PiratesTimer

class DistributedPlayerSeizeableShip(DistributedPlayerSimpleShip):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedPlayerSeizeableShip')

    def __init__(self, cr=None, shipMgr=None, shipClass=None, isFlagship=0):
        DistributedPlayerSimpleShip.__init__(self, cr)
        self.allowCrewState = False
        self.allowFriendState = False
        self.allowGuildState = False
        self.allowPublicState = True
        self.captureTimer = None
        return

    def generate(self):
        self.setupAggroCollisions()
        DistributedPlayerSimpleShip.generate(self)

    def announceGenerate(self):
        DistributedPlayerSimpleShip.announceGenerate(self)

    def disable(self):
        self.cleanupAggroCollisions()
        DistributedPlayerSimpleShip.disable(self)

    def delete(self):
        if self.captureTimer:
            self.captureTimer.destroy()
            self.captureTimer = None
        DistributedPlayerSimpleShip.delete(self)
        return

    def getNPCship(self):
        return True

    def setShipClass(self, shipClass):
        self.hpModifier, self.cargoModifier, self.expModifier = ShipGlobals.getModifiedShipStats(self.level)
        DistributedPlayerSimpleShip.setShipClass(self, shipClass)

    def d_suggestResync(self, avId, timestampA, timestampB, serverTime, uncertainty):
        self.cr.timeManager.synchronize('suggested by %d' % avId)

    def enableShipForPlayerInteractions(self):
        self.enableOnDeckInteractions()

    def setSinkTimer(self, duration, timestamp):
        messenger.send('localAvatarToSea')
        if self.getTeam() != PiratesGlobals.PLAYER_TEAM:
            DistributedPlayerSimpleShip.setSinkTimer(self, duration, timestamp)
        else:
            self.sinkTime = duration
            self.sinkTimestamp = timestamp
            dt = globalClockDelta.localElapsedTime(self.sinkTimestamp)
            if self.shipStatusDisplay:
                if self.sinkTime > dt >= 0:
                    if not self.captureTimer:
                        self.captureTimer = PiratesTimer.PiratesTimer(showMinutes=True, alarmTime=10)
                        self.captureTimer.setFontColor(PiratesGuiGlobals.TextFG2)
                        self.captureTimer.reparentTo(self.shipStatusDisplay)
                        self.captureTimer.setScale(0.55)
                        self.captureTimer.setPos(0.62, 0, 0.0)
                        self.captureTimer.unstash()
                    self.captureTimer.setTime(self.sinkTime - dt)
                    self.captureTimer.countdown(self.sinkTime - dt)
                elif self.captureTimer:
                    self.captureTimer.destroy()
                    self.captureTimer = None
        return