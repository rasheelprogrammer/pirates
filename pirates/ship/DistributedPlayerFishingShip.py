# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.DistributedPlayerFishingShip
from direct.directnotify import DirectNotifyGlobal
from pirates.ship.DistributedPlayerSimpleShip import DistributedPlayerSimpleShip
from pirates.minigame.DistributedFishingSpot import DistributedFishingSpot

class DistributedPlayerFishingShip(DistributedPlayerSimpleShip):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedPlayerFishingShip')

    def __init__(self, cr=None, shipMgr=None, shipClass=None, isFlagship=0, isFishing=True):
        DistributedPlayerSimpleShip.__init__(self, cr)
        self.pendingCannons = None
        self.isFishing = isFishing
        self.fishingSpots = {}
        self.maxFishingSpots = 6
        return

    def generate(self):
        DistributedPlayerSimpleShip.generate(self)

    def announceGenerate(self):
        DistributedPlayerSimpleShip.announceGenerate(self)

    def delete(self):
        self.isFishing = None
        self.fishingSpots = None
        self.maxFishingSpots = None
        DistributedPlayerSimpleShip.delete(self)
        return

    def setIsFishing(self, isFishing):
        self.isFishing = isFishing

    def registerFishingSpot(self, spot):
        if spot.index >= 0:
            locator = self.model.locators.find('**/cannon_%s;+s' % spot.index)
            self.loadFishingSpotAtLocator(spot, locator)
        else:
            print 'ERROR! This fishing spot needs an index!', spot

    def loadFishingSpotAtLocator(self, spot, locator):
        spot.model = loader.loadModel('models/minigames/pir_m_gam_fsh_fishingSpot')
        spot.model.reparentTo(self.getModelRoot())
        spot.model.setScale(1, 1, 1)
        spot.model.setPos(locator.getPos())
        spot.reparentTo(spot.model)