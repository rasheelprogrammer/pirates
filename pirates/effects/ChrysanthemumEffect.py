# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.ChrysanthemumEffect
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController

class ChrysanthemumEffect(NodePath, EffectController):
    __module__ = __name__

    def __init__(self):
        NodePath.__init__(self, 'ChrysanthemumEffect')
        EffectController.__init__(self)
        self.effectScale = 1.0
        self.effectColor = Vec4(1, 1, 1, 1)
        self.effectModel = loader.loadModel('models/effects/fireworkBurst_tflip')
        self.effectModel.setColorScale(Point4(0, 0, 0, 0))
        self.effectModel.reparentTo(self)
        self.seqNode = self.effectModel.getChild(0).getChild(0).node()
        self.effectModel2 = loader.loadModel('models/effects/fireworkBurst_tflip')
        self.effectModel2.setColorScale(Point4(0, 0, 0, 0))
        self.effectModel2.reparentTo(self)
        self.seqNode2 = self.effectModel2.getChild(0).getChild(0).node()
        model = loader.loadModel('models/effects/fireworkCards')
        self.stars = model.find('**/pir_t_efx_msc_fireworkStars_02')
        self.stars.setColorScale(Point4(0, 0, 0, 0))
        self.stars.reparentTo(self)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setBillboardPointWorld()
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()

    def createTrack(self):
        self.effectModel.setColorScale(0, 0, 0, 0)
        self.effectModel2.setColorScale(0, 0, 0, 0)
        self.stars.setColorScale(0, 0, 0, 0)
        fadeColor = self.effectColor - Vec4(0, 0, 0, 1)
        fadeBlast = self.effectModel.colorScaleInterval(1.25, fadeColor, startColorScale=Vec4(1, 1, 0.8, 1), blendType='easeIn')
        scaleBlast = self.effectModel.scaleInterval(0.5, 700 * self.effectScale, startScale=200 * self.effectScale, blendType='easeOut')
        fadeBlast2 = self.effectModel2.colorScaleInterval(1.0, fadeColor, startColorScale=Vec4(1, 1, 0.8, 1), blendType='easeIn')
        scaleBlast2 = self.effectModel2.scaleInterval(1.0, 720 * self.effectScale, startScale=250 * self.effectScale, blendType='easeOut')
        starsFadeIn = self.stars.colorScaleInterval(0.25, self.effectColor, startColorScale=Vec4(1, 1, 1, 0))
        starsFadeOut = self.stars.colorScaleInterval(1.0, Vec4(0, 0, 0, 0), startColorScale=self.effectColor, blendType='easeIn')
        starsScaleUp = self.stars.scaleInterval(1.5, 720 * self.effectScale, startScale=660 * self.effectScale, blendType='easeOut')
        self.track = Parallel(Func(self.effectModel.setColorScale, self.effectColor), Func(self.effectModel2.setColorScale, self.effectColor), scaleBlast, fadeBlast, scaleBlast2, fadeBlast2, starsScaleUp, Sequence(Wait(0.4), starsFadeIn, starsFadeOut, Wait(0.5), Func(self.cleanUpEffect)))

    def setEffectColor(self, color):
        self.effectColor = color

    def setEffectScale(self, scale):
        self.effectScale = scale