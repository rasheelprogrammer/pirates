# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.BossBase
from pirates.piratesbase import PLocalizer
from pirates.battle import EnemyGlobals
from pirates.npc.BossNPCList import BOSS_NPC_LIST

class BossBase:
    __module__ = __name__

    def __init__(self, repository):
        pass

    def getAvatarType(self):
        pass

    def getLevel(self):
        pass

    def loadBossData(self, uniqueId, avatarType):
        if uniqueId:
            avatarType and self.loadBossDataUid(uniqueId)
        else:
            if avatarType:
                not uniqueId and self.loadBossDataAvatarType(avatarType)
            else:
                self.loadBossDataAvatarType(uniqueId, avatarType)

    def loadBossDataUid(self, uniqueId):
        defaultData = BOSS_NPC_LIST[''].copy()
        self.bossData = BOSS_NPC_LIST.get(uniqueId)
        defaultData.update(self.bossData)
        self.bossData = defaultData
        self.bossData['Name'] = PLocalizer.BossNPCNames[uniqueId]

    def loadBossDataAvatarType(self, avatarType):
        self.bossData = BOSS_NPC_LIST[''].copy()
        self.bossData['AvatarType'] = avatarType
        self.bossData['Name'] = PLocalizer.BossNames[avatarType.faction][avatarType.track][avatarType.id][avatarType.boss - 1]

    def loadBossDataHybrid(self, uniqueId, avatarType):
        defaultData = BOSS_NPC_LIST[''].copy()
        self.bossData = BOSS_NPC_LIST.get(uniqueId)
        defaultData.update(self.bossData)
        self.bossData = defaultData
        self.bossData['AvatarType'] = avatarType
        self.bossData['Name'] = PLocalizer.BossNPCNames[uniqueId]

    def _getBossName(self):
        return self.bossData['Name']

    def _getBossLevel(self):
        return self.bossData['Level']