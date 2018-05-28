# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pirate.HumanAnimationMixer
from direct.directnotify import DirectNotifyGlobal
from pirates.pirate.BipedAnimationMixer import BipedAnimationMixer

class HumanAnimationMixer(BipedAnimationMixer):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('HumanAnimationMixer')