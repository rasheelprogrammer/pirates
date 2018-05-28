# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestPrereq
from direct.showbase.PythonUtil import POD, makeTuple
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals

class QuestPrereq(POD):
    __module__ = __name__

    def avIsReady(self, av):
        return True

    def avIsReadyAI(self, av):
        return self.avIsReady(av)

    def giverCanGive(self, giver):
        return True


class HpAtLeast(QuestPrereq):
    __module__ = __name__
    DataSet = {'minHp': None}

    def __init__(self, minHp):
        QuestPrereq.__init__(self, minHp=minHp)

    def avIsReady(self, av):
        return av.getMaxHp() >= self.minHp


class SwiftnessAtLeast(QuestPrereq):
    __module__ = __name__
    DataSet = {'minSwiftness': None}

    def __init__(self, minSwiftness):
        QuestPrereq.__init__(self, minSwiftness=minSwiftness)

    def avIsReady(self, av):
        return av.getMaxSwiftness() >= self.minSwiftness


class LuckAtLeast(QuestPrereq):
    __module__ = __name__
    DataSet = {'minLuck': None}

    def __init__(self, minLuck):
        QuestPrereq.__init__(self, minLuck=minLuck)

    def avIsReady(self, av):
        return av.getMaxLuck() >= self.minLuck


class MojoAtLeast(QuestPrereq):
    __module__ = __name__
    DataSet = {'minMojo': None}

    def __init__(self, minMojo):
        QuestPrereq.__init__(self, minMojo=minMojo)

    def avIsReady(self, av):
        return av.getMaxMojo() >= self.minMojo


class DidQuest(QuestPrereq):
    __module__ = __name__
    DataSet = {'questIds': None}

    def __init__(self, questIds):
        QuestPrereq.__init__(self, questIds=questIds)

    def setQuestIds(self, questIds):
        self.questIds = makeTuple(questIds)

    def avIsReady(self, av):
        from pirates.quest import QuestLadderDB
        questHistory = av.getQuestLadderHistory()
        for questId in self.questIds:
            container = QuestLadderDB.getContainer(questId)
            questInts = QuestLadderDB.getAllParentQuestInts(container)
            thisQuestInHistory = False
            for qInt in questInts:
                if qInt in questHistory:
                    thisQuestInHistory = True
                    break

            if not thisQuestInHistory:
                return False

        return True

    def giverCanGive(self, avId):
        return False


class GetFrom(QuestPrereq):
    __module__ = __name__
    DataSet = {'questGivers': None}

    def __init__(self, questGivers):
        QuestPrereq.__init__(self, questGivers=questGivers)

    def setQuestGivers(self, questGivers):
        self.questGivers = makeTuple(questGivers)

    def giverCanGive(self, giver):
        return giver in self.questGivers


class HasQuest(QuestPrereq):
    __module__ = __name__
    DataSet = {'questIds': None}

    def __init__(self, questIds):
        QuestPrereq.__init__(self, questIds=questIds)

    def setQuestIds(self, questIds):
        self.questIds = makeTuple(questIds)

    def avIsReady(self, av):
        quests = []
        for q in av.getQuests():
            quests.append(q.getQuestId())

        for questId in self.questIds:
            if questId not in quests:
                return False

        return True


class NotCompleted(QuestPrereq):
    __module__ = __name__
    DataSet = {'questIds': None}

    def __init__(self, questIds):
        QuestPrereq.__init__(self, questIds=questIds)

    def setQuestIds(self, questIds):
        self.questIds = makeTuple(questIds)

    def avIsReady(self, av):
        from pirates.quest import QuestLadderDB
        questHistory = av.getQuestLadderHistory()
        for questId in self.questIds:
            container = QuestLadderDB.getContainer(questId)
            questInts = QuestLadderDB.getAllParentQuestInts(container)
            thisQuestInHistory = False
            for qInt in questInts:
                if qInt in questHistory:
                    thisQuestInHistory = True
                    break

            if thisQuestInHistory:
                return False
            currentQuests = av.getQuests()
            for quest in currentQuests:
                if questId == quest.getQuestId() or container.hasQuest(quest.getQuestId()):
                    return False

        return True


class WithinTimeOfDay(QuestPrereq):
    __module__ = __name__
    DataSet = {'timeFrom': 0, 'timeTo': 0}

    def __init__(self, timeFrom, timeTo):
        QuestPrereq.__init__(self, timeFrom=timeFrom, timeTo=timeTo)
        self.timeFrom2 = None
        self.timeTo2 = None
        return

    def avIsReady(self, av):
        currTime = base.cr.timeOfDayManager.getCurrentIngameTime()
        if self.timeFrom > self.timeTo:
            self.timeTo2 = 25
            self.timeFrom2 = 0
            return currTime >= self.timeFrom and currTime < self.timeTo2 or currTime >= self.timeFrom2 and currTime < self.timeTo
        else:
            return currTime >= self.timeFrom and currTime < self.timeTo

    def avIsReadyAI(self, av):
        currTime = simbase.air.timeOfDayManager.getCurrentIngameTime()
        if self.timeFrom > self.timeTo:
            self.timeTo2 = 25
            self.timeFrom2 = 0
            return currTime >= self.timeFrom and currTime < self.timeTo2 or currTime >= self.timeFrom2 and currTime < self.timeTo
        else:
            return currTime >= self.timeFrom and currTime < self.timeTo


class RequiresItemEquipped(QuestPrereq):
    __module__ = __name__
    DataSet = {'itemId': None}

    def __init__(self, itemId):
        QuestPrereq.__init__(self, itemId=itemId)

    def avIsReady(self, av):
        from pirates.inventory.InventoryGlobals import Locations
        inv = av.getInventory()
        if not inv:
            return False
        categoryId = ItemGlobals.getClass(self.itemId)
        if inv.getItemQuantity(categoryId, self.itemId) > 0:
            if categoryId == InventoryType.ItemTypeWeapon:
                if av.currentWeaponId == itemId:
                    return True
                else:
                    return False
            else:
                if categoryId == InventoryType.ItemTypeCharm:
                    if av.getCurrentCharm() == self.itemId:
                        return True
                    else:
                        return False
                else:
                    if categoryId == InventoryType.ItemTypeClothing:
                        locationRange = Locations.RANGE_EQUIP_CLOTHES
                    else:
                        if categoryId == InventoryType.ItemTypeJewelry:
                            locationRange = Locations.RANGE_EQUIP_JEWELRY
                        else:
                            if categoryId == InventoryType.ItemTypeTattoo:
                                locationRange = Locations.RANGE_EQUIP_TATTOO
                            else:
                                locationRange = (0, 0)
            for location in range(locationRange[0], locationRange[1] + 1):
                locatable = inv.getLocatables().get(location)
                if locatable:
                    return locatable[1] == self.itemId and True

        return False


class RequiresItemUnequipped(QuestPrereq):
    __module__ = __name__
    DataSet = {'itemId': None}

    def __init__(self, itemId):
        QuestPrereq.__init__(self, itemId=itemId)

    def avIsReady(self, av):
        from pirates.inventory.InventoryGlobals import Locations
        inv = av.getInventory()
        if not inv:
            return False
        categoryId = ItemGlobals.getClass(self.itemId)
        if inv.getItemQuantity(categoryId, self.itemId) > 0:
            if categoryId == InventoryType.ItemTypeWeapon:
                if av.currentWeaponId == self.itemId:
                    return False
                else:
                    return True
            else:
                if categoryId == InventoryType.ItemTypeCharm:
                    if av.getCurrentCharm() == self.itemId:
                        return False
                    else:
                        return True
                else:
                    if categoryId == InventoryType.ItemTypeClothing:
                        locationRange = Locations.RANGE_EQUIP_CLOTHES
                    else:
                        if categoryId == InventoryType.ItemTypeJewelry:
                            locationRange = Locations.RANGE_EQUIP_JEWELRY
                        else:
                            if categoryId == InventoryType.ItemTypeTattoo:
                                locationRange = Locations.RANGE_EQUIP_TATTOO
                            else:
                                locationRange = (0, 0)
            equippedItem = False
            for location in range(locationRange[0], locationRange[1] + 1):
                locatable = inv.getLocatables().get(location)
                if locatable:
                    equippedItem = locatable[1] == self.itemId and True

            if not equippedItem:
                return True
            return False
        return True


class RequiresItem(QuestPrereq):
    __module__ = __name__
    DataSet = {'itemId': None}

    def __init__(self, itemId):
        QuestPrereq.__init__(self, itemId=itemId)

    def avIsReady(self, av):
        inv = av.getInventory()
        if not inv:
            return False
        categoryId = ItemGlobals.getClass(self.itemId)
        if inv.getItemQuantity(categoryId, self.itemId) > 0:
            return True
        else:
            return False


class IsGender(QuestPrereq):
    __module__ = __name__
    DataSet = {'gender': 'm'}

    def __init__(self, gender):
        QuestPrereq.__init__(self, gender=gender)

    def avIsReady(self, av):
        return av.style.getGender() == self.gender

    def avIsReadyAI(self, av):
        return av.dna.getGender() == self.gender


class IsHoliday(QuestPrereq):
    __module__ = __name__
    DataSet = {'holidayId': None}

    def __init__(self, holidayId):
        QuestPrereq.__init__(self, holidayId=holidayId)

    def avIsReady(self, av):
        return base.cr.newsManager and self.holidayId in base.cr.newsManager.getHolidayIdList()

    def avIsReadyAI(self, av):
        return simbase.air.holidayManager.isHolidayActive(self.holidayId)