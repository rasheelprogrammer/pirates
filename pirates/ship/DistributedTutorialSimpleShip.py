# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.ship.DistributedTutorialSimpleShip
from pirates.audio import SoundGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
from pirates.ship.DistributedSimpleShip import DistributedSimpleShip

class DistributedTutorialSimpleShip(DistributedSimpleShip):
    __module__ = __name__

    def __init__(self, cr):
        DistributedSimpleShip.__init__(self, cr)
        self.interactTube = None
        return

    def announceGenerate(self):
        DistributedSimpleShip.announceGenerate(self)
        self.setupBoardingSphere(bitmask=PiratesGlobals.WallBitmask | PiratesGlobals.SelectBitmask | PiratesGlobals.RadarShipBitmask)
        self.addDeckInterest()

    def localPirateArrived(self, av):
        DistributedSimpleShip.localPirateArrived(self, av)
        if av.isLocal():
            self.gameFSM.stopCurrentMusic()
            self.gameFSM.startCurrentMusic(SoundGlobals.MUSIC_CUBA_COMBAT)

    def localPirateLeft(self, av):
        DistributedSimpleShip.localPirateLeft(self, av)