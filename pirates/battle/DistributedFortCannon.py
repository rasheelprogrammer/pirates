# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.DistributedFortCannon
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.effects.Bonfire import Bonfire
from pirates.battle import DistributedIslandCannon

class DistributedFortCannon(DistributedIslandCannon.DistributedIslandCannon):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedFortCannon')

    def __init__(self, cr):
        DistributedIslandCannon.DistributedIslandCannon.__init__(self, cr)

    def loadModel(self):
        DistributedIslandCannon.DistributedIslandCannon.loadModel(self)

    def announceGenerate(self):
        DistributedIslandCannon.DistributedIslandCannon.announceGenerate(self)
        self.notify.debug('doId=%s pos=%s renderPos=%s parent=%s' % (self.doId, self.getPos(), self.getPos(render), self.getParent()))
        self.prop.fortId = self.fortId

    def setFortId(self, fortId):
        self.fortId = fortId

    def setDestructState(self, state):
        if state != self.destructState:
            self.destructState = state
            if self.destructState == PiratesGlobals.CANNON_STATE_DESTRUCT:
                self.request('Off')
            else:
                self.request('Idle')
                if self.bf:
                    self.bf.removeNode()
                    self.bf = None
        return