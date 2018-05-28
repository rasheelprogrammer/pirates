# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.CannonSmokeSimple
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from PooledEffect import PooledEffect
from EffectController import EffectController

class CannonSmokeSimple(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.effectModel = model.find('**/particleWhiteSmoke')
        self.effectModel.setBillboardAxis(0)
        self.effectModel.reparentTo(self)
        self.effectModel.setPos(0, 1, 2.5)
        self.smoke = model.find('**/particleSmoke')
        self.smoke.setBillboardPointEye()
        self.smoke.reparentTo(self)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.hide()

    def createTrack(self):
        fadeBlast = LerpColorScaleInterval(self, 0.75, Vec4(1, 1, 1, 0.0), startColorScale=Vec4(1, 1, 1, 1))
        scaleBlast = LerpScaleInterval(self.effectModel, 0.75, Vec3(10, 10, 16), startScale=Vec3(6, 6, 12))
        scaleBlast2 = LerpScaleInterval(self.smoke, 0.75, 10, startScale=6)
        self.track = Sequence(Wait(0.1), Func(self.show), Parallel(fadeBlast, scaleBlast, scaleBlast2), Func(self.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)