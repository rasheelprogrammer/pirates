# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.DistributedAnimal
from direct.directnotify import DirectNotifyGlobal
from pirates.creature import DistributedCreature
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPRender

class DistributedAnimal(DistributedCreature.DistributedCreature):
    __module__ = __name__

    def __init__(self, cr):
        DistributedCreature.DistributedCreature.__init__(self, cr)
        self.battleCollisionBitmask = PiratesGlobals.WallBitmask | PiratesGlobals.TargetBitmask
        OTPRender.renderReflection(False, self, 'p_animal', None)
        return

    def setupCreature(self, avatarType):
        DistributedCreature.DistributedCreature.setupCreature(self, avatarType)
        self.motionFSM.motionAnimFSM.setupSplashAnimOverride(self.creature.getSplashOverride())
        self.motionFSM.motionAnimFSM.setupSplashAnimOverrideDelay(12)

    def customInteractOptions(self):
        self.setInteractOptions(proximityText=None, allowInteract=False)
        return

    def showHpMeter(self):
        pass

    def isBattleable(self):
        return 0

    def initializeBattleCollisions(self):
        pass

    def getMinimapObject(self):
        return

    def canIdleSplashEver(self):
        return self.creature.getSplashOverride()

    def canIdleSplash(self):
        return self.creature.getCurrentAnim() == 'idle'