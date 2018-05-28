# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.InventoryRequestGameType
from pirates.uberdog.InventoryRequestBase import InventoryRequestBase
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.world import GameTypeGlobals

class InventoryRequestGameType(InventoryRequestBase):
    __module__ = __name__

    def __init__(self):
        InventoryRequestBase.__init__(self)

    def getGameStyles(self, gameType, callback=None):
        self._getGameInfo(True, gameType, callback=callback)

    def getGameOptions(self, gameType, gameStyle=None, callback=None):
        self._getGameInfo(False, gameType, gameStyle, callback)

    def _getGameInfo(self, styles, gameType, gameStyle=None, callback=None):

        def gotGameInfo(info):
            requestId = DistributedInventoryBase.getLastInventoryRequestId()
            if requestId in self.myInventoryRequests:
                self.myInventoryRequests.remove(requestId)
            if callback:
                callback(info)

        if styles:
            inventoryRequestId, styles = GameTypeGlobals.getGameStyles(gameType, gameStyle, callback=gotGameInfo)
        else:
            inventoryRequestId, options = GameTypeGlobals.getGameOptions(gameType, gameStyle, callback=gotGameInfo)
        if inventoryRequestId != None:
            self.myInventoryRequests.append(inventoryRequestId)
        return