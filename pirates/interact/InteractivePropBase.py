# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.interact.InteractivePropBase
from pandac.PandaModules import *

class InteractivePropBase:
    __module__ = __name__

    def getTransitionOffset(self):
        if self.modelPath == 'models/props/pir_m_prp_cnt_crate_ravensCove':
            return [
             Point3(0, 3.29, 0), Point3(180, 0, 0)]
        else:
            return [
             Point3(0, 0, 0), Point3(180, 0, 0)]

    def adjustPos(self, av):
        myOrigPos = self.getPos()
        myOrigHpr = self.getHpr()
        posOffset, hprOffset = self.getTransitionOffset()
        self.setPos(myOrigPos - posOffset)
        self.setHpr(myOrigHpr - hprOffset)
        myPos = self.getPos(av.getParent())
        myHpr = self.getHpr(av.getParent())
        self.setPos(myOrigPos)
        self.setHpr(myOrigHpr)
        av.setPos(myPos)
        av.setHpr(myHpr)