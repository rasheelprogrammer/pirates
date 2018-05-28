# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.instance.DistributedMatchMaker
from direct.distributed import DistributedObjectGlobal

class DistributedMatchMaker(DistributedObjectGlobal.DistributedObjectGlobal):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedMatchMaker')

    def __init__(self, cr):
        DistributedObjectGlobal.DistributedObjectGlobal.__init__(self, cr)

    def requestActivity(self, gameType, gameCategory=-1, options=[], shipIds=[]):
        self.notify.debug('requestActivity...')
        self.sendUpdate('requestActivity', [gameType, gameCategory, options, shipIds])

    def requestJoin(self, matchId):
        self.notify.debug('requestJoin...')
        self.sendUpdate('requestJoin', [matchId])

    def skipJoin(self, matchId, clearSearch=False):
        self.notify.debug('skipJoin %s %s...' % (matchId, clearSearch))
        self.sendUpdate('skipJoin', [matchId, clearSearch])

    def cancelRequest(self, matchId):
        self.sendUpdate('cancelRequest', [matchId])