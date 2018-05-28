# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.audio.PiratesAmbientManager
from direct.directnotify import DirectNotifyGlobal
from pirates.audio import AmbientManagerBase
from pirates.audio import SoundGlobals

class PiratesAmbientManager(AmbientManagerBase.AmbientManagerBase):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesAmbientManager')

    def __init__(self):
        AmbientManagerBase.AmbientManagerBase.__init__(self)
        self.volumeModifierDict = {SoundGlobals.AMBIENT_JUNGLE: 0.6, SoundGlobals.AMBIENT_SWAMP: 0.75, SoundGlobals.AMBIENT_JAIL: 1.25}

    def requestFadeIn(self, name, duration=5, finalVolume=1.0, priority=0):
        if name and not self.ambientDict.has_key(name):
            self.load(name, 'audio/' + name)
        AmbientManagerBase.AmbientManagerBase.requestFadeIn(self, name, duration, finalVolume, priority)

    def requestChangeVolume(self, name, duration, finalVolume, priority=0):
        newFinalVolume = finalVolume
        if name in self.volumeModifierDict.keys():
            newFinalVolume = finalVolume * self.volumeModifierDict[name]
        AmbientManagerBase.AmbientManagerBase.requestChangeVolume(self, name, duration, newFinalVolume, priority)