# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Monstrous


class Monstrous:
    __module__ = __name__

    def initializeMonstrousTags(self, rootNodePath):
        from pirates.piratesbase import PiratesGlobals
        rootNodePath.setPythonTag('MonstrousObject', self)
        self.setPythonTag('MonstrousObject', self)
        rootNodePath.setTag('objType', str(PiratesGlobals.COLL_MONSTROUS))
        self.setTag('objType', str(PiratesGlobals.COLL_MONSTROUS))

    def cleanupMontstrousTags(self, rootNodePath):
        rootNodePath.clearPythonTag('MonstrousObject')
        self.clearPythonTag('MonstrousObject')

    def initializeBattleCollisions(self):
        pass