# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.FireworkGlobals
from pandac.PandaModules import *
from pirates.world.LocationConstants import LocationIds
ShowPosHpr = {LocationIds.PORT_ROYAL_ISLAND: (Point3(-525, 1285, 150), Point3(-20, 0, 0)), LocationIds.TORTUGA_ISLAND: (Point3(10525, 19000, 245), Point3(0, 0, 0)), LocationIds.DEL_FUEGO_ISLAND: (Point3(7900, -25500, 325), Point3(55, 0, 0))}

def getShowPosition(locationId):
    return ShowPosHpr.get(locationId)[0]


def getShowOrientation(locationId):
    return ShowPosHpr.get(locationId)[1]


class FireworkTrailType:
    __module__ = __name__
    Default = 0
    Polygonal = 1
    Glow = 2
    Sparkle = 3
    GlowSparkle = 4
    LongSparkle = 5
    LongGlowSparkle = 6


class FireworkBurstType:
    __module__ = __name__
    Sparkles = 0
    PeonyShell = 1
    PeonyParticleShell = 2
    PeonyDiademShell = 3
    ChrysanthemumShell = 4
    ChrysanthemumDiademShell = 5
    RingShell = 6
    SaturnShell = 7
    BeeShell = 8
    SkullBlast = 9
    TrailExplosion = 10


class FireworkType:
    __module__ = __name__
    BasicPeony = 0
    AdvancedPeony = 1
    DiademPeony = 2
    Chrysanthemum = 3
    DiademChrysanthemum = 4
    Ring = 5
    Saturn = 6
    Bees = 7
    TrailBurst = 8
    GlowFlare = 9
    PalmTree = 10
    Mickey = 11
    PirateSkull = 12
    AmericanFlag = 13