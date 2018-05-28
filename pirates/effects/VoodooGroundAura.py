# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.VoodooGroundAura
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
from otp.otpbase import OTPRender
import random

class VoodooGroundAura(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_groundAura')
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.effectModel.setBillboardAxis(3)
        self.effectModel.setDepthWrite(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.setLightOff()
        self.effectModel.setTransparency(1)
        self.effectModel.reparentTo(self)
        self.effectModel.setScale(1.0)
        self.effectModel.hide(OTPRender.MainCameraBitmask)
        self.effectModel.showThrough(OTPRender.EnviroCameraBitmask)
        self.effectModel.setBin('shadow', -10)
        self.effectModel.setColorScale(0, 0, 0, 0)

    def createTrack(self):
        self.effectModel.setColorScale(0, 0, 0, 0)
        textureStage = self.effectModel.findAllTextureStages()[0]
        uvScroll = LerpFunctionInterval(self.setNewUVs, 1.25, toData=1.0, fromData=0.0, extraArgs=[self.effectModel, textureStage])
        fadeIn = LerpColorScaleInterval(self.effectModel, 0.5, self.effectColor)
        fadeOut = LerpColorScaleInterval(self.effectModel, 0.5, Vec4(0, 0, 0, 0))
        self.startEffect = Parallel(Func(uvScroll.loop), fadeIn)
        self.endEffect = Sequence(fadeOut, Func(uvScroll.pause), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(0.25), self.endEffect)

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def setEffectColor(self, color):
        self.effectColor = color

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        self.stop()
        if self.track:
            self.track = None
        self.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return