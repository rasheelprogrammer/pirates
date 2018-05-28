# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.SeaSerpent
from pandac.PandaModules import *
from pirates.creature.SeaMonster import SeaMonster
from pirates.pirate import AvatarTypes
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class SeaSerpent(SeaMonster):
    __module__ = __name__
    ModelInfo = ('models/char/serpent_hi', 'models/char/serpent_')
    SfxNames = dict(SeaMonster.SfxNames)
    SfxNames.update({'death': SoundGlobals.SFX_MONSTER_SERPENT_DEATH, 'pain': SoundGlobals.SFX_MONSTER_SERPENT_PAIN})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('swim', 'swim'), ('walk', 'swim'), ('submerge', 'submerge'), ('attack', 'attack'), ('emerge', 'emerge'), ('death', 'submerge'))

    class AnimationMixer(SeaMonster.AnimationMixer):
        __module__ = __name__
        LOOP = SeaMonster.AnimationMixer.LOOP
        ACTION = SeaMonster.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'swim': (LOOP['LOOP'],), 'walk': (LOOP['LOOP'],), 'submerge': (ACTION['ACTION'],), 'attack': (ACTION['ACTION'],), 'emerge': (ACTION['ACTION'],), 'death': (ACTION['MOVIE'],)}

    def __init__(self):
        SeaMonster.__init__(self)
        self.setAvatarType(AvatarTypes.SeaSerpent)
        if not SeaSerpent.sfx:
            for name in SeaSerpent.SfxNames:
                SeaSerpent.sfx[name] = loadSfx(SeaSerpent.SfxNames[name])

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))