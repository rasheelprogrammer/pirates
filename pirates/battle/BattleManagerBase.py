# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.BattleManagerBase
from direct.directnotify import DirectNotifyGlobal
from pirates.battle import WeaponGlobals
from pirates.minigame import PotionGlobals
from pirates.inventory import ItemGlobals
from pirates.pirate import AvatarTypes
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import EnemyGlobals
from pirates.battle.EnemySkills import EnemySkills
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PiratesGlobals

def isKraken(target):
    return hasattr(target, 'krakenId')


class BattleManagerBase:
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleManager')
    SkillRechargeTimeConfig = config.GetFloat('skill-recharge-time', -1.0)
    wantOutput = config.GetBool('show-attack-calc', 0)

    def isPVP(self, attacker, target):
        if target and target.getTeam() == PiratesGlobals.PLAYER_TEAM and attacker and attacker.getTeam() == PiratesGlobals.PLAYER_TEAM:
            return True
        return False

    def obeysPirateCode(self, attacker, target):
        if not hasattr(target, 'avatarType'):
            return True
        if (not target.isNpc and target).zombie:
            return True
        if (hasattr(target, 'isGhost') and target).isGhost:
            return True
        human = target.avatarType.isA(AvatarTypes.Navy) or target.avatarType.isA(AvatarTypes.Townfolk) or target.avatarType.isA(AvatarTypes.Pirate) or target.avatarType.isA(AvatarTypes.BountyHunter) or target.avatarType.isA(AvatarTypes.TradingCo)
        weaponType = ItemGlobals.getType(attacker.currentWeaponId)
        if human and weaponType == ItemGlobals.GUN:
            return False
        return True

    def willWeaponHit(self, attacker, target, skillId, ammoSkillId, charge):
        if not attacker.getWorld():
            return WeaponGlobals.RESULT_NOT_AVAILABLE
        inPVPMode = self.isPVP(attacker, target)
        chanceOfHit = WeaponGlobals.getAttackAccuracy(skillId, ammoSkillId)
        if target and not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
            if not inPVPMode and (config.GetBool('want-dev', 0) and not attacker.isInInvasion() and not target.isInInvasion() or (not hasattr(attacker, 'inInvasion') or not attacker.isInInvasion()) and (not hasattr(target, 'inInvasion') or not target.isInInvasion())):
                accuracyModifier = WeaponGlobals.getComparativeLevelAccuracyModifier(attacker, target)
                chanceOfHit = max(0.0, chanceOfHit + accuracyModifier)
        chanceOfParry = 0.0
        chanceOfDodge = 0.0
        chanceOfResist = 0.0
        skillEffects = attacker.getSkillEffects()
        potionMultiplier = 0.0
        for targetEffect in skillEffects:
            if targetEffect == WeaponGlobals.C_BLIND or targetEffect == WeaponGlobals.C_DIRT:
                chanceOfHit *= WeaponGlobals.BLIND_PERCENT
            else:
                if targetEffect == WeaponGlobals.C_TAUNT:
                    chanceOfHit *= WeaponGlobals.TAUNT_PERCENT
            if not attacker.isNpc:
                if targetEffect in [WeaponGlobals.C_ACCURACY_BONUS_LVL1, WeaponGlobals.C_ACCURACY_BONUS_LVL2, WeaponGlobals.C_ACCURACY_BONUS_LVL3]:
                    potionMultiplier += PotionGlobals.getPotionPotency(targetEffect)

        chanceOfHit *= 1.0 + potionMultiplier
        attackType = WeaponGlobals.getAttackClass(skillId)
        if target and hasattr(target, 'isNpc') and not target.isNpc:
            if attackType == WeaponGlobals.AC_MISSILE:
                if WeaponGlobals.C_MISSILE_SHIELD in target.getSkillEffects():
                    return WeaponGlobals.RESULT_PROTECT
                chanceOfDodge = target.getSkillRankBonus(InventoryType.PistolDodge)
            elif attackType == WeaponGlobals.AC_COMBAT:
                if WeaponGlobals.C_MELEE_SHIELD in target.getSkillEffects():
                    return WeaponGlobals.RESULT_PROTECT
                chanceOfParry = target.getSkillRankBonus(InventoryType.CutlassParry) * 100
                targetWeaponId = target.currentWeaponId
                if ItemGlobals.getSubtype(targetWeaponId) == ItemGlobals.SABRE:
                    chanceOfParry *= WeaponGlobals.SABRE_PARRY_BONUS
                chanceOfParry += WeaponGlobals.getSubtypeParryBonus(targetWeaponId)
                if WeaponGlobals.C_MASTERS_RIPOSTE in target.getSkillEffects():
                    chanceOfParry += WeaponGlobals.MASTERS_RIPOSTE_BONUS
            elif attackType == WeaponGlobals.AC_MAGIC:
                if WeaponGlobals.C_MAGIC_SHIELD in target.getSkillEffects():
                    return WeaponGlobals.RESULT_PROTECT
                chanceOfResist = target.getSkillRankBonus(InventoryType.DollSpiritWard) * 100
        if not attacker.isNpc:
            if attackType == WeaponGlobals.AC_MAGIC:
                pass
            elif attackType == WeaponGlobals.AC_MISSILE:
                chanceOfHit += attacker.getSkillRankBonus(InventoryType.PistolSharpShooter) * 100
                chanceOfDodge -= attacker.getSkillRankBonus(InventoryType.PistolSharpShooter) / 2.0 * 100
            elif attackType == WeaponGlobals.AC_COMBAT:
                pass
        randVal = attacker.battleRandom.getRandom('willWeaponHit:accuracy')
        hitRand = randVal
        hitRoll = chanceOfHit - randVal
        randVal = attacker.battleRandom.getRandom('willWeaponHit:dodge')
        dodgeRoll = chanceOfDodge - randVal
        randVal = attacker.battleRandom.getRandom('willWeaponHit:resist')
        resistRoll = chanceOfResist - randVal
        randVal = attacker.battleRandom.getRandom('willWeaponHit:parry')
        parryRoll = chanceOfParry - randVal
        if hitRoll < 0:
            return WeaponGlobals.RESULT_MISS
        if dodgeRoll >= 0:
            return WeaponGlobals.RESULT_DODGE
        if parryRoll >= 0:
            return WeaponGlobals.RESULT_PARRY
        if resistRoll >= 0:
            return WeaponGlobals.RESULT_RESIST
        return WeaponGlobals.RESULT_HIT

    def getModifiedSkillEffects(self, attacker, target, skillId, ammoSkillId, charge=0, distance=0.0):
        if not attacker.getWorld():
            return ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [])
        attackerEffects, targetEffects = WeaponGlobals.getAttackEffects(skillId, ammoSkillId)
        if self.wantOutput:
            print ''
            print 'Basic Effects attacker %s target %s' % (attackerEffects, targetEffects)
        itemEffects = []
        inPVPMode = self.isPVP(attacker, target)
        tHealth = targetEffects[0]
        tMojo = targetEffects[3]
        aHealth = attackerEffects[0]
        aMojo = attackerEffects[3]
        randVal = attacker.battleRandom.getRandom('getModifiedSkillEffect %s %s' % (attacker, target), range=[50, 100])
        if attacker.isNpc:
            minValue = -1
        else:
            minValue = 0
        if tHealth <= 0:
            if attacker.isNpc:
                tHealth = -1 * attacker.getMonsterDmg() * WeaponGlobals.getNPCModifier(skillId)
            oldTHealth = tHealth
            tHealth = min(tHealth * (randVal * 0.01), minValue)
            if self.wantOutput:
                print ' A - NPC Level Mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
        if tMojo < 0:
            tMojo = min(tMojo * (randVal * 0.01), minValue)
        buffId = WeaponGlobals.getSkillEffectFlag(ammoSkillId)
        if not attacker.isNpc:
            if not WeaponGlobals.isSelfUseSkill(skillId):
                if not inPVPMode or tHealth > 0:
                    damageMod = WeaponGlobals.getLevelDamageModifier(attacker.getLevel())
                    oldTHealth = tHealth
                    tHealth *= damageMod
                    tMojo *= damageMod
                    aHealth *= damageMod
                    print self.wantOutput and ' B - PC Level Mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
        if not WeaponGlobals.isSelfUseSkill(skillId):
            if hasattr(attacker, 'currentWeaponId'):
                attackerBonus, targetBonus = WeaponGlobals.getWeaponStats(attacker, attacker.currentWeaponId)
                if attackerBonus:
                    if targetBonus:
                        if aHealth > 0:
                            aHealth -= attackerBonus[0]
                        else:
                            if aHealth < 0:
                                aHealth += attackerBonus[0]
                        if tHealth > 0:
                            oldTHealth = tHealth
                            tHealth -= targetBonus[0]
                            if self.wantOutput:
                                print ' C - Positive Effect -  tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                        else:
                            if tHealth < 0:
                                oldTHealth = tHealth
                                tHealth += targetBonus[0]
                                if self.wantOutput:
                                    print ' D - Negative Effect - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                        if tMojo > 0:
                            tMojo -= targetBonus[3]
                        elif tMojo < 0:
                            tMojo += targetBonus[3]
            if not WeaponGlobals.isSelfUseSkill(skillId):
                scaleVal = 1
                if hasattr(attacker, 'currentWeaponId'):
                    scaleVal = WeaponGlobals.getWeaponDamageScale(attacker.currentWeaponId)
                    distanceModifiers = WeaponGlobals.getDistanceDamageModifier(attacker.currentWeaponId, skillId)
                    if distanceModifiers:
                        if WeaponGlobals.getAttackClass(skillId) != WeaponGlobals.AC_COMBAT:
                            for distanceModifier in distanceModifiers:
                                if distanceModifier[0] >= distance:
                                    scaleVal *= distanceModifier[1]
                                    break

                    aHealth *= scaleVal
                    oldTHealth = tHealth
                    tHealth *= scaleVal
                    if self.wantOutput:
                        print ' E - Distance Modifier - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                if hasattr(attacker, 'isNpc'):
                    if not attacker.isNpc:
                        attackClass = WeaponGlobals.getAttackClass(skillId)
                        oldTHealth = tHealth
                        tHealth *= 1.0 - WeaponGlobals.getSubtypeDamageModifier(attacker.currentWeaponId, attackClass)
                        if self.wantOutput:
                            print ' F - Sub Type Mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                    if hasattr(attacker, 'currentWeaponId'):
                        weaponPow = ItemGlobals.getPower(attacker.currentWeaponId) * WeaponGlobals.WEAPON_POWER_MULT
                        aHealth += aHealth * weaponPow
                        oldTHealth = tHealth
                        tHealth += tHealth * weaponPow
                        if self.wantOutput:
                            print ' G - Weapon Power Mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                    if not WeaponGlobals.isSelfUseSkill(skillId):
                        amt = attacker.getSkillRankBonus(skillId)
                        oldTHealth = tHealth
                        tHealth += tHealth * amt
                        if self.wantOutput:
                            print ' H - Skill Mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                        tMojo += tMojo * amt
                        aHealth += aHealth * amt
                    if ammoSkillId:
                        amt = attacker.getSkillRankBonus(ammoSkillId)
                        oldTHealth = tHealth
                        tHealth += tHealth * amt
                        if self.wantOutput:
                            print ' I - Ammo Skill Mod -  tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                        tMojo += tMojo * amt
                        aHealth += aHealth * amt
                    if hasattr(attacker, 'currentWeaponId'):
                        if WeaponGlobals.isVoodooWeapon(attacker.currentWeaponId):
                            amt = attacker.getSkillRankBonus(InventoryType.StaffSpiritLore)
                            tHealth += tHealth * amt
                            tMojo += tMojo * amt
                            aHealth += aHealth * amt
                        if WeaponGlobals.isVoodooWeapon(attacker.currentWeaponId):
                            if aMojo < 0:
                                amt = attacker.getSkillRankBonus(InventoryType.StaffConservation)
                                aMojo -= aMojo * amt
                                aMojo = min(aMojo, 1)
                            if WeaponGlobals.isBladedWeapon(attacker.currentWeaponId):
                                amt = attacker.getSkillRankBonus(InventoryType.DaggerBladeInstinct)
                                tHealth += tHealth * amt
                                tMojo += tMojo * amt
                                aHealth += aHealth * amt
                        if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_CANNON or WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_GRENADE:
                            amt = attacker.getSkillRankBonus(InventoryType.CannonBarrage)
                            oldTHealth = tHealth
                            tHealth += tHealth * amt
                            if self.wantOutput:
                                print ' I.1 - Barrage -  tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                            tMojo += tMojo * amt
                            aHealth += aHealth * amt
                        if skillId in WeaponGlobals.BackstabSkills:
                            if charge:
                                if attacker:
                                    if ItemGlobals.getSubtype(attacker.currentWeaponId) == ItemGlobals.DAGGER_SUBTYPE:
                                        oldTHealth = tHealth
                                        tHealth *= WeaponGlobals.BACKSTAB_BONUS
                                        if self.wantOutput:
                                            print ' I.2 - Backstab -  tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                                if attacker:
                                    if hasattr(attacker, 'isNpc'):
                                        if not attacker.isNpc:
                                            attackClass = WeaponGlobals.getAttackClass(skillId)
                                            if attackClass == WeaponGlobals.AC_GRENADE or attackClass == WeaponGlobals.AC_CANNON:
                                                aHealth -= aHealth * attacker.getSkillRankBonus(InventoryType.GrenadeToughness)
                                    if target:
                                        if hasattr(target, 'isNpc'):
                                            if not target.isNpc:
                                                attackClass = WeaponGlobals.getAttackClass(skillId)
                                                if attackClass == WeaponGlobals.AC_GRENADE or attackClass == WeaponGlobals.AC_CANNON:
                                                    oldTHealth = tHealth
                                                    tHealth -= tHealth * target.getSkillRankBonus(InventoryType.GrenadeToughness)
                                                    if self.wantOutput:
                                                        print ' I.3 - Toughness Cannon -  tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                                                if hasattr(target, 'currentWeaponId'):
                                                    oldTHealth = tHealth
                                                    tHealth *= 1.0 - WeaponGlobals.getAttackClassProtection(target.currentWeaponId, attackClass)
                                                    print self.wantOutput and ' I.4 - Toughness -  tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                                    if skillId in (InventoryType.PistolTakeAim, EnemySkills.PISTOL_SCATTERSHOT_AIM):
                                        if charge > 0:
                                            weaponType = ItemGlobals.getType(attacker.currentWeaponId)
                                            weaponSubType = ItemGlobals.getSubtype(attacker.currentWeaponId)
                                            maxCharge = WeaponGlobals.getAttackMaxCharge(skillId, ammoSkillId)
                                            if weaponType == ItemGlobals.GUN and weaponSubType == ItemGlobals.BLUNDERBUSS:
                                                maxCharge = maxCharge * 0.4
                                            charge = min(charge, maxCharge)
                                            oldTHealth = tHealth
                                            tHealth += tHealth * charge * 1.0
                                            if self.wantOutput:
                                                print ' I.5 - Charging -  tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                                            aHealth += aHealth * charge * 1.0
                                    randVal = attacker.battleRandom.getRandom('getModifiedSkillEffects:crit')
                                    if hasattr(attacker, 'currentWeaponId'):
                                        chanceOfCrit = 0
                                        if ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.CRITICAL):
                                            chanceOfCrit += WeaponGlobals.CRITICAL_BASE + ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.CRITICAL) * WeaponGlobals.CRITICAL_MOD
                                        if WeaponGlobals.getExtraCriticalChance(attacker.currentWeaponId, ammoSkillId):
                                            chanceOfCrit += WeaponGlobals.CRITICAL_BASE + WeaponGlobals.getExtraCriticalChance(attacker.currentWeaponId, ammoSkillId) * WeaponGlobals.CRITICAL_MOD
                                        critRoll = chanceOfCrit - randVal
                                        if critRoll >= 0:
                                            oldTHealth = tHealth
                                            tHealth *= WeaponGlobals.CRIT_MULTIPLIER
                                            if self.wantOutput:
                                                print ' J - Crit Mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                                            itemEffects.append(ItemGlobals.CRITICAL)
                                    if hasattr(attacker, 'currentWeaponId') and ItemGlobals.getSubtype(attacker.currentWeaponId) == ItemGlobals.SPIRIT and WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
                                        tHealth *= WeaponGlobals.SPIRIT_BONUS
                                    skillEffects = hasattr(attacker, 'getSkillEffects') and not WeaponGlobals.isSelfUseSkill(skillId) and attacker.getSkillEffects()
                                    if WeaponGlobals.C_OPENFIRE in skillEffects:
                                        if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_CANNON:
                                            tHealth *= WeaponGlobals.OPEN_FIRE_BONUS
                                            aHealth *= WeaponGlobals.OPEN_FIRE_BONUS
                                    if WeaponGlobals.C_WEAKEN in skillEffects:
                                        if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_COMBAT:
                                            tHealth = min(-1, tHealth - tHealth * WeaponGlobals.WEAKEN_PENALTY)
                                            aHealth = min(-1, aHealth - aHealth * WeaponGlobals.WEAKEN_PENALTY)
                                    potionMultiplier = attacker.isNpc or 0.0
                                    repId = WeaponGlobals.getSkillReputationCategoryId(skillId)
                                    for buff in skillEffects:
                                        if buff in [WeaponGlobals.C_CANNON_DAMAGE_LVL1, WeaponGlobals.C_CANNON_DAMAGE_LVL2, WeaponGlobals.C_CANNON_DAMAGE_LVL3] and repId == InventoryType.CannonRep or buff in [WeaponGlobals.C_PISTOL_DAMAGE_LVL1, WeaponGlobals.C_PISTOL_DAMAGE_LVL2, WeaponGlobals.C_PISTOL_DAMAGE_LVL3] and repId == InventoryType.PistolRep or buff in [WeaponGlobals.C_CUTLASS_DAMAGE_LVL1, WeaponGlobals.C_CUTLASS_DAMAGE_LVL2, WeaponGlobals.C_CUTLASS_DAMAGE_LVL3] and repId == InventoryType.CutlassRep or buff in [WeaponGlobals.C_DOLL_DAMAGE_LVL1, WeaponGlobals.C_DOLL_DAMAGE_LVL2, WeaponGlobals.C_DOLL_DAMAGE_LVL3] and repId == InventoryType.DollRep:
                                            potionMultiplier += PotionGlobals.getPotionPotency(buff)

                                    tHealth *= 1.0 + potionMultiplier
                                    aHealth *= 1.0 + potionMultiplier
                                if WeaponGlobals.C_DARK in skillEffects:
                                    tHealth += tHealth * WeaponGlobals.DARK_BOOST
                                    aHealth += aHealth * WeaponGlobals.DARK_BOOST
                                if WeaponGlobals.C_MONKEY_PANIC in skillEffects:
                                    tHealth += tHealth * WeaponGlobals.MONKEY_PANIC_ATTACK_BOOST
                                    aHealth += aHealth * WeaponGlobals.MONKEY_PANIC_ATTACK_BOOST
                                if WeaponGlobals.C_FURY in skillEffects:
                                    if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_COMBAT:
                                        tHealth += tHealth * WeaponGlobals.FURY_ATTACK_BOOST
                                        aHealth += aHealth * WeaponGlobals.FURY_ATTACK_BOOST
                                if WeaponGlobals.C_DARK_CURSE in skillEffects:
                                    tHealth += tHealth * WeaponGlobals.DARK_CURSE_BOOST
                                    aHealth += aHealth * WeaponGlobals.DARK_CURSE_BOOST
                                WeaponGlobals.C_GHOST_FORM in skillEffects and tHealth += tHealth * WeaponGlobals.GHOST_FORM_BOOST
                                aHealth += aHealth * WeaponGlobals.GHOST_FORM_BOOST
                        skillEffects = target and not WeaponGlobals.isSelfUseSkill(skillId) and hasattr(target, 'getSkillEffects') and target.getSkillEffects()
                        if WeaponGlobals.C_CURSE in skillEffects:
                            if WeaponGlobals.getAttackClass(skillId) != WeaponGlobals.AC_MAGIC:
                                tHealth += int(tHealth * WeaponGlobals.CURSED_DAM_AMP)
                                aHealth += int(aHealth * WeaponGlobals.CURSED_DAM_AMP)
                        if WeaponGlobals.C_BANE in skillEffects:
                            if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_COMBAT:
                                tHealth = min(-1, tHealth - tHealth * WeaponGlobals.BANE_PENALTY)
                                aHealth = min(-1, aHealth - aHealth * WeaponGlobals.BANE_PENALTY)
                        if WeaponGlobals.C_MOJO in skillEffects:
                            if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_MAGIC and not WeaponGlobals.isHealingSkill(skillId) and WeaponGlobals.getSkillEffectFlag(skillId) != WeaponGlobals.C_ATTUNE:
                                tHealth = min(-1, tHealth - tHealth * WeaponGlobals.MOJO_PENALTY)
                                aHealth = min(-1, aHealth - aHealth * WeaponGlobals.MOJO_PENALTY)
                        if WeaponGlobals.C_WARDING in skillEffects and not WeaponGlobals.isHealingSkill(skillId) and (attacker.isNpc or inPVPMode):
                            tHealth = min(-1, tHealth - tHealth * WeaponGlobals.WARDING_PENALTY)
                            aHealth = min(-1, aHealth - aHealth * WeaponGlobals.WARDING_PENALTY)
                        if WeaponGlobals.C_DARK_CURSE in skillEffects:
                            if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_MISSILE or WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_COMBAT:
                                tHealth = min(-1, tHealth - tHealth * WeaponGlobals.DARK_CURSE_PENALTY)
                                aHealth = min(-1, aHealth - aHealth * WeaponGlobals.DARK_CURSE_PENALTY)
                        tHealth = WeaponGlobals.C_GHOST_FORM in skillEffects and (WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_MISSILE or WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_COMBAT) and min(-1, tHealth - tHealth * WeaponGlobals.GHOST_FORM_PENALTY)
                        aHealth = min(-1, aHealth - aHealth * WeaponGlobals.GHOST_FORM_PENALTY)
        if target and 0:
            if ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.ANTI_VOODOO_ZOMBIE) and target.avatarType.isA(AvatarTypes.VoodooZombie):
                tHealth += tHealth * WeaponGlobals.ANTI_VOODOO_ZOMBIE_BOOST
        buff = WeaponGlobals.getSkillEffectFlag(skillId)
        ammoBuff = WeaponGlobals.getSkillEffectFlag(ammoSkillId)
        if target and not WeaponGlobals.isSelfUseSkill(skillId):
            if not inPVPMode:
                if hasattr(target, 'avatarType'):
                    avClass = EnemyGlobals.getMonsterClass(target.avatarType)
                    if avClass == EnemyGlobals.MONSTER:
                        if buff == WeaponGlobals.C_UNDEAD_KILLER or ammoBuff == WeaponGlobals.C_UNDEAD_KILLER:
                            oldTHealth = tHealth
                            tHealth = min(-1, tHealth * WeaponGlobals.RESIST_DAMAGE_PENALTY)
                            if self.wantOutput:
                                print ' K - Resist Monster Mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                    elif avClass == EnemyGlobals.SKELETON:
                        if buff == WeaponGlobals.C_MONSTER_KILLER or ammoBuff == WeaponGlobals.C_MONSTER_KILLER:
                            oldTHealth = tHealth
                            tHealth = min(-1, tHealth * WeaponGlobals.RESIST_DAMAGE_PENALTY)
                            if self.wantOutput:
                                print ' L - resist skel mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                    elif avClass == EnemyGlobals.HUMAN:
                        if buff == WeaponGlobals.C_MONSTER_KILLER or ammoBuff == WeaponGlobals.C_MONSTER_KILLER or buff == WeaponGlobals.C_UNDEAD_KILLER or ammoBuff == WeaponGlobals.C_UNDEAD_KILLER:
                            oldTHealth = tHealth
                            tHealth = min(-1, tHealth * WeaponGlobals.RESIST_DAMAGE_PENALTY)
                            if self.wantOutput:
                                print ' M - resist human mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
            if buff == WeaponGlobals.C_LIFEDRAIN or ammoBuff == WeaponGlobals.C_LIFEDRAIN:
                aHealth += abs(tHealth)
            else:
                if buff == WeaponGlobals.C_SOULTAP or ammoBuff == WeaponGlobals.C_SOULTAP:
                    aHealth -= attacker.hp * 0.666
                else:
                    if buff == WeaponGlobals.C_MONKEY_PANIC or ammoBuff == WeaponGlobals.C_MONKEY_PANIC:
                        aHealth += attacker.getMaxHp() * WeaponGlobals.MONKEY_PANIC_HEALTH_BOOST
            if WeaponGlobals.getIsDollAttackSkill(skillId):
                if not attacker.isNpc:
                    if WeaponGlobals.getSplitTarget(skillId):
                        if buff != WeaponGlobals.C_FULLSPLIT:
                            friendlyFire = WeaponGlobals.isFriendlyFire(skillId)
                            if friendlyFire:
                                numTargets = len(attacker.getFriendlyStickyTargets())
                            else:
                                numTargets = len(attacker.getHostileStickyTargets())
                            if numTargets > 1:
                                tHealth /= numTargets
                                tMojo /= numTargets
                        if attacker.isNpc:
                            aHealth *= self.getGameStatManager().getEnemyDamageNerf()
                            tHealth *= self.getGameStatManager().getEnemyDamageNerf()
                            tMojo *= self.getGameStatManager().getEnemyDamageNerf()
                        if not WeaponGlobals.isSelfUseSkill(skillId):
                            if target:
                                if not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId) and not inPVPMode and (config.GetBool('want-dev', 0) and not attacker.isInInvasion() and not target.isInInvasion() or (not hasattr(attacker, 'inInvasion') or not attacker.isInInvasion()) and (not hasattr(target, 'inInvasion') or not target.isInInvasion())):
                                    damageMod = WeaponGlobals.getComparativeLevelDamageModifier(attacker, target)
                                    numHits = WeaponGlobals.getNumHits(skillId, ammoSkillId)
                                    if numHits > 1:
                                        numHits += 1
                                    if tHealth <= 0:
                                        oldTHealth = tHealth
                                        tHealth = min(-numHits, tHealth * damageMod)
                                        if self.wantOutput:
                                            print ' N - Level Nurf Mod - tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                                    if aHealth <= 0:
                                        aHealth = min(0.0, aHealth * damageMod)
                                if inPVPMode:
                                    scale = WeaponGlobals.getWeaponPvpDamageScale(attacker.currentWeaponId)
                                    tHealth *= scale
                                    tMojo *= scale
                                    aHealth *= scale
                                if target and (config.GetBool('want-dev', 0) or hasattr(target, 'getArmorScale')):
                                    if tHealth < 0:
                                        oldTHealth = tHealth
                                        tHealth *= target.getArmorScale()
                                        tHealth = min(-1.0, tHealth)
                                        print self.wantOutput and ' O - Armor Mod -  tHealth Modified from %s to %s' % (oldTHealth, tHealth)
                            if target and hasattr(attacker, 'currentWeaponId') and tHealth < 0 and ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.DAMAGE_MANA):
                                tMojo += tHealth * (WeaponGlobals.DAMAGE_MANA_BASE + ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.DAMAGE_MANA) * WeaponGlobals.DAMAGE_MANA_MOD)
                            if ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.LEECH_HEALTH):
                                aHealth += -tHealth * (WeaponGlobals.LEECH_HEALTH_BASE + ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.LEECH_HEALTH) * WeaponGlobals.LEECH_HEALTH_MOD)
                            mojo = ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.LEECH_VOODOO) and hasattr(target, 'currentWeaponId') and (target.avatarType.isA(AvatarTypes.Pirate) or target.avatarType.isA(AvatarTypes.Muck) or target.avatarType.isA(AvatarTypes.Cadaver) or target.avatarType.isA(AvatarTypes.Splatter) or target.avatarType.isA(AvatarTypes.Drench) or target.avatarType.isA(AvatarTypes.JollyRoger)) and target.getMojo()
                            changeInMojo = -tHealth * (WeaponGlobals.LEECH_VOODOO_BASE + ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.LEECH_VOODOO) * WeaponGlobals.LEECH_VOODOO_MOD)
                            if mojo - changeInMojo < 0:
                                changeInMojo = mojo
                            tMojo -= changeInMojo
                            aMojo += changeInMojo
                targetEffects = [
                 tHealth, targetEffects[1], targetEffects[2], tMojo, targetEffects[4]]
                attackerEffects = [aHealth, attackerEffects[1], attackerEffects[2], aMojo, attackerEffects[4]]
                if not target:
                    for i in xrange(len(targetEffects)):
                        targetEffects[i] = 0

                targetEffects[0] = max(-30000, int(targetEffects[0]))
                targetEffects[3] = max(-30000, int(targetEffects[3]))
                attackerEffects[0] = max(-30000, int(attackerEffects[0]))
                attackerEffects[3] = max(-30000, int(attackerEffects[3]))
                if target and skillId == InventoryType.UseItem:
                    if buffId == WeaponGlobals.C_SHIPHEAL:
                        hpDelta = hasattr(target, 'updateSpDelta') and WeaponGlobals.getAttackHullHP(skillId, ammoSkillId)
                        spDelta = WeaponGlobals.getAttackSailHP(skillId, ammoSkillId)
                        if WeaponGlobals.C_FIX_IT_NOW in target.getSkillEffects():
                            hpDelta *= WeaponGlobals.FIX_IT_NOW_BONUS
                            spDelta *= WeaponGlobals.FIX_IT_NOW_BONUS
                        target.updateHpDelta(hpDelta)
                        target.updateSpDelta(spDelta)
            if attacker and skillId == InventoryType.UsePotion:
                if self.__class__.__name__ == 'BattleManagerAI':
                    simbase.config.GetBool('want-potion-game', 0) and taskMgr.doMethodLater(1.0, self.addPotionBuff, 'addPotionBuff%i%i' % (attacker.doId, buffId), extraArgs=[buffId, attacker])
        if self.wantOutput:
            print 'return effects attacker %s target %s' % (attackerEffects, targetEffects)
            print ''
        return (attackerEffects, targetEffects, itemEffects)

    def addPotionBuff(self, buffId, attacker):
        if attacker.isDeleted():
            return
        if buffId == WeaponGlobals.C_REMOVE_GROGGY:
            attacker.removeDeathPenalty()
        else:
            if PotionGlobals.getIsPotionBuff(buffId):
                duration = PotionGlobals.getPotionBuffDuration(buffId)
                inventoryTypeId = PotionGlobals.potionBuffIdToInventoryTypeId(buffId)
                attacker.skillProcessor.startEffect(buffId, 0, duration, attacker)

    def getModifiedSkillEffectsSword(self, attacker, target, skillId, ammoSkillId, charge=0, distance=0.0):
        if not target or not attacker.getWorld():
            return ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [])
        attackerEffects, targetEffects = WeaponGlobals.getAttackEffects(skillId, ammoSkillId)
        tHealth = targetEffects[0]
        tMojo = targetEffects[3]
        aHealth = attackerEffects[0]
        aMojo = attackerEffects[3]
        itemEffects = []
        inPVPMode = self.isPVP(attacker, target)
        randVal = attacker.battleRandom.getRandom('getModifiedSkillEffectSword %s' % tHealth, range=[50, 100])
        if attacker.isNpc:
            if not WeaponGlobals.isSelfUseSkill(skillId):
                minValue = -1
            else:
                minValue = 0
            if attacker.isNpc:
                if not WeaponGlobals.isSelfUseSkill(skillId):
                    tHealth = -1 * attacker.getMonsterDmg() * WeaponGlobals.getNPCModifier(skillId)
                tHealth = min(tHealth * (randVal * 0.01), minValue)
                if not attacker.isNpc:
                    if not inPVPMode:
                        damageMod = WeaponGlobals.getLevelDamageModifier(attacker.getLevel())
                        tHealth *= damageMod
                    if hasattr(attacker, 'currentWeaponId'):
                        attackerBonus, targetBonus = WeaponGlobals.getWeaponStats(attacker, attacker.currentWeaponId)
                        if tHealth != 0:
                            tHealth += targetBonus[0]
                    if hasattr(attacker, 'currentWeaponId'):
                        tHealth *= WeaponGlobals.getWeaponDamageScale(attacker.currentWeaponId)
                    tHealth += tHealth * attacker.getSkillRankBonus(skillId)
                    tHealth += tHealth * attacker.getSkillRankBonus(InventoryType.DaggerBladeInstinct)
                    if hasattr(attacker, 'currentWeaponId'):
                        if ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.ANTI_VOODOO_ZOMBIE):
                            if hasattr(target, 'avatarType'):
                                if target.avatarType.isA(AvatarTypes.VoodooZombie):
                                    tHealth += tHealth * WeaponGlobals.ANTI_VOODOO_ZOMBIE_BOOST
                                if hasattr(attacker, 'currentWeaponId'):
                                    if ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.BLOOD_FIRE):
                                        tHealth += tHealth * attacker.bloodFireLevel * ItemGlobals.BLOOD_FIRE_BONUS
                                    if target:
                                        if hasattr(target, 'currentWeaponId'):
                                            tHealth *= 1.0 - WeaponGlobals.getSubtypeDamageModifier(target.currentWeaponId, WeaponGlobals.AC_COMBAT)
                                            tHealth *= 1.0 - WeaponGlobals.getAttackClassProtection(target.currentWeaponId, WeaponGlobals.AC_COMBAT)
                                    if hasattr(attacker, 'currentWeaponId'):
                                        weaponPow = ItemGlobals.getPower(attacker.currentWeaponId) * WeaponGlobals.WEAPON_POWER_MULT
                                        tHealth += tHealth * weaponPow
                                    randVal = attacker.battleRandom.getRandom('getModifiedSkillEffects:crit')
                                    if hasattr(attacker, 'currentWeaponId'):
                                        chanceOfCrit = 0
                                        if ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.CRITICAL):
                                            chanceOfCrit += WeaponGlobals.CRITICAL_BASE + ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.CRITICAL) * WeaponGlobals.CRITICAL_MOD
                                        if WeaponGlobals.getExtraCriticalChance(attacker.currentWeaponId, ammoSkillId):
                                            chanceOfCrit += WeaponGlobals.CRITICAL_BASE + WeaponGlobals.getExtraCriticalChance(attacker.currentWeaponId, ammoSkillId) * WeaponGlobals.CRITICAL_MOD
                                        critRoll = chanceOfCrit - randVal
                                        if critRoll >= 0:
                                            tHealth *= WeaponGlobals.CRIT_MULTIPLIER
                                            itemEffects.append(ItemGlobals.CRITICAL)
                                    if hasattr(attacker, 'getSkillEffects'):
                                        skillEffects = attacker.getSkillEffects()
                                        if WeaponGlobals.C_WEAKEN in skillEffects:
                                            tHealth = min(-1, tHealth - tHealth * WeaponGlobals.WEAKEN_PENALTY)
                                        if not attacker.isNpc:
                                            potionMultiplier = 0.0
                                            repId = WeaponGlobals.getSkillReputationCategoryId(skillId)
                                            for buff in skillEffects:
                                                if buff in [WeaponGlobals.C_CUTLASS_DAMAGE_LVL1, WeaponGlobals.C_CUTLASS_DAMAGE_LVL2, WeaponGlobals.C_CUTLASS_DAMAGE_LVL3]:
                                                    repId == InventoryType.CutlassRep and potionMultiplier += PotionGlobals.getPotionPotency(buff)

                                            tHealth *= 1.0 + potionMultiplier
                                        if WeaponGlobals.C_DARK in skillEffects:
                                            tHealth += tHealth * WeaponGlobals.DARK_BOOST
                                        if WeaponGlobals.C_MONKEY_PANIC in skillEffects:
                                            tHealth += tHealth * WeaponGlobals.MONKEY_PANIC_ATTACK_BOOST
                                        if WeaponGlobals.C_FURY in skillEffects:
                                            tHealth += tHealth * WeaponGlobals.FURY_ATTACK_BOOST
                                    skillEffects = hasattr(target, 'getSkillEffects') and target.getSkillEffects()
                                    if WeaponGlobals.C_CURSE in skillEffects:
                                        tHealth += int(tHealth * WeaponGlobals.CURSED_DAM_AMP)
                                    if WeaponGlobals.C_BANE in skillEffects:
                                        tHealth = min(-1, tHealth - tHealth * WeaponGlobals.BANE_PENALTY)
                                    if WeaponGlobals.C_WARDING in skillEffects and (attacker.isNpc or inPVPMode):
                                        tHealth = min(-1, tHealth - tHealth * WeaponGlobals.WARDING_PENALTY)
                                    if WeaponGlobals.C_DARK_CURSE in skillEffects:
                                        tHealth = min(-1, tHealth - tHealth * WeaponGlobals.DARK_CURSE_PENALTY)
                                    tHealth = WeaponGlobals.C_GHOST_FORM in skillEffects and min(-1, tHealth - tHealth * WeaponGlobals.GHOST_FORM_PENALTY)
                            if hasattr(target, 'isTeamCombo'):
                                if target.isTeamCombo > 1:
                                    comboLength = target.combo
                                    bonus = WeaponGlobals.getComboBonus(comboLength)
                                    bonus and tHealth -= bonus
                        if not WeaponGlobals.isSelfUseSkill(skillId) and target and not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId) and (not hasattr(attacker, 'inInvasion') or not attacker.isInInvasion()) and (not hasattr(target, 'inInvasion') or not target.isInInvasion()) and not isKraken(target):
                            damageMod = WeaponGlobals.getComparativeLevelDamageModifier(attacker, target)
                            if inPVPMode:
                                damageMod = 1
                            numHits = WeaponGlobals.getNumHits(skillId, ammoSkillId)
                            if numHits > 1:
                                numHits += 1
                            if tHealth <= 0:
                                tHealth = min(-numHits, tHealth * damageMod)
                        attacker.isNpc and tHealth *= EnemyGlobals.ENEMY_DAMAGE_NERF
                    else:
                        if inPVPMode:
                            scale = WeaponGlobals.getWeaponPvpDamageScale(attacker.currentWeaponId)
                            tHealth *= scale
                    if target and (config.GetBool('want-dev', 0) or hasattr(target, 'getArmorScale')):
                        if tHealth < 0:
                            tHealth *= target.getArmorScale()
                            tHealth = min(-1.0, tHealth)
                    if target and hasattr(attacker, 'currentWeaponId') and tHealth < 0 and ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.DAMAGE_MANA):
                        tMojo += tHealth * (WeaponGlobals.DAMAGE_MANA_BASE + ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.DAMAGE_MANA) * WeaponGlobals.DAMAGE_MANA_MOD)
                    if ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.LEECH_HEALTH):
                        aHealth += -tHealth * (WeaponGlobals.LEECH_HEALTH_BASE + ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.LEECH_HEALTH) * WeaponGlobals.LEECH_HEALTH_MOD)
                    mojo = ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.LEECH_VOODOO) and hasattr(target, 'currentWeaponId') and (target.avatarType.isA(AvatarTypes.Pirate) or target.avatarType.isA(AvatarTypes.Muck) or target.avatarType.isA(AvatarTypes.Cadaver) or target.avatarType.isA(AvatarTypes.Splatter) or target.avatarType.isA(AvatarTypes.Drench) or target.avatarType.isA(AvatarTypes.JollyRoger)) and target.getMojo()
                    changeInMojo = -tHealth * (WeaponGlobals.LEECH_VOODOO_BASE + ItemGlobals.getWeaponAttributes(attacker.currentWeaponId, ItemGlobals.LEECH_VOODOO) * WeaponGlobals.LEECH_VOODOO_MOD)
                    if mojo - changeInMojo < 0:
                        changeInMojo = mojo
                    tMojo -= changeInMojo
                    aMojo += changeInMojo
        return (
         [
          int(aHealth), attackerEffects[1], attackerEffects[2], int(aMojo), attackerEffects[4]], [int(tHealth), targetEffects[1], targetEffects[2], int(tMojo), targetEffects[4]], itemEffects)

    def getModifiedShipEffects(self, skillId, ammoSkillId=0, distance=0.0):
        shipEffects = WeaponGlobals.getShipEffects(skillId, ammoSkillId)
        return shipEffects

    def addStats(self, attackerStats, targetStats, attackerBonusStats, targetBonusStats):
        for i in range(len(attackerStats)):
            if attackerStats[i] != 0:
                attackerStats[i] += attackerBonusStats[i]

        for i in range(len(targetStats)):
            if targetStats[i] != 0:
                targetStats[i] += targetBonusStats[i]

        return (
         attackerStats, targetStats)

    def damageModifier(self, level, attacker, damage):
        modifier = level * EnemyGlobals.CANNON_DAMAGE_MODIFIER_PER_LEVEL + EnemyGlobals.CANNON_BASE_DAMAGE_MODIFIER
        return int(damage * modifier)

    def getModifiedHullDamage(self, attacker, target, skillId, ammoSkillId):
        damage = WeaponGlobals.getAttackHullHP(skillId, ammoSkillId)
        if attacker:
            damage = self.damageModifier(attacker.getLevel(), attacker, damage)
        else:
            self.notify.warning('ship taking damage with no attacker')
        if hasattr(attacker, 'getSkillEffects'):
            skillEffects = attacker.getSkillEffects()
            if WeaponGlobals.C_WRECKHULL in skillEffects:
                damage *= WeaponGlobals.WRECK_HULL_BONUS
        finalDamage, itemEffects = self.getModifiedShipDamage(attacker, target, skillId, ammoSkillId, damage)
        return (
         finalDamage, itemEffects)

    def getModifiedSailDamage(self, attacker, target, skillId, ammoSkillId):
        damage = WeaponGlobals.getAttackSailHP(skillId, ammoSkillId)
        if attacker:
            damage = self.damageModifier(attacker.getLevel(), attacker, damage)
        else:
            self.notify.warning('ship taking damage with no attacker')
        if hasattr(attacker, 'getSkillEffects'):
            skillEffects = attacker.getSkillEffects()
            if WeaponGlobals.C_WRECKMASTS in skillEffects:
                damage *= WeaponGlobals.WRECK_MASTS_BONUS
        finalDamage, itemEffects = self.getModifiedShipDamage(attacker, target, skillId, ammoSkillId, damage)
        return (
         finalDamage, itemEffects)

    def getModifiedShipDamage(self, attacker, target, skillId, ammoSkillId, damage):
        if not attacker:
            return damage
        itemEffects = []
        if hasattr(attacker, 'ship'):
            if attacker.ship:
                damage *= attacker.ship.getDamageOutputModifier()
            else:
                if hasattr(attacker, 'getDamageOutputModifier'):
                    damage *= attacker.getDamageOutputModifier()
            if hasattr(target, 'ship'):
                target.ship and damage *= target.ship.getDamageInputModifier()
            else:
                if hasattr(target, 'getDamageInputModifier'):
                    damage *= target.getDamageInputModifier()
            if skillId != InventoryType.CannonShoot:
                amt = attacker.getSkillRankBonus(skillId)
                amt += 1.0
                damage *= amt
            if ammoSkillId:
                amt = attacker.getSkillRankBonus(ammoSkillId)
                amt += 1.0
                damage *= amt
            randVal = attacker.battleRandom.getRandom('getModifiedSkillEffects:crit')
            if hasattr(attacker, 'currentWeaponId'):
                chanceOfCrit = 0
                if ItemGlobals.getWeaponAttributes(attacker.getCurrentCharm(), ItemGlobals.CRITICAL):
                    chanceOfCrit += WeaponGlobals.CRITICAL_BASE + ItemGlobals.getWeaponAttributes(attacker.getCurrentCharm(), ItemGlobals.CRITICAL) * WeaponGlobals.CRITICAL_MOD
                if WeaponGlobals.getExtraCriticalChance(attacker.getCurrentCharm(), ammoSkillId):
                    chanceOfCrit += WeaponGlobals.CRITICAL_BASE + WeaponGlobals.getExtraCriticalChance(attacker.getCurrentCharm(), ammoSkillId) * WeaponGlobals.CRITICAL_MOD
                critRoll = chanceOfCrit - randVal
                if critRoll >= 0:
                    damage *= WeaponGlobals.CRIT_MULTIPLIER
                    itemEffects.append(ItemGlobals.CRITICAL)
            if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_CANNON or WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_GRENADE or skillId == EnemySkills.LEFT_BROADSIDE or skillId == EnemySkills.RIGHT_BROADSIDE:
                amt = attacker.getSkillRankBonus(InventoryType.CannonBarrage)
                amt += 1.0
                damage *= amt
            if skillId == EnemySkills.LEFT_BROADSIDE:
                amt = attacker.getSkillRankBonus(InventoryType.SailBroadsideLeft)
                amt += 1.0
                damage *= amt
            if skillId == EnemySkills.RIGHT_BROADSIDE:
                amt = attacker.getSkillRankBonus(InventoryType.SailBroadsideRight)
                amt += 1.0
                damage *= amt
            if hasattr(attacker, 'getSkillEffects'):
                skillEffects = attacker.getSkillEffects()
                for buff in skillEffects:
                    if buff == WeaponGlobals.C_OPENFIRE:
                        damage = damage * WeaponGlobals.OPEN_FIRE_BONUS
                    if buff in [WeaponGlobals.C_CANNON_DAMAGE_LVL1, WeaponGlobals.C_CANNON_DAMAGE_LVL2, WeaponGlobals.C_CANNON_DAMAGE_LVL3]:
                        damage *= 1.0 + PotionGlobals.getPotionPotency(buff)

            if (hasattr(attacker, 'ship') and attacker).ship:
                skillEffects = attacker.ship.getSkillEffects()
                for buff in skillEffects:
                    if buff == WeaponGlobals.C_INCOMING:
                        (skillId == EnemySkills.LEFT_BROADSIDE or skillId == EnemySkills.RIGHT_BROADSIDE) and damage *= 1.0 - WeaponGlobals.INCOMING_DAMAGE_REDUCTION

            if hasattr(target, 'getSkillEffects'):
                skillEffects = target.getSkillEffects()
                for buff in skillEffects:
                    if buff == WeaponGlobals.C_TAKECOVER:
                        damage = damage * WeaponGlobals.TAKE_COVER_BONUS
                    elif buff == WeaponGlobals.C_INCOMING:
                        damage *= 1.0 - WeaponGlobals.INCOMING_DAMAGE_REDUCTION

            if attacker.isNpc and ammoSkillId:
                scale = WeaponGlobals.getAmmoNPCDamageScale(ammoSkillId)
                damage *= scale
            if target:
                if hasattr(attacker, 'getNPCship') and attacker.getNPCship() or hasattr(target, 'getNPCship') and target.getNPCship():
                    damageMod = max(EnemyGlobals.MAX_COMPARATIVE_SHIP_LEVEL_DAMAGE_MOD, WeaponGlobals.getComparativeShipLevelDamageModifier(attacker, target))
                    damage = damage <= 0 and min(-1, damage * damageMod)
        return (
         int(damage), itemEffects)

    def getModifiedRechargeTime(self, av, skillId, ammoSkillId=0):
        if config.GetBool('instant-skill-recharge', 0):
            return 0.0
        if self.SkillRechargeTimeConfig >= 0.0:
            return self.SkillRechargeTimeConfig
        if skillId == InventoryType.CannonShoot or skillId == InventoryType.DefenseCannonShoot or skillId == EnemySkills.LEFT_BROADSIDE or skillId == EnemySkills.RIGHT_BROADSIDE:
            ammoSkillId = 0
        rechargeTime = WeaponGlobals.getAttackRechargeTime(skillId, ammoSkillId)
        if rechargeTime:
            if av:
                if not av.isNpc:
                    if WeaponGlobals.getIsShipSkill(skillId):
                        if hasattr(av.ship, 'getSkillEffects'):
                            skillEffects = av.ship.getSkillEffects()
                            for buff in skillEffects:
                                if buff == WeaponGlobals.C_RECHARGE:
                                    if skillId != InventoryType.SailPowerRecharge:
                                        rechargeTime *= WeaponGlobals.POWER_RECHARGE_RATE_REDUCTION

                    if skillId == InventoryType.CannonShoot:
                        rechargeTime *= 1.0 - (av.getSkillRank(InventoryType.CannonShoot) - 1) * WeaponGlobals.CANNON_SHOOT_RATE_REDUCTION
                    else:
                        if WeaponGlobals.getIsShipSkill(skillId):
                            if skillId == InventoryType.SailBroadsideLeft or skillId == InventoryType.SailBroadsideRight:
                                rechargeTime *= 1.0 - av.getSkillRankBonus(InventoryType.SailTaskmaster)
                        else:
                            if WeaponGlobals.isBladedWeapon(av.currentWeaponId):
                                rechargeTime *= 1.0 - av.getSkillRankBonus(InventoryType.DaggerFinesse)
                            if WeaponGlobals.getIsStaffAttackSkill(skillId) and WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.RADIAL_SKILL_INDEX:
                                rechargeTime *= 1.0 - av.getSkillRankBonus(InventoryType.StaffSpiritLore)
                    if not WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX:
                        if av.isWeaponDrawn:
                            rechargeTime *= WeaponGlobals.getSubtypeRechargeModifier(av.currentWeaponId)
                        skillId in (InventoryType.SailFullSail, InventoryType.SailComeAbout, InventoryType.SailRammingSpeed) and ItemGlobals.getWeaponAttributes(av.getCurrentCharm(), ItemGlobals.NAVIGATION) and rechargeTime *= WeaponGlobals.NAVIGATION_RECHARGE_RATE_REDUCTION
        return rechargeTime

    def getModifiedReloadTime(self, av, skillId, ammoSkillId=0):
        if config.GetBool('instant-skill-recharge', 0):
            return 0.0
        rechargeTime = WeaponGlobals.getAttackRechargeTime(0, ammoSkillId)
        if rechargeTime:
            if av:
                if not av.isNpc:
                    if WeaponGlobals.getIsCannonSkill(skillId):
                        if hasattr(av.ship, 'getSkillEffects'):
                            skillEffects = av.ship.getSkillEffects()
                            for buff in skillEffects:
                                if buff == WeaponGlobals.C_RECHARGE:
                                    rechargeTime *= WeaponGlobals.POWER_RECHARGE_RATE_REDUCTION

                    if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_CANNON:
                        amt = av.getSkillRankBonus(InventoryType.CannonRapidReload)
                        amt = 1.0 - amt
                        rechargeTime *= amt
        return rechargeTime

    def getModifiedAttackRange(self, av, skillId, ammoSkillId=0):
        range = WeaponGlobals.getAttackRange(skillId, ammoSkillId)
        if range:
            if av:
                if not av.isNpc:
                    attackType = WeaponGlobals.getAttackClass(skillId)
                    if attackType == WeaponGlobals.AC_MISSILE:
                        range += range * av.getSkillRankBonus(InventoryType.PistolEagleEye)
                    if ItemGlobals.getType(av.currentWeaponId) == ItemGlobals.GUN:
                        weaponRange = WeaponGlobals.getRange(av.currentWeaponId)
                        if weaponRange == ItemGlobals.SHORT:
                            range *= 0.4
                        else:
                            if weaponRange == ItemGlobals.MEDIUM:
                                range *= 1.0
                            else:
                                if weaponRange == ItemGlobals.LONG:
                                    range *= 1.5
                        range += WeaponGlobals.getExtraRange(av.currentWeaponId, ammoSkillId)
        return range

    def getModifiedAttackDeadzone(self, av, skillId, ammoSkillId=0):
        deadzone = 0
        if av and not av.isNpc and WeaponGlobals.hasDeadzone(av.currentWeaponId):
            return WeaponGlobals.DEADZONE_RANGE
        return deadzone

    def getModifiedAttackAreaRadius(self, av, skillId, ammoSkillId=0):
        aoeRadius = WeaponGlobals.getAttackAreaRadius(skillId, ammoSkillId)
        if aoeRadius:
            if av:
                if hasattr(av, 'isNpc'):
                    if not av.isNpc:
                        attackType = WeaponGlobals.getAttackClass(skillId)
                        amt = (attackType == WeaponGlobals.AC_GRENADE or attackType == WeaponGlobals.AC_CANNON) and av.getSkillRankBonus(InventoryType.GrenadeDemolitions)
                        amt += 1.0
                        aoeRadius *= amt
        return aoeRadius

    def getModifiedAttackReputation(self, attacker, target, skillId, ammoSkillId):
        reputation = WeaponGlobals.getAttackReputation(skillId, ammoSkillId)
        if reputation:
            reputation *= WeaponGlobals.getWeaponExperienceScale(attacker.currentWeaponId)
        return reputation

    def getModifiedExperienceGrade(self, attacker, target, skillId=0, ammoSkillId=0, currentWeaponId=0, repId=0, forColor=False):
        attackerLevel = 0
        targetLevel = 0
        isBoss = 0
        inv = None
        if attacker:
            attackerLevel = attacker.getLevel()
            inv = attacker.getInventory()
        if target:
            targetLevel = target.getLevel()
            isBoss = target.isBoss()
        if not attackerLevel or not targetLevel or not inv:
            return 0
        weaponLevel = 0
        if not repId:
            if currentWeaponId:
                repId = WeaponGlobals.getRepId(currentWeaponId)
            elif skillId or ammoSkillId:
                repId = WeaponGlobals.getSkillReputationCategoryId(skillId)
        if repId:
            value = inv.getReputation(repId)
            weaponLevel, leftoverValue = ReputationGlobals.getLevelFromTotalReputation(repId, value)
        levelWeight = 0
        if weaponLevel:
            levelWeight = 2
        expLevel = (attackerLevel + weaponLevel * 2) / (1 + levelWeight)
        if isBoss:
            targetLevel *= 1.5
        if not forColor:
            levelGrade = ((config.GetBool('want-dev', 0) and target.isInInvasion() or hasattr(target, 'inInvasion') and target.isInInvasion()) and EnemyGlobals).YELLOW
        else:
            if expLevel > targetLevel + self.getGameStatManager().getEnemyLevelThreshold():
                levelGrade = EnemyGlobals.GREY
            else:
                if expLevel > targetLevel:
                    levelGrade = EnemyGlobals.GREEN
                else:
                    if expLevel > targetLevel - self.getGameStatManager().getEnemyLevelThreshold():
                        levelGrade = EnemyGlobals.YELLOW
                    else:
                        levelGrade = EnemyGlobals.RED
        return levelGrade

    def getEnemyLevelThreshold(self):
        self.notify.error('getEnemyLevelThreshold: should be pure virtual')

    def getExperienceColor(self, av, target):
        levelRank = self.getModifiedExperienceGrade(av, target, currentWeaponId=av.currentWeaponId, forColor=True)
        if levelRank >= EnemyGlobals.RED:
            color = '\x01red\x01'
        else:
            if levelRank >= EnemyGlobals.YELLOW:
                color = '\x01yellow\x01'
            else:
                if levelRank >= EnemyGlobals.GREEN:
                    color = '\x01midgreen\x01'
                else:
                    if levelRank == EnemyGlobals.GREY:
                        color = '\x01grey\x01'
                    else:
                        color = '\x01white\x01'
        return color

    def getCannonDefenseDamage(self, attacker, target, skillId, ammoSkillId):
        damage = WeaponGlobals.getAttackHullHP(skillId, ammoSkillId)
        amt = attacker.getSkillRankBonus(InventoryType.CannonBarrage)
        amt += 1.0
        damage *= amt
        if hasattr(attacker, 'getSkillEffects'):
            skillEffects = attacker.getSkillEffects()
            for buff in skillEffects:
                if buff in [WeaponGlobals.C_CANNON_DAMAGE_LVL1, WeaponGlobals.C_CANNON_DAMAGE_LVL2, WeaponGlobals.C_CANNON_DAMAGE_LVL3]:
                    damage *= 1.0 + PotionGlobals.getPotionPotency(buff)

        return damage


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 compare
#                     compare_single (3)
#                          0. expr
#                             attribute (2)
#                                  0. expr
#                                     L. 495    3796  LOAD_GLOBAL           2  'WeaponGlobals'
#                                  1.           3799  LOAD_ATTR           128  'C_GHOST_FORM'
#                          1. expr
#                                       3802  LOAD_FAST            10  'skillEffects'
#                          2.           3805  COMPARE_OP            6  'in'
#              1. jmp_false (2)
#                  0.           3808  JUMP_IF_FALSE        38  'to 3849'
#                  1.           3811  POP_TOP          
#              2. expr
#                 L. 496    3812  LOAD_FAST            18  'tHealth'
#              3. come_from_opt
#      1. expr
#         binary_expr (3)
#              0. expr
#                           3815  LOAD_FAST            18  'tHealth'
#              1. expr
#                 attribute (2)
#                      0. expr
#                                   3818  LOAD_GLOBAL           2  'WeaponGlobals'
#                      1.           3821  LOAD_ATTR           129  'GHOST_FORM_BOOST'
#              2. binary_op
#                           3824  BINARY_MULTIPLY  
#      2. inplace_op
#                   3825  INPLACE_ADD      
#      3. store
#                   3826  STORE_FAST           18  'tHealth'
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 compare
#                     compare_single (3)
#                          0. expr
#                                       1248  LOAD_FAST            20  'repId'
#                          1. expr
#                             attribute (2)
#                                  0. expr
#                                               1251  LOAD_GLOBAL          36  'InventoryType'
#                                  1.           1254  LOAD_ATTR            74  'CutlassRep'
#                          2.           1257  COMPARE_OP            2  '=='
#              1. jmp_false (2)
#                  0.           1260  JUMP_IF_FALSE        23  'to 1286'
#                  1.           1263  POP_TOP          
#              2. expr
#                 L. 885    1264  LOAD_FAST            11  'potionMultiplier'
#              3. come_from_opt
#      1. expr
#         call (3)
#              0. expr
#                 attribute (2)
#                      0. expr
#                                   1267  LOAD_GLOBAL          75  'PotionGlobals'
#                      1.           1270  LOAD_ATTR            76  'getPotionPotency'
#              1. expr
#                           1273  LOAD_FAST            32  'buff'
#              2.           1276  CALL_FUNCTION_1       1  None
#      2. inplace_op
#                   1279  INPLACE_ADD      
#      3. store
#                   1280  STORE_FAST           11  'potionMultiplier'
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 L. 936    1756  LOAD_FAST            25  'bonus'
#              1. jmp_false (2)
#                  0.           1759  JUMP_IF_FALSE        14  'to 1776'
#                  1.           1762  POP_TOP          
#              2. expr
#                 L. 938    1763  LOAD_FAST            14  'tHealth'
#              3. come_from_opt
#      1. expr
#                   1766  LOAD_FAST            25  'bonus'
#      2. inplace_op
#                   1769  INPLACE_SUBTRACT 
#      3. store
#                   1770  STORE_FAST           14  'tHealth'
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 attribute (2)
#                      0. expr
#                         L. 962    2026  LOAD_FAST             1  'attacker'
#                      1.           2029  LOAD_ATTR            20  'isNpc'
#              1. jmp_false (2)
#                  0.           2032  JUMP_IF_FALSE        17  'to 2052'
#                  1.           2035  POP_TOP          
#              2. expr
#                 L. 965    2036  LOAD_FAST            14  'tHealth'
#              3. come_from_opt
#      1. expr
#         attribute (2)
#              0. expr
#                           2039  LOAD_GLOBAL         105  'EnemyGlobals'
#              1.           2042  LOAD_ATTR           106  'ENEMY_DAMAGE_NERF'
#      2. inplace_op
#                   2045  INPLACE_MULTIPLY 
#      3. store
#                   2046  STORE_FAST           14  'tHealth'
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 attribute (2)
#                      0. expr
#                                    122  LOAD_FAST             2  'target'
#                      1.            125  LOAD_ATTR             4  'ship'
#              1. jmp_false (2)
#                  0.            128  JUMP_IF_FALSE        23  'to 154'
#                  1.            131  POP_TOP          
#              2. expr
#                 L.1094     132  LOAD_FAST             5  'damage'
#              3. come_from_opt
#      1. expr
#         call (2)
#              0. expr
#                 attribute (2)
#                      0. expr
#                         attribute (2)
#                              0. expr
#                                            135  LOAD_FAST             2  'target'
#                              1.            138  LOAD_ATTR             4  'ship'
#                      1.            141  LOAD_ATTR             7  'getDamageInputModifier'
#              1.            144  CALL_FUNCTION_0       0  None
#      2. inplace_op
#                    147  INPLACE_MULTIPLY 
#      3. store
#                    148  STORE_FAST            5  'damage'
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 or (4)
#                      0. expr
#                         compare
#                             compare_single (3)
#                                  0. expr
#                                                990  LOAD_FAST             3  'skillId'
#                                  1. expr
#                                     attribute (2)
#                                          0. expr
#                                                        993  LOAD_GLOBAL          32  'EnemySkills'
#                                          1.            996  LOAD_ATTR            33  'LEFT_BROADSIDE'
#                                  2.            999  COMPARE_OP            2  '=='
#                      1. jmp_true (2)
#                          0.           1002  JUMP_IF_TRUE         16  'to 1021'
#                          1.           1005  POP_TOP          
#                      2. expr
#                         compare
#                             compare_single (3)
#                                  0. expr
#                                               1006  LOAD_FAST             3  'skillId'
#                                  1. expr
#                                     attribute (2)
#                                          0. expr
#                                                       1009  LOAD_GLOBAL          32  'EnemySkills'
#                                          1.           1012  LOAD_ATTR            34  'RIGHT_BROADSIDE'
#                                  2.           1015  COMPARE_OP            2  '=='
#                      3.         1018_0  COME_FROM          1002  '1002'
#              1. jmp_false (2)
#                  0.           1018  JUMP_IF_FALSE        21  'to 1042'
#                  1.           1021  POP_TOP          
#              2. expr
#                 L.1161    1022  LOAD_FAST             5  'damage'
#              3. come_from_opt
#      1. expr
#         binary_expr (3)
#              0. expr
#                           1025  LOAD_CONST            4  1.0
#              1. expr
#                 attribute (2)
#                      0. expr
#                                   1028  LOAD_GLOBAL          22  'WeaponGlobals'
#                      1.           1031  LOAD_ATTR            49  'INCOMING_DAMAGE_REDUCTION'
#              2. binary_op
#                           1034  BINARY_SUBTRACT  
#      2. inplace_op
#                   1035  INPLACE_MULTIPLY 
#      3. store
#                   1036  STORE_FAST            5  'damage'
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 compare
#                     compare_single (3)
#                          0. expr
#                             L.1236     619  LOAD_FAST             2  'skillId'
#                          1. expr
#                             tuple (4)
#                                  0. expr
#                                     attribute (2)
#                                          0. expr
#                                                        622  LOAD_GLOBAL           5  'InventoryType'
#                                          1.            625  LOAD_ATTR            42  'SailFullSail'
#                                  1. expr
#                                     attribute (2)
#                                          0. expr
#                                                        628  LOAD_GLOBAL           5  'InventoryType'
#                                          1.            631  LOAD_ATTR            43  'SailComeAbout'
#                                  2. expr
#                                     attribute (2)
#                                          0. expr
#                                                        634  LOAD_GLOBAL           5  'InventoryType'
#                                          1.            637  LOAD_ATTR            44  'SailRammingSpeed'
#                                  3.            640  BUILD_TUPLE_3         3  None
#                          2.            643  COMPARE_OP            6  'in'
#              1. jmp_false (2)
#                  0.            646  JUMP_IF_FALSE        45  'to 694'
#                  1.            649  POP_TOP          
#              2. expr
#                 and (4)
#                      0. expr
#                         call (4)
#                              0. expr
#                                 attribute (2)
#                                      0. expr
#                                                    650  LOAD_GLOBAL          45  'ItemGlobals'
#                                      1.            653  LOAD_ATTR            46  'getWeaponAttributes'
#                              1. expr
#                                 call (2)
#                                      0. expr
#                                         attribute (2)
#                                              0. expr
#                                                            656  LOAD_FAST             1  'av'
#                                              1.            659  LOAD_ATTR            47  'getCurrentCharm'
#                                      1.            662  CALL_FUNCTION_0       0  None
#                              2. expr
#                                 attribute (2)
#                                      0. expr
#                                                    665  LOAD_GLOBAL          45  'ItemGlobals'
#                                      1.            668  LOAD_ATTR            48  'NAVIGATION'
#                              3.            671  CALL_FUNCTION_2       2  None
#                      1. jmp_false (2)
#                          0.            674  JUMP_IF_FALSE        17  'to 694'
#                          1.            677  POP_TOP          
#                      2. expr
#                         L.1238     678  LOAD_FAST             4  'rechargeTime'
#                      3. come_from_opt
#              3. come_from_opt
#      1. expr
#         attribute (2)
#              0. expr
#                            681  LOAD_GLOBAL          12  'WeaponGlobals'
#              1.            684  LOAD_ATTR            49  'NAVIGATION_RECHARGE_RATE_REDUCTION'
#      2. inplace_op
#                    687  INPLACE_MULTIPLY 
#      3. store
#                    688  STORE_FAST            4  'rechargeTime'