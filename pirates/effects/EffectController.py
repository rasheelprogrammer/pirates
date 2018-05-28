# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.EffectController
from pandac.PandaModules import *

class EffectController:
    __module__ = __name__
    particleDummy = None

    def __init__(self):
        self.track = None
        self.startEffect = None
        self.endEffect = None
        self.f = None
        self.p0 = None
        return

    def createTrack(self):
        pass

    @report(types=['args'], dConfigParam='quest-indicator')
    def destroy(self):
        self.finish()
        if self.f:
            self.f.cleanup()
        self.f = None
        self.p0 = None
        self.removeNode()
        return

    @report(types=['args'], dConfigParam='quest-indicator')
    def cleanUpEffect(self):
        self.setPosHpr(0, 0, 0, 0, 0, 0)
        if self.f:
            self.f.disable()
        self.detachNode()

    @report(types=['args'], dConfigParam='quest-indicator')
    def reallyCleanUpEffect(self):
        self.cleanUpEffect()
        self.finish()

    @report(types=['args'], dConfigParam='quest-indicator')
    def play(self, lod=None):
        if lod != None:
            try:
                self.createTrack(lod)
            except TypeError, e:
                raise TypeError('Error loading %s effect.' % self.__class__.__name__)

        else:
            self.createTrack()
        self.track.start()
        return

    @report(types=['args'], dConfigParam='quest-indicator')
    def stop(self):
        if self.track:
            self.track.pause()
            self.track = None
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        self.cleanUpEffect()
        return

    @report(types=['args'], dConfigParam='quest-indicator')
    def finish(self):
        if self.track:
            self.track.pause()
            self.track = None
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        return

    @report(types=['args'], dConfigParam='quest-indicator')
    def startLoop(self, lod=None):
        if lod != None:
            try:
                self.createTrack(lod)
            except TypeError, e:
                raise TypeError('Error loading %s effect.' % self.__class__.__name__)

        else:
            self.createTrack()
        if self.startEffect:
            self.startEffect.start()
        return

    @report(types=['args'], dConfigParam='quest-indicator')
    def stopLoop(self):
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect and not self.endEffect.isPlaying():
            self.endEffect.start()
        return

    @report(types=['args'], dConfigParam='quest-indicator')
    def getTrack(self):
        if not self.track:
            self.createTrack()
        return self.track

    @report(types=['args'], dConfigParam='quest-indicator')
    def enableEffect(self):
        if self.f:
            self.particleDummy and self.f.start(self, self.particleDummy)
        else:
            if self.f:
                self.f.start(self, self)

    @report(types=['args'], dConfigParam='quest-indicator')
    def disableEffect(self):
        if self.f:
            self.f.disable()