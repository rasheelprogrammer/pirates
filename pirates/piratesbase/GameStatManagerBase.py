# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesbase.GameStatManagerBase
from pirates.piratesbase import PiratesGlobals
from pirates.battle import EnemyGlobals

class GameStatManagerBase:
    __module__ = __name__
    from direct.directnotify import DirectNotifyGlobal
    notify = DirectNotifyGlobal.directNotify.newCategory('GameStatManagerBase')

    def __init__(self):
        self.aggroModelIndex = None
        return

    def disable(self):
        pass

    def delete(self):
        pass

    def getEnemyLevelThreshold(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ENEMY_LEVEL_THRESHOLD_MODEL0
        else:
            return EnemyGlobals.ENEMY_LEVEL_THRESHOLD_MODEL1

    def getEnemyDamageNerf(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ENEMY_DAMAGE_NERF_MODEL0
        else:
            return EnemyGlobals.ENEMY_DAMAGE_NERF_MODEL1

    def getEnemyHPNerf(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ENEMY_HP_NERF_MODEL0
        else:
            return EnemyGlobals.ENEMY_HP_NERF_MODEL1

    def getInstantAggroRadius(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.INSTANT_AGGRO_RADIUS_DEFAULT_MODEL1
        else:
            return EnemyGlobals.INSTANT_AGGRO_RADIUS_DEFAULT_MODEL0

    def getSelfHealAmount(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.SELF_HEAL_AMOUNT_MODEL1
        else:
            return EnemyGlobals.SELF_HEAL_AMOUNT_MODEL0

    def getDamageThreshold(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ATTACK_DAMAGE_THRESHOLD_MODEL1
        else:
            return EnemyGlobals.ATTACK_DAMAGE_THRESHOLD_MODEL0

    def getAccuracyThreshold(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ATTACK_ACCURACY_THRESHOLD_MODEL1
        else:
            return EnemyGlobals.ATTACK_ACCURACY_THRESHOLD_MODEL0