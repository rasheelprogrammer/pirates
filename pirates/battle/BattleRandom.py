# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.BattleRandom
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
from direct.showbase import RandomNumGen

class BattleRandom:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleRandom')

    def __init__(self, avId):
        self.avId = avId
        self.mainRandomGen = RandomNumGen.RandomNumGen(self.avId)
        self.attackRandomGen = RandomNumGen.RandomNumGen(self.avId)
        self.mainCounter = 0
        self.attackCounter = 0

    def delete(self):
        del self.mainRandomGen
        del self.attackRandomGen

    def advanceAttackSeed(self):
        seedVal = self.mainRandomGen.randint(0, (1 << 16) - 1)
        self.mainCounter += 1
        self.attackCounter = 0
        self.attackRandomGen = RandomNumGen.RandomNumGen(seedVal)

    def getRandom(self, debugString='Unknown', range=[1, 100]):
        minVal = range[0]
        maxVal = range[1]
        randVal = self.attackRandomGen.randint(minVal, maxVal)
        self.attackCounter += 1
        return randVal

    def makeRandomChoice(self, rList):
        self.attackCounter += 1
        return self.attackRandomGen.choice(rList)

    def resync(self, seed=None):
        if seed is None:
            seed = self.avId
        self.mainRandomGen = RandomNumGen.RandomNumGen(self.avId)
        self.attackRandomGen = RandomNumGen.RandomNumGen(self.avId)
        self.mainCounter = 0
        self.attackCounter = 0
        return