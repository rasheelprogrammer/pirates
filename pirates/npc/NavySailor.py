# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.NavySailor
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import Human
from pirates.pirate import AvatarTypes

class NavySailor(Human.Human):
    __module__ = __name__

    def __init__(self, avatarType=AvatarTypes.Navy):
        Human.Human.__init__(self)
        self.avatarType = avatarType