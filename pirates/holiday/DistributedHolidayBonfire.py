# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.holiday.DistributedHolidayBonfire
from pirates.holiday.DistributedHolidayObject import DistributedHolidayObject
from pirates.piratesbase import PLocalizer
from pirates.effects.FeastFire import FeastFire
from pirates.ai import HolidayGlobals

class DistributedHolidayBonfire(DistributedHolidayObject):
    __module__ = __name__

    def __init__(self, cr):
        holiday = None
        proximityText = ''
        if base.cr.newsManager.getHoliday(HolidayGlobals.FOUNDERSFEAST):
            holiday = HolidayGlobals.FOUNDERSFEAST
        else:
            if base.cr.newsManager.getHoliday(HolidayGlobals.MARDIGRAS):
                holiday = HolidayGlobals.MARDIGRAS
        holidayMsgs = PLocalizer.holidayMessages.get(holiday)
        if holidayMsgs:
            proximityText = holidayMsgs.get(HolidayGlobals.MSG_PIG)
        DistributedHolidayObject.__init__(self, cr, proximityText=proximityText)
        self.fireStarted = False
        return

    def setFireStarted(self, value=False):
        self.fireStarted = value

    def getFireStarted(self):
        return self.fireStarted

    def acceptInteraction(self):
        DistributedHolidayObject.acceptInteraction(self)
        localAvatar.b_setGameState('BeginFeast')

    def rejectInteraction(self):
        DistributedHolidayObject.rejectInteraction(self)
        holiday = None
        if base.cr.newsManager.getHoliday(HolidayGlobals.FOUNDERSFEAST):
            holiday = HolidayGlobals.FOUNDERSFEAST
        else:
            if base.cr.newsManager.getHoliday(HolidayGlobals.MARDIGRAS):
                holiday = HolidayGlobals.MARDIGRAS
        holidayMsgs = PLocalizer.holidayMessages.get(holiday)
        if holidayMsgs:
            localAvatar.guiMgr.createWarning(holidayMsgs.get(HolidayGlobals.MSG_BONFIRE_STARTED))
        return

    def finishInteraction(self):
        localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)