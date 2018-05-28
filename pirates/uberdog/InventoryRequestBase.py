# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.InventoryRequestBase
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase

class InventoryRequestBase:
    __module__ = __name__

    def __init__(self):
        self.myInventoryRequests = []

    def __del__(self):
        self.cancelAllInventoryRequests()

    def getInventory(self, inventoryId, callback, timeout=30):

        def gotInventory(inventory):
            requestId = DistributedInventoryBase.getLastInventoryRequestId()
            if requestId in self.myInventoryRequests:
                self.myInventoryRequests.remove(requestId)
            if callback:
                callback(inventory)

        requestId = DistributedInventoryBase.getInventory(inventoryId, gotInventory, timeout)
        if requestId:
            self.myInventoryRequests.append(requestId)
        return requestId

    def cancelGetInventory(self, requestId):
        if requestId in self.myInventoryRequests:
            self.myInventoryRequests.remove(requestId)
            DistributedInventoryBase.cancelGetInventory(requestId)
            return True
        return False

    def cancelAllInventoryRequests(self):
        canceled = False
        for currRequest in self.myInventoryRequests:
            DistributedInventoryBase.cancelGetInventory(currRequest)
            canceled = True

        self.myInventoryRequests = []
        return canceled