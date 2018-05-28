# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.DistributedPirateProfileMgr
from direct.distributed import DistributedObject

class DistributedPirateProfileMgr(DistributedObject.DistributedObject):
    __module__ = __name__

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        base.cr.profileMgr = self

    def disable(self):
        DistributedObject.DistributedObject.disable(self)
        base.cr.profileMgr = None
        return

    def delete(self):
        DistributedObject.DistributedObject.disable(self)

    def requestAvatar(self, avId):
        self.sendUpdate('requestAvatar', [avId, localAvatar.getDoId()])

    def receiveAvatarInfo(self, dna, guildId, guildName, founder, hp, maxHp, voodoo, maxVoodoo, shardId, disableButtons, showGoTo):
        messenger.send('avatarInfoRetrieved', [dna, guildId, guildName, founder, hp, maxHp, voodoo, maxVoodoo, shardId, disableButtons, showGoTo])

    def receiveAvatarSkillLevels(self, level, cannon, sailing, cutlass, pistol, doll, dagger, grenade, staff, potions, fishing):
        messenger.send('avatarSkillLevelsRetrieved', [level, cannon, sailing, cutlass, pistol, doll, dagger, grenade, staff, potions, fishing])

    def receiveAvatarOnlineInfo(self, islandName, locationName, siege, profileIcon):
        messenger.send('avatarOnlineInfoRetrieved', [islandName, locationName, siege, profileIcon])

    def receiveAvatarShipInfo(self, guildState, crewState, friendState):
        messenger.send('avatarShipInfoRetrieved', [guildState, crewState, friendState])

    def receiveAvatarChatPermissions(self, chatPermission):
        messenger.send('avatarChatPermissionsRetrieved', [chatPermission])