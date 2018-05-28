# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.holiday.MessageHolidayGlobals
from pirates.ai.HolidayDates import *

class ConfigIds:
    __module__ = __name__
    CrewDays = 1


MessageHolidayConfigs = {ConfigIds.CrewDays: {'id': ConfigIds.CrewDays, 'name': 'CrewDays (Msg)', 'dates': HolidayDates(HolidayDates.TYPE_WEEKLY, [
                                (
                                 Day.FRIDAY, 15, 0, 0), (Day.FRIDAY, 20, 0, 0), (Day.SATURDAY, 15, 0, 0), (Day.SATURDAY, 20, 0, 0)])}}