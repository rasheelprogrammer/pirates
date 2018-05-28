# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.inventory.DistributedLootManager
from direct.distributed import DistributedObject

class DistributedLootManager(DistributedObject.DistributedObject):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        base.cr.lootMgr = self

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        base.cr.lootMgr = None
        return

    def delete(self):
        DistributedObject.DistributedObject.disable(self)

    def d_requestItemFromContainer(self, containerId, itemInfo):
        self.sendUpdate('requestItemFromContainer', [containerId, itemInfo])

    def d_requestItems(self, containers):
        self.sendUpdate('requestItems', [containers])

    def warnRemoveLootContainerFromScoreboard(self, containerId):
        if (hasattr(base, 'localAvatar') and base).localAvatar.guiMgr:
            scoreboard = base.localAvatar.guiMgr.scoreboard
            if scoreboard and hasattr(scoreboard, 'removeLootContainer'):
                messenger.send('Scoreboard-Loot-Timed-Out-Warning', [containerId])

    def removeLootContainerFromScoreboard(self, containerId):
        messenger.send('Scoreboard-Loot-Timed-Out', [containerId])
        if (hasattr(base, 'localAvatar') and base).localAvatar.guiMgr:
            scoreboard = base.localAvatar.guiMgr.scoreboard
            if scoreboard and hasattr(scoreboard, 'removeLootContainer'):
                scoreboard.removeLootContainer(containerId)