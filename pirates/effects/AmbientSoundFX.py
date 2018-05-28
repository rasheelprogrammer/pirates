# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.AmbientSoundFX
from pirates.leveleditor.LevelEntity import LevelEntity
from pandac.PandaModules import *

class AmbientSoundFX(LevelEntity):
    __module__ = __name__

    def __init__(self):
        LevelEntity.__init__(self)
        base.cr.timeOfDayManager.registerAmbientSFXNode(self)

    def setProperty(self, propertyName, propertyValue):
        if propertyName == 'None':
            pass
        else:
            if propertyName == 'Range':
                self.range = float(propertyValue)
            else:
                LevelEntity.setProperty(propertyName, propertyValue)

    def cleanUp(self):
        LevelEntity.cleanUp(self)
        if base.cr.timeOfDayManager:
            base.cr.timeOfDayManager.removeAmbientSFXNode(self)