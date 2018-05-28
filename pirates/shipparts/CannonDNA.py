# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.CannonDNA
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
from otp.speedchat import ColorSpace
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.ship import ShipGlobals
notify = directNotify.newCategory('CannonDNA')
CannonDict = {InventoryType.CannonL1: 'models/shipparts/cannon', InventoryType.CannonL2: 'models/shipparts/cannon', InventoryType.CannonL3: 'models/shipparts/cannon', ShipGlobals.Cannons.Tutorial: 'models/shipparts/cannon', ShipGlobals.Cannons.Skel_L1: 'models/shipparts/GP_cannon', ShipGlobals.Cannons.Skel_L2: 'models/shipparts/GP_cannon', ShipGlobals.Cannons.Skel_L3: 'models/shipparts/GP_cannon', ShipGlobals.Cannons.BP: 'models/shipparts/cannon_bp'}

class CannonDNA(AvatarDNA.AvatarDNA):
    __module__ = __name__

    def __init__(self):
        self.baseTeam = 0
        self.cannonType = 0
        self.ammoType = InventoryType.CannonRoundShot

    def __str__(self):
        string = 'decorType %s, posIndex %s, colorIndex %s' % (self.decorType, self.posIndex, self.colorIndex)
        return string

    def setBaseTeam(self, val):
        self.baseTeam = val

    def setCannonType(self, val):
        self.cannonType = val

    def getBaseTeam(self):
        return self.baseTeam

    def getCannonType(self):
        return self.cannonType