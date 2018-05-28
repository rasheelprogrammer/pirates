# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.DistributedLocationManager
from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedLocationManager(DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('LocationManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def delete(self):
        self.ignoreAll()
        self.notify.warning('LocationManager is going offline')
        self.cr.locationMgr = None
        DistributedObject.delete(self)
        return

    def online(self):
        pass

    def queryOcean(self):
        self.requestQueryLocation(WorldGlobals.OCEAN)

    def queryIsland(self):
        self.requestQueryLocation(WorldGlobals.ISLAND)

    def queryTown(self):
        self.requestQueryLocation(WorldGlobals.TOWN)

    def queryBuilding(self):
        self.requestQueryLocation(WorldGlobals.BUILDING)

    def queryPort(self):
        self.requestQueryLocation(WorldGlobals.PORT)

    def queryGameArea(self):
        self.requestQueryLocation(WorldGlobals.GAMEAREA)

    def queryShip(self):
        self.requestQueryLocation(WorldGlobals.SHIP)

    def queryLocation(self, category):
        self.sendUpdate('requestLocation', [category])