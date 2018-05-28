# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.PowderKegDomeExplosion
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class PowderKegDomeExplosion(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.speed = 0.75
        self.size = 40
        self.explosionSequence = 0
        self.explosion = loader.loadModel('models/effects/explosion_sphere')
        self.explosion.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
        self.explosion.setFogOff()
        self.explosion.setLightOff()
        self.explosion.reparentTo(self)
        self.explosion.setDepthWrite(0)
        self.hide()

    def createTrack(self, rate=1):
        self.speed = 0.5
        self.explosion.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.explosion.setScale(1)
        self.explosion.setColorScale(1, 1, 1, 0.45)
        fadeBlast = self.explosion.colorScaleInterval(self.speed * 0.9, Vec4(0, 0, 0, 0))
        waitFade = Sequence(Wait(self.speed * 0.5), fadeBlast)
        scaleUp = self.explosion.scaleInterval(self.speed, self.size, startScale=0.0, blendType='easeIn', other=render)
        self.track = Sequence(Func(self.show), Parallel(scaleUp, waitFade), Func(self.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)