# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.ExplosionFlip
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class ExplosionFlip(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.speed = 20.0
        self.explosionSequence = 0
        self.explosion = loader.loadModel('models/effects/explosion.bam')
        self.explosion.setBillboardAxis()
        self.explosion.setDepthWrite(0)
        self.explosion.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.explosion.setLightOff()
        self.explosion.setFogOff()
        self.explosion.setColorScaleOff()
        self.explosion.reparentTo(self)
        self.explosion.hide()

    def createTrack(self, rate=1):
        self.track = Sequence(Func(self.explosion.show), Wait(0.35), Func(self.explosion.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)