# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.MuzzleFlash
from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class MuzzleFlash(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.setColorScaleOff()
        self.startCol = Vec4(0.5, 0.5, 0.5, 1)
        self.fadeTime = 0.15
        self.flash = loader.loadModel('models/effects/lanternGlow')
        self.flash.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.flash.setDepthWrite(0)
        self.flash.setFogOff()
        self.flash.setColorScale(self.startCol)
        self.flash.setBillboardPointEye(0.2)
        self.flash.setBin('fixed', 120)
        self.flash.setScale(25)
        self.flash.reparentTo(self)
        self.flash.hide()

    def createTrack(self):
        fadeBlast = self.flash.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=self.startCol, blendType='easeOut')
        scaleBlast = self.flash.scaleInterval(self.fadeTime, 10, blendType='easeIn')
        self.track = Sequence(Func(self.flash.show), Parallel(fadeBlast, scaleBlast), Func(self.flash.hide), Func(self.flash.setColorScale, Vec4(1, 1, 1, 1)), Func(self.cleanUpEffect))
        self.reparentTo(render)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)