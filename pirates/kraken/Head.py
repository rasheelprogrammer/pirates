# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.kraken.Head
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.pirate import AvatarTypes
from pirates.audio import SoundGlobals

class Head(Creature):
    __module__ = __name__
    ModelInfo = ('models/char/krakenHead-high', 'models/char/krakenHead-')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'pain': SoundGlobals.SFX_MONSTER_KRAKEN_PAIN, 'death': SoundGlobals.SFX_MONSTER_KRAKEN_DEATH})
    sfx = {}
    AnimList = (('idle', 'idle'), )

    class AnimationMixer(Creature.AnimationMixer):
        __module__ = __name__
        notify = DirectNotifyGlobal.directNotify.newCategory('CrabAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Head.sfx:
            for name in Head.SfxNames:
                Head.sfx[name] = loader.loadSfx('audio/' + Head.SfxNames[name])

        self.generateCreature()
        self.target = loader.loadModel('models/misc/smiley')
        self.target.reparentTo(self)

    def generateCreature(self):
        filePrefix = self.ModelInfo[1]
        try:
            self.loadModel(filePrefix + 'hi', 'modelRoot', 'hi', copy=1)
            self.loadModel(filePrefix + 'med', 'modelRoot', 'med', copy=1)
            self.loadModel(filePrefix + 'low', 'modelRoot', 'low', copy=1)
            hasLOD = True
            self.setLODs()
        except Exception, e:
            hasLOD = False
            self.loadModel(self.ModelInfo[0], copy=1)
        else:
            CreatureAnimDict = {}
            for anim in self.AnimList:
                CreatureAnimDict[anim[0]] = filePrefix + anim[1]

            if hasLOD:
                self.loadAnims(CreatureAnimDict, 'modelRoot', 'all')
            self.loadAnims(CreatureAnimDict)

    def uniqueName(self, name):
        return name + '-%s' % id(self)