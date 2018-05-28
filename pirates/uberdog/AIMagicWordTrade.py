# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.AIMagicWordTrade
from AITrade import AITrade
from pirates.uberdog.UberDogGlobals import GiftOrigin, InventoryCategory, InventoryType, InventoryId
from direct.directnotify.DirectNotifyGlobal import directNotify

class AIMagicWordTrade(AITrade):
    __module__ = __name__
    notify = directNotify.newCategory('AIMagicWordTrade')

    def __init__(self, distObj, fromId, avatarId=None, inventoryId=None, timeout=4.0):
        AITrade.__init__(self, distObj, avatarId, inventoryId, timeout)
        self.giftOrigin = GiftOrigin.MAGIC_WORD
        self.fromId = fromId

    def _checkRules(self, givingLimitChanges, givingStacks, givingAccumulators, givingDoIds, givingLocatable, takingLimitChanges, takingStacks, takingAccumulators, takingDoIds, takingLocatable):
        pass

    def setAccumulator(self, accumulatorType, quantity):
        setAccumulator = InventoryId.getLimitChange(accumulatorType)
        self.giving.append((setAccumulator, quantity))

    def setReputation(self, category, amount):
        self.setAccumulator(category, amount)

    def getOrigin(self):
        return self.giftOrigin