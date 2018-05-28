# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Animal
from pirates.creature.Creature import Creature

class Animal(Creature):
    __module__ = __name__

    def __init__(self, animationMixer=None):
        Creature.__init__(self, animationMixer)

    @report(types=['module', 'args'], dConfigParam='nametag')
    def initializeNametag3d(self):
        pass

    def initializeNametag3dPet(self):
        Creature.initializeNametag3d(self)