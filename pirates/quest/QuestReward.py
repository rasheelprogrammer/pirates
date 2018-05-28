# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestReward
import random
from direct.showbase.PythonUtil import POD, invertDict, getSetterName
from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestRewardStruct
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
from pirates.piratesbase import CollectionMap
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.economy import EconomyGlobals
from pirates.battle import EnemyGlobals
from pirates.minigame import PlayingCardDropper
from pirates.makeapirate import JewelryGlobals, TattooGlobals, ClothingGlobals
from pirates.economy.EconomyGlobals import ItemId
from pirates.piratesbase import Freebooter
from pirates.inventory import ItemGlobals
from pirates.inventory.InventoryGlobals import Locations
REPFACTOR_HOLIDAY = 1
GOLDFACTOR_HOLIDAY = 1
REWARD_TO = 3

class QuestReward(POD):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('QuestReward')
    DataSet = {'amount': 1, 'questId': ''}

    def __init__(self, amount=None, bonus=False, **kwArgs):
        if amount is not None:
            kwArgs['amount'] = amount
        POD.__init__(self, **kwArgs)
        self.bonus = bonus
        return

    def applyTo(self, trade, av):
        raise 'derived must override'

    def getQuestRewardStruct(self):
        rewardStruct = QuestRewardStruct.QuestRewardStruct().copyFrom(self)
        rewardStruct.setRewardType(Class2DBId[self.__class__])
        return rewardStruct

    @staticmethod
    @exceptionLogged()
    def makeFromStruct(rewardStruct):
        return DBId2Class[rewardStruct.rewardType]().copyFrom(rewardStruct, strict=True)

    @staticmethod
    def getDescriptionText(rewards):
        if len(rewards) == 0:
            return ''
        if len(rewards) == 1:
            str = PLocalizer.QuestRewardDescS % rewards[0].getDescriptionText()
            if rewards[0].isBonus():
                str = PLocalizer.QuestRewardDescItemBonus + str
        else:
            rewardsStr = ''
            for reward in rewards:
                if not reward.isBonus():
                    rewardsStr += PLocalizer.QuestRewardDescItem % ('', reward.getDescriptionText())

            for reward in rewards:
                if reward.isBonus():
                    rewardsStr += PLocalizer.QuestRewardDescItem % (PLocalizer.QuestRewardDescItemBonus, reward.getDescriptionText())

            str = PLocalizer.QuestRewardDescM % rewardsStr
        return str

    @staticmethod
    def getItemId():
        return

    def isBonus(self):
        return self.bonus

    def setBonus(self, bonus):
        self.bonus = bonus

    def canGive(self, av):
        return True

    def isSame(self, otherReward):
        for currVal in self.DataSet:
            getterStr = getSetterName(currVal, prefix='get') + '()'
            otherVal = eval('otherReward.' + getterStr)
            myVal = eval('self.' + getterStr)
            if otherVal != myVal:
                return False

        return True


class GoldAmountReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        global GOLDFACTOR_HOLIDAY
        avId = av.getDoId()
        goldAmt = self.amount
        if Freebooter.getPaidStatusAI(avId):
            (REWARD_TO == 2 or REWARD_TO == 3) and goldAmt *= GOLDFACTOR_HOLIDAY
        else:
            if not Freebooter.getPaidStatusAI(avId) and (REWARD_TO == 1 or REWARD_TO == 3):
                goldAmt *= GOLDFACTOR_HOLIDAY
        trade.giveGoldInPocket(goldAmt)

    def getDescriptionText(self):
        goldAmt = self.amount
        text = PLocalizer.GoldRewardDesc % goldAmt
        if GOLDFACTOR_HOLIDAY == 2:
            text = +'\\ + ' + PLocalizer.LootGoldDouble % goldAmt
        return text

    def setGoldFactor(self, multiplier):
        global GOLDFACTOR_HOLIDAY
        GOLDFACTOR_HOLIDAY = multiplier


class GoldReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        avId = av.getDoId()
        goldAmt = EnemyGlobals.getMaxGoldDrop(None, self.amount, 5)
        if Freebooter.getPaidStatusAI(avId):
            (REWARD_TO == 2 or REWARD_TO == 3) and goldAmt *= GOLDFACTOR_HOLIDAY
        else:
            if not Freebooter.getPaidStatusAI(avId) and (REWARD_TO == 1 or REWARD_TO == 3):
                goldAmt *= GOLDFACTOR_HOLIDAY
        trade.giveGoldInPocket(goldAmt)
        return

    def getDescriptionText(self):
        goldAmt = EnemyGlobals.getMaxGoldDrop(None, self.amount, 5)
        text = PLocalizer.GoldRewardDesc % goldAmt
        if GOLDFACTOR_HOLIDAY == 2:
            text = +'\\ + ' + PLocalizer.LootGoldDouble % goldAmt
        return text

    def setGoldFactor(self, multiplier):
        global GOLDFACTOR_HOLIDAY
        GOLDFACTOR_HOLIDAY = multiplier


class PlayingCardReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        for i in range(self.amount):
            cardId = random.randint(0, 51)
            trade.giveStack(InventoryType.begin_Cards + cardId, 1)

        trade.setSuccessCallback(av.giveCardMessage, extraArgs=[InventoryType.begin_Cards + cardId])

    def getDescriptionText(self):
        if self.amount > 1:
            return PLocalizer.PlayingCardRewardDescPlural % self.amount
        else:
            return PLocalizer.PlayingCardRewardDesc % self.amount


class PlayingCardTier0Reward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        card = PlayingCardDropper.dropTier0()
        trade.givePlayingCard(card)
        trade.setSuccessCallback(av.giveCardMessage, extraArgs=[card])

    def getDescriptionText(self):
        return PLocalizer.PlayingCardRewardDesc % self.amount


class PlayingCardTier1Reward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        card = PlayingCardDropper.dropTier1()
        trade.givePlayingCard(card)
        trade.setSuccessCallback(av.giveCardMessage, extraArgs=[card])

    def getDescriptionText(self):
        return PLocalizer.PlayingCardRewardDesc % self.amount


class PlayingCardTier2Reward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        card = PlayingCardDropper.dropTier2()
        trade.givePlayingCard(card)
        trade.setSuccessCallback(av.giveCardMessage, extraArgs=[card])

    def getDescriptionText(self):
        return PLocalizer.PlayingCardRewardDesc % self.amount


class PlayingCardTier3Reward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        card = PlayingCardDropper.dropTier3()
        trade.givePlayingCard(card)
        trade.setSuccessCallback(av.giveCardMessage, extraArgs=[card])

    def getDescriptionText(self):
        return PLocalizer.PlayingCardRewardDesc % self.amount


class MaxHpReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveStack(InventoryType.Hp, self.amount)

    def getDescriptionText(self):
        return PLocalizer.MaxHpRewardDesc % self.amount


class MaxMojoReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveStack(InventoryType.Mojo, self.amount)

    def getDescriptionText(self):
        return PLocalizer.MaxMojoRewardDesc % self.amount


class LuckReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        raise 'TODO'

    def getDescriptionText(self):
        return PLocalizer.LuckRewardDesc % self.amount


class SwiftnessReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        raise 'TODO'

    def getDescriptionText(self):
        return PLocalizer.SwiftnessRewardDesc % self.amount


class CollectReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if self.amount >= InventoryType.begin_Collections and self.amount < InventoryType.end_Collections:
            trade.giveStackableTypeLimit(self.amount, 2)
            trade.giveStack(self.amount, 1)
            for i in range(CollectionMap.Collection_Set_Sizes[self.amount]):
                curItem = 1 + self.amount + i
                trade.giveStackableTypeLimit(curItem, 99)

    def getDescriptionText(self):
        return PLocalizer.Collections[self.amount]


class TreasureMapReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveNewTreasureMap('DistributedTreasureMap')

    def getDescriptionText(self):
        return PLocalizer.TreasureMapDesc


class ShipReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if av.constructedShipDoId:
            trade.giveShip(av.constructedShipDoId)
            trade.giveNewShipToken()
        av.constructedShipDoId = None
        return

    def getDescriptionText(self):
        return PLocalizer.ShipRewardDesc


class PistolUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        itemId = self.getItemId()
        if itemId:
            trade.giveWeapon(itemId)
            trade.setSuccessCallback(av.giveWeaponMessage, extraArgs=[self.amount])
            trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getItemId(self):
        if self.amount == ItemId.PISTOL_L1:
            return ItemGlobals.FLINTLOCK_PISTOL
        else:
            if self.amount == ItemId.PISTOL_L2:
                return ItemGlobals.DOUBLE_BARREL
            else:
                if self.amount == ItemId.PISTOL_L3:
                    return ItemGlobals.TRI_BARREL
                else:
                    if self.amount == ItemId.PISTOL_L4:
                        return ItemGlobals.HEAVY_TRI_BARREL
                    else:
                        if self.amount == ItemId.PISTOL_L5:
                            return ItemGlobals.GRAND_PISTOL
        return

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.PistolRewardDesc

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class PistolReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.givePistolTraining()
        trade.giveWeapon(self.getItemId())
        trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getDescriptionText(self):
        return PLocalizer.PistolRewardDesc

    def getItemId(self):
        return ItemGlobals.FLINTLOCK_PISTOL

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class DollReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveDollTraining()
        trade.giveWeapon(self.getItemId())
        trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getDescriptionText(self):
        return PLocalizer.DollRewardDesc

    def getItemId(self):
        return ItemGlobals.VOODOO_DOLL

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class DaggerUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        itemId = self.getItemId()
        if itemId:
            trade.giveWeapon(itemId)
            trade.setSuccessCallback(av.giveWeaponMessage, extraArgs=[self.amount])
            trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.DaggerRewardDesc

    def getItemId(self):
        if self.amount == ItemId.DAGGER_L1:
            return ItemGlobals.BASIC_DAGGER
        else:
            if self.amount == ItemId.DAGGER_L2:
                return ItemGlobals.BATTLE_DIRK
            else:
                if self.amount == ItemId.DAGGER_L3:
                    return ItemGlobals.MAIN_GAUCHE
                else:
                    if self.amount == ItemId.DAGGER_L4:
                        return ItemGlobals.COLTELLO
                    else:
                        if self.amount == ItemId.DAGGER_L5:
                            return ItemGlobals.BLOODLETTER

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class WeaponItemReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveWeapon(self.amount)

    def getDescriptionText(self):
        if PLocalizer.ItemNames.has_key(self.amount):
            return PLocalizer.ItemNames.get(self.amount)
        else:
            return 'No named Weapon'

    def getItemId(self):
        return self.amount


class CutlassItemReward(WeaponItemReward):
    __module__ = __name__


class GunItemReward(WeaponItemReward):
    __module__ = __name__


class DollItemReward(WeaponItemReward):
    __module__ = __name__


class DaggerItemReward(WeaponItemReward):
    __module__ = __name__


class GrenadeItemReward(WeaponItemReward):
    __module__ = __name__


class StaffItemReward(WeaponItemReward):
    __module__ = __name__


class CutlassUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        itemId = self.getItemId()
        if itemId:
            trade.giveWeapon(self.getItemId())
            trade.setSuccessCallback(av.giveWeaponMessage, extraArgs=[self.amount])
            trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.CutlassRewardDesc

    def getItemId(self):
        if self.amount == ItemId.CUTLASS_L1:
            return ItemGlobals.RUSTY_CUTLASS
        else:
            if self.amount == ItemId.CUTLASS_L2:
                return ItemGlobals.IRON_CUTLASS
            else:
                if self.amount == ItemId.CUTLASS_L3:
                    return ItemGlobals.STEEL_CUTLASS
                else:
                    if self.amount == ItemId.CUTLASS_L4:
                        return ItemGlobals.FINE_CUTLASS
                    else:
                        if self.amount == ItemId.CUTLASS_L5:
                            return ItemGlobals.PIRATE_BLADE
        return

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class DollUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        itemId = self.getItemId()
        if itemId:
            trade.giveWeapon(self.getItemId())
            trade.setSuccessCallback(av.giveWeaponMessage, extraArgs=[self.amount])
            trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.DollRewardDesc

    def getItemId(self):
        if self.amount == ItemId.DOLL_L1:
            return ItemGlobals.VOODOO_DOLL
        else:
            if self.amount == ItemId.DOLL_L2:
                return ItemGlobals.CLOTH_DOLL
            else:
                if self.amount == ItemId.DOLL_L3:
                    return ItemGlobals.WITCH_DOLL
                else:
                    if self.amount == ItemId.DOLL_L4:
                        return ItemGlobals.PIRATE_DOLL
                    else:
                        if self.amount == ItemId.DOLL_L5:
                            return ItemGlobals.TABOO_DOLL
        return

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class WandUpgradeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        itemId = self.getItemId()
        if itemId:
            trade.giveWeapon(self.getItemId())
            trade.setSuccessCallback(av.giveWeaponMessage, extraArgs=[self.amount])
            trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getDescriptionText(self):
        if PLocalizer.InventoryTypeNames.has_key(self.amount):
            return PLocalizer.InventoryTypeNames.get(self.amount)
        else:
            return PLocalizer.StaffRewardDesc

    def getItemId(self):
        if self.amount == ItemId.WAND_L1:
            return ItemGlobals.CURSED_STAFF
        else:
            if self.amount == ItemId.WAND_L2:
                return ItemGlobals.WARPED_STAFF
            else:
                if self.amount == ItemId.WAND_L3:
                    return ItemGlobals.REND_STAFF
                else:
                    if self.amount == ItemId.WAND_L4:
                        return ItemGlobals.HARROW_STAFF
                    else:
                        if self.amount == ItemId.WAND_L5:
                            return ItemGlobals.VILE_STAFF
        return

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class DaggerReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveDaggersTraining()
        trade.giveWeapon(self.getItemId())
        trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getDescriptionText(self):
        return PLocalizer.DaggerRewardDesc

    def getItemId(self):
        return ItemGlobals.BASIC_DAGGER

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class GrenadeReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveGrenadeTraining()
        trade.giveWeapon(self.getItemId())
        trade.giveStack(InventoryType.GrenadeExplosion, 2)
        trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getDescriptionText(self):
        return PLocalizer.GrenadeRewardDesc

    def getItemId(self):
        return ItemGlobals.GRENADE_POUCH

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class StaffReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveWandTraining()
        trade.giveWeapon(self.getItemId())
        trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeWeapon])

    def getDescriptionText(self):
        if self.bonus:
            return PLocalizer.StaffRewardDescBurnt
        else:
            return PLocalizer.StaffRewardDesc

    def getItemId(self):
        if self.bonus:
            return ItemGlobals.BURNT_STAFF
        else:
            return ItemGlobals.CURSED_STAFF

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeWeapon) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeWeapon)
                return False
            return True
        return False


class CharmReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveCharm(self.getItemId())
        trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeCharm])

    def getDescriptionText(self):
        return PLocalizer.CharmRewardDesc

    def getItemId(self):
        return ItemGlobals.BANDIT_SEA_GLOBE

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeCharm) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeCharm)
                return False
            return True
        return False


class TeleportTotemReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveTortugaTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.TeleportTotemRewardDesc


class CubaTeleportReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveCubaTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.CubaTeleportRewardDesc


class PortRoyalTeleportReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.givePortRoyalTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.PortRoyalTeleportRewardDesc


class PadresDelFuegoTeleportReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.givePadresDelFuegoTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.PadresDelFuegoTeleportRewardDesc


class KingsHeadTeleportReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveKingsheadTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.KingsHeadTeleportRewardDesc


class RavensCoveTeleportReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        trade.giveRavensCoveTeleportToken()

    def getDescriptionText(self):
        return PLocalizer.RavensCoveTeleportRewardDesc


class MainStoryReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        if not av.checkQuestRewardFlag(PiratesGlobals.QRFlagMainStory):
            av.assignQuestRewardFlag(PiratesGlobals.QRFlagMainStory)
            trade.giveStackableTypeLimit(InventoryType.SailPowerRecharge, 2)
            trade.giveStack(InventoryType.SailPowerRecharge, 2)

    def getDescriptionText(self):
        return PLocalizer.Chapter3RewardDesc


class ReputationReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        global REPFACTOR_HOLIDAY
        avId = av.getDoId()
        rewardAmount = self.amount
        if Freebooter.getPaidStatusAI(avId):
            rewardAmount = (REWARD_TO == 2 or REWARD_TO == 3) and self.amount * REPFACTOR_HOLIDAY
        else:
            if not Freebooter.getPaidStatusAI(avId) and (REWARD_TO == 1 or REWARD_TO == 3):
                rewardAmount = self.amount * REPFACTOR_HOLIDAY
        if av.getTempDoubleXPReward():
            rewardAmount = rewardAmount * 2
        trade.giveReputation(InventoryType.GeneralRep, rewardAmount)
        trade.giveReputation(InventoryType.OverallRep, rewardAmount)

    def getDescriptionText(self):
        rewardAmount = self.amount * REPFACTOR_HOLIDAY
        return PLocalizer.ReputationRewardDesc % rewardAmount

    def setReputationFactor(self, multiplier):
        global REPFACTOR_HOLIDAY
        REPFACTOR_HOLIDAY = multiplier


class SpecialQuestReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        av.acceptSpecialQuestReward(self.questId, trade)

    def getDescriptionText(self):
        return PLocalizer.SpecialQuestRewardDesc


class JewelryQuestReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        gender = av.dna.getGender()
        questDrop = JewelryGlobals.questDrops.get(self.amount)
        if questDrop is None:
            return
        if gender == 'm':
            uid = questDrop[0]
        else:
            uid = questDrop[1]
        trade.giveAccessory(InventoryType.ItemTypeJewelry, uid)
        trade.setSuccessCallback(av.giveJewelryMessage, extraArgs=[uid])
        trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeJewelry])
        return

    def getDescriptionText(self):
        return PLocalizer.JewelryQuestRewardDesc

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeJewelry) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeJewelry)
                return False
            return True
        return False


class TattooQuestReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        doId = av.getDoId()
        questDrop = TattooGlobals.questDrops.get(self.amount)
        tattooUIDs = []
        for drop in questDrop:
            trade.giveAccessory(InventoryType.ItemTypeTattoo, drop)
            tattooUIDs.append(drop)

        if tattooUIDs:
            trade.setSuccessCallback(av.giveTattooMessages, extraArgs=[tattooUIDs])
            trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeTattoo])

    def getDescriptionText(self):
        return PLocalizer.TattooQuestRewardDesc

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeTattoo) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeTattoo)
                return False
            return True
        return False


class ClothingQuestReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        doId = av.getDoId()
        gender = av.dna.getGender()
        questDrop = ClothingGlobals.questDrops.get(self.amount)
        if questDrop is None:
            return
        dropForGender = questDrop.get(gender)
        if dropForGender is None:
            return
        dropId = dropForGender[0]
        colorId = dropForGender[1]
        trade.giveClothing(dropId, colorId)
        trade.setSuccessCallback(av.giveClothingMessage, extraArgs=[dropId, colorId])
        trade.setFailureCallback(av.giveFreeInventoryMessage, extraArgs=[InventoryType.ItemTypeClothing])
        return

    def getDescriptionText(self):
        questDrop = ClothingGlobals.questDrops.get(self.amount)
        gender = 'm'
        if hasattr(localAvatar, 'style'):
            gender = localAvatar.style.getGender()
        dropForGender = questDrop.get(gender)[0]
        itemName = PLocalizer.ItemNames.get(dropForGender)
        return itemName

    def canGive(self, av):
        inv = av.getInventory()
        if inv:
            if inv.findAvailableLocation(InventoryType.ItemTypeClothing) == Locations.INVALID_LOCATION:
                av.giveFreeInventoryMessage(InventoryType.ItemTypeClothing)
                return False
            return True
        return False


class TempDoubleRepReward(QuestReward):
    __module__ = __name__

    def applyTo(self, trade, av):
        av.updateTempDoubleXPReward(self.amount)

    def getDescriptionText(self):
        return PLocalizer.Temp2xRepQuestRewardDesc


DBId2Class = {0: GoldReward, 1: MaxHpReward, 2: MaxMojoReward, 3: LuckReward, 4: SwiftnessReward, 5: TreasureMapReward, 6: CollectReward, 7: ShipReward, 8: ReputationReward, 9: PistolReward, 10: SpecialQuestReward, 11: DollReward, 12: DaggerReward, 13: PlayingCardReward, 14: GrenadeReward, 15: StaffReward, 16: TeleportTotemReward, 17: PlayingCardTier0Reward, 18: PlayingCardTier1Reward, 19: PlayingCardTier2Reward, 20: PlayingCardTier3Reward, 21: CubaTeleportReward, 22: PortRoyalTeleportReward, 23: PadresDelFuegoTeleportReward, 24: KingsHeadTeleportReward, 25: GoldAmountReward, 26: MainStoryReward, 27: JewelryQuestReward, 28: TattooQuestReward, 29: ClothingQuestReward, 30: PistolUpgradeReward, 31: DaggerUpgradeReward, 32: CutlassUpgradeReward, 33: DollUpgradeReward, 34: WandUpgradeReward, 35: TempDoubleRepReward, 36: CharmReward, 37: RavensCoveTeleportReward, 38: CutlassItemReward, 39: DaggerItemReward, 40: GunItemReward, 41: DollItemReward, 42: GrenadeItemReward, 43: StaffItemReward}
Class2DBId = invertDict(DBId2Class)
# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
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
#                                                 37  LOAD_GLOBAL           8  'REWARD_TO'
#                                  1. expr
#                                                 40  LOAD_CONST            1  2
#                                  2.             43  COMPARE_OP            2  '=='
#                      1. jmp_true (2)
#                          0.             46  JUMP_IF_TRUE         13  'to 62'
#                          1.             49  POP_TOP          
#                      2. expr
#                         compare
#                             compare_single (3)
#                                  0. expr
#                                                 50  LOAD_GLOBAL           8  'REWARD_TO'
#                                  1. expr
#                                                 53  LOAD_CONST            2  3
#                                  2.             56  COMPARE_OP            2  '=='
#                      3.           59_0  COME_FROM            46  '46'
#              1. jmp_false (2)
#                  0.             59  JUMP_IF_FALSE        14  'to 76'
#                  1.             62  POP_TOP          
#              2. expr
#                 L. 134      63  LOAD_FAST             4  'goldAmt'
#              3. come_from_opt
#      1. expr
#                     66  LOAD_GLOBAL           9  'GOLDFACTOR_HOLIDAY'
#      2. inplace_op
#                     69  INPLACE_MULTIPLY 
#      3. store
#                     70  STORE_FAST            4  'goldAmt'
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
#                                                 52  LOAD_GLOBAL          11  'REWARD_TO'
#                                  1. expr
#                                                 55  LOAD_CONST            2  2
#                                  2.             58  COMPARE_OP            2  '=='
#                      1. jmp_true (2)
#                          0.             61  JUMP_IF_TRUE         13  'to 77'
#                          1.             64  POP_TOP          
#                      2. expr
#                         compare
#                             compare_single (3)
#                                  0. expr
#                                                 65  LOAD_GLOBAL          11  'REWARD_TO'
#                                  1. expr
#                                                 68  LOAD_CONST            3  3
#                                  2.             71  COMPARE_OP            2  '=='
#                      3.           74_0  COME_FROM            61  '61'
#              1. jmp_false (2)
#                  0.             74  JUMP_IF_FALSE        14  'to 91'
#                  1.             77  POP_TOP          
#              2. expr
#                 L. 164      78  LOAD_FAST             4  'goldAmt'
#              3. come_from_opt
#      1. expr
#                     81  LOAD_GLOBAL          12  'GOLDFACTOR_HOLIDAY'
#      2. inplace_op
#                     84  INPLACE_MULTIPLY 
#      3. store
#                     85  STORE_FAST            4  'goldAmt'