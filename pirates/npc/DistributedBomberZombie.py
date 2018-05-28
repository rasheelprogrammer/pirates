# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.DistributedBomberZombie
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from pirates.battle import DistributedBattleNPC
from pirates.npc import BomberZombie
from pirates.pirate import AvatarTypes
from pirates.battle import WeaponGlobals
from pirates.effects import CombatEffect
from pirates.effects.AttuneSmoke import AttuneSmoke
from pirates.effects import ExplodingBarrel
import NPCSkeletonGameFSM, random

class DistributedBomberZombie(DistributedBattleNPC.DistributedBattleNPC, BomberZombie.BomberZombie):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBomberZombie')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        BomberZombie.BomberZombie.__init__(self)

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        self.barrel = ExplodingBarrel.ExplodingBarrel()
        self.barrel.reparentTo(self.leftHandNode)
        self.barrel.setScale(0.88)
        self.barrel.lightUp()

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        self.setInteractOptions(isTarget=False, allowInteract=False)

    def disable(self):
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        BomberZombie.BomberZombie.disable(self)
        self.barrel.cleanUp()
        self.barrel.detachNode()
        self.barrel = None
        return

    def delete(self):
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        BomberZombie.BomberZombie.delete(self)

    def explode(self):
        if self.barrel:
            self.barrel.wrtReparentTo(self)
            self.barrel.explode()

    def getNameText(self):
        return BomberZombie.BomberZombie.getNameText(self)

    def setAvatarType(self, avatarType):
        BomberZombie.BomberZombie.setAvatarType(self, avatarType)
        DistributedBattleNPC.DistributedBattleNPC.setAvatarType(self, avatarType)

    def createGameFSM(self):
        self.gameFSM = NPCSkeletonGameFSM.NPCSkeletonGameFSM(self)

    def initializeDropShadow(self):
        BomberZombie.BomberZombie.initializeDropShadow(self)

    def setSpeed(self, forwardSpeed, rotateSpeed):
        if self.gameFSM.state == 'Jump':
            return
        BomberZombie.BomberZombie.setSpeed(self, forwardSpeed, rotateSpeed)

    def play(self, *args, **kwArgs):
        BomberZombie.BomberZombie.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        BomberZombie.BomberZombie.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        BomberZombie.BomberZombie.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        BomberZombie.BomberZombie.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        BomberZombie.BomberZombie.stop(self, *args, **kwArgs)

    def shouldNotice(self):
        return 0

    def _handleEnterAggroSphere(self, collEntry):
        pass

    def playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, itemEffects=[], multihit=0, targetBonus=0, skillResult=0):
        targetHp, targetPower, targetEffect, targetMojo, targetSwiftness = targetEffects
        if attacker:
            self.addCombo(attacker.getDoId(), attacker.currentWeaponId, skillId, -targetHp)
        self.cleanupOuchIval()
        if not targetBonus:
            if ammoSkillId:
                effectId = WeaponGlobals.getHitEffect(ammoSkillId)
            else:
                effectId = WeaponGlobals.getHitEffect(skillId)
        if not targetBonus:
            if not self.NoPain:
                if not self.noIntervals:
                    if targetEffects[0] < 0:
                        if self.gameFSM.state not in ('Ensnared', 'Knockdown', 'Stunned',
                                                      'Rooted', 'NPCInteract', 'ShipBoarding',
                                                      'Injured', 'Dying'):
                            ouchSfx = None
                            currentAnim = self.getCurrentAnim()
                            if currentAnim == 'run':
                                painAnim = 'run_hit'
                            else:
                                if currentAnim == 'walk':
                                    painAnim = 'walk_hit'
                                else:
                                    painAnim = 'idle_hit'
                            actorIval = self.actorInterval(painAnim, playRate=random.uniform(0.7, 1.5))
                            skillInfo = self.currentWeapon and WeaponGlobals.getIsStaffAttackSkill(skillId) and WeaponGlobals.getSkillAnimInfo(skillId)
                            getOuchSfxFunc = skillInfo[WeaponGlobals.OUCH_SFX_INDEX]
                            ouchSfx = getOuchSfxFunc and getOuchSfxFunc()
                    else:
                        ouchSfx = self.getSfx('pain')
                    self.ouchAnim = ouchSfx and Sequence(Func(base.playSfx, ouchSfx, node=self, cutoff=75), actorIval)
                else:
                    self.ouchAnim = actorIval
                self.ouchAnim.start()
        if self.combatEffect:
            self.combatEffect.destroy()
            self.combatEffect = None
        self.combatEffect = CombatEffect.CombatEffect(effectId, multihit, attacker)
        self.combatEffect.reparentTo(self)
        self.combatEffect.setPos(self, pos[0], pos[1], pos[2])
        if not WeaponGlobals.getIsDollAttackSkill(skillId) and not WeaponGlobals.getIsStaffAttackSkill(skillId):
            if attacker and not attacker.isEmpty():
                self.combatEffect.lookAt(attacker)
            self.combatEffect.setH(self.combatEffect, 180)
        self.combatEffect.play()
        if WeaponGlobals.getIsDollAttackSkill(skillId):
            self.voodooSmokeEffect2 = AttuneSmoke.getEffect()
            if self.voodooSmokeEffect2:
                self.voodooSmokeEffect2.reparentTo(self)
                self.voodooSmokeEffect2.setPos(0, 0, 0.2)
                self.voodooSmokeEffect2.play()
        return

    def _addInterruptedEffect(self, attackerId, duration):
        pass