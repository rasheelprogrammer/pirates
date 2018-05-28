# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.inventory.Lootable


class Lootable:
    __module__ = __name__

    def __init__(self):
        pass

    def startLooting(self, plunderList, itemsToTake=0, timer=0, autoShow=False, customName=None):
        self.itemsToTake = itemsToTake
        localAvatar.setPlundering(self.getDoId())
        localAvatar.guiMgr.inventoryUIManager.openPlunder(plunderList, self, customName, timer=timer, autoShow=autoShow)

    def stopLooting(self):
        if localAvatar.getPlundering() == self.getDoId():
            localAvatar.setPlundering(0)
            localAvatar.guiMgr.inventoryUIManager.closePlunder()

    def d_requestItem(self, itemInfo):
        self.sendUpdate('requestItem', [itemInfo])

    def d_requestItems(self, items):
        self.sendUpdate('requestItems', [items])

    def subtractItemsToTake(self, itemsToTake):
        self.itemsToTake -= itemsToTake

    def getItemsToTake(self):
        return self.itemsToTake

    def doneTaking(self):
        self.sendUpdate('doneTaking', [])

    def getRating(self):
        return -1

    def getTypeName(self):
        return ''