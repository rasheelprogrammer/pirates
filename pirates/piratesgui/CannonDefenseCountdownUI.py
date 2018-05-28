# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.CannonDefenseCountdownUI
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer

class CannonDefenseCountdownUI(NodePath):
    __module__ = __name__

    def __init__(self):
        NodePath.__init__(self, 'CountDown')

    def setTime(self, value):
        if value < 0:
            return
        number = TextNode('Number')
        number.setFont(PiratesGlobals.getInterfaceFont())
        number.setTextColor(PiratesGuiGlobals.TextFG1)
        number.setAlign(TextNode.ACenter)
        number.setShadow(0.05, 0.05)
        number.setShadowColor(0, 0, 0, 1)
        if value > 0:
            number.setText(str(value))
        else:
            number.setText(PLocalizer.CannonDefenseHelp['BeginGame'])
        numberNode = self.attachNewNode(number)
        numberNode.setTransparency(1)
        numberNode.setDepthTest(False)
        numberNode.setDepthWrite(False)
        seq = Sequence(Parallel(numberNode.scaleInterval(1, Vec3(0, 0, 0), Vec3(0.3, 0.3, 0.3)), numberNode.colorScaleInterval(1, Vec4(1, 1, 1, 0), Vec4(1, 1, 1, 1))), Func(numberNode.removeNode))
        seq.start()