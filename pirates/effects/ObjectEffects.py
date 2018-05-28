# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.ObjectEffects
from pandac.PandaModules import *

def Defaults(objectNode):
    objectNode.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
    objectNode.setColorScale(1.0, 1.0, 1.0, 1.0)
    objectNode.setTransparency(0, 1)
    objectNode.setDepthWrite(1)
    objectNode.clearLight()


def Ghost_Effect(objectNode):
    objectNode.setTransparency(1, 1)
    objectNode.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
    objectNode.setColorScale(0.3, 0.6, 0.1, 0.6)
    objectNode.setDepthWrite(0)
    objectNode.setLightOff()
    objectNode.setFogOff()


OBJECT_EFFECTS = {'None': Defaults, 'Ghost': Ghost_Effect}