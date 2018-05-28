# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Monkey
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class Monkey(Creature):
    __module__ = __name__
    ModelInfo = ('models/char/monkey_hi', 'models/char/monkey_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('run', 'run'), ('pain', 'get_hit'), ('jump', 'jump'), ('taunt', 'taunt'))

    class AnimationMixer(Creature.AnimationMixer):
        __module__ = __name__
        notify = DirectNotifyGlobal.directNotify.newCategory('MonkeyAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'run': (LOOP['LOOP'],), 'pain': (ACTION['ACTION'],), 'jump': (ACTION['ACTION'],), 'taunt': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Monkey.sfx:
            for name in Monkey.SfxNames:
                Monkey.sfx[name] = loadSfx(Monkey.SfxNames[name])

        self.generateCreature()