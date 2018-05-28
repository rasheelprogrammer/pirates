# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.CannonDefenseCamera
from pirates.minigame import CannonDefenseGlobals
from pirates.pirate.CannonCamera import CannonCamera
from direct.showbase.PythonUtil import ParamObj

class CannonDefenseCamera(CannonCamera):
    __module__ = __name__

    class ParamSet(CannonCamera.ParamSet):
        __module__ = __name__
        Params = {'minH': -60.0, 'maxH': 60.0, 'minP': -32.0, 'maxP': 2.0, 'sensitivityH': CannonDefenseGlobals.MOUSE_SENSITIVITY_H, 'sensitivityP': CannonDefenseGlobals.MOUSE_SENSITIVITY_P}

    def __init__(self, params=None):
        CannonCamera.__init__(self, params)
        self.keyboardRate = CannonDefenseGlobals.KEYBOARD_RATE

    def enterActive(self):
        CannonCamera.enterActive(self)
        camera.setPos(0, -20, 15)
        camera.setP(-25)

    def changeModel(self, prop):
        if self.cannonProp:
            if prop.ship:
                self.reparentTo(prop.ship.avCannonView)
            else:
                self.reparentTo(prop.hNode)
        self.cannonProp = prop