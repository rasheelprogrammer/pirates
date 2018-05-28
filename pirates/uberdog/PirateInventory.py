# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.PirateInventory
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.DistributedInventory import DistributedInventory
from direct.directnotify.DirectNotifyGlobal import directNotify

class PirateInventory(DistributedInventory):
    __module__ = __name__
    notify = directNotify.newCategory('Inventory')

    def __init__(self, repository):
        DistributedInventory.__init__(self, repository)