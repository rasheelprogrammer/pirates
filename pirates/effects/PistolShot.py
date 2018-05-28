# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.PistolShot
from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
import random
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect
from EffectController import EffectController

class PistolShot(PooledEffect, EffectController):
    __module__ = __name__
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.flame = model.find('**/particleDot')
        self.flame.setBillboardAxis(0)
        self.flame.setPos(0, 0, 0.5)
        self.flame.reparentTo(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.flash = model.find('**/particleGlow')
        self.flash.setBillboardPointWorld(0.2)
        self.flash.setColorScale(1, 0.8, 0.8, 0.8)
        self.flash.reparentTo(self)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()

    def createTrack(self):
        scaleFlame = self.flame.scaleInterval(0.08, Vec3(1, 1, 4), startScale=Vec3(5, 5, 8))
        scaleFlash = self.flash.scaleInterval(0.06, 5, startScale=14)
        self.track = Sequence(Func(self.flame.show), Func(self.flash.show), Parallel(scaleFlame, scaleFlash), Func(self.flame.hide), Func(self.flash.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)