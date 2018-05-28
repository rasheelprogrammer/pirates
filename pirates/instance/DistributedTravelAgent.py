# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.instance.DistributedTravelAgent
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from pirates.piratesbase import PiratesGlobals

class DistributedTravelAgent(DistributedObjectGlobal):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedTravelAgent')

    @report(types=['args'], dConfigParam='dteleport')
    def d_requestTutorialTeleport(self):
        self.sendUpdate('requestTutorialTeleport')

    @report(types=['args'], dConfigParam='dteleport')
    def d_requestWelcomeWorldTeleport(self):
        self.sendUpdate('requestWelcomeWorldTeleport')

    @report(types=['args'], dConfigParam='dteleport')
    def d_requestLoginTeleport(self, shardId=0):
        self.sendUpdate('requestLoginTeleport', [shardId])

    @report(types=['args'], dConfigParam='dteleport')
    def d_requestInstanceTeleport(self, shardId=0):
        self.sendUpdate('requestInstanceTeleport', [shardId])