# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.kraken.KrakenBody
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.creature.Creature import Creature
from pirates.kraken.BodyGameFSM import BodyGameFSM
from pirates.piratesbase import PiratesGlobals
from pandac.PandaModules import *

class bp:
    __module__ = __name__
    kraken = bpdb.bpPreset(cfg='kraken', static=1)


class KrakenBody(Creature):
    __module__ = __name__
    ModelInfo = ('models/char/live_kraken_zero', 'models/char/live_kraken_zero')
    AnimList = {}

    def __init__(self):
        Creature.__init__(self)
        self.enableMixing()
        self.collideBattleMask = PiratesGlobals.TargetBitmask | PiratesGlobals.BattleAimBitmask

    def setupCollisions(self):
        from pandac.PandaModules import *
        coll = CollisionSphere((0, 0, 0), 1)
        cn = CollisionNode('KrakenCollisions')
        cn.addSolid(coll)
        self.collision = self.attachNewNode(cn)
        self.collision.node().setIntoCollideMask(self.collideBattleMask)
        self.collision.setScale(100)
        self.collision.setZ(-80)
        self.collision.flattenStrong()

    def generateCreature(self):
        self.loadModel(ModelInfo[0])