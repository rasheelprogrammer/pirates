# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.holiday.KrakenHolidayGlobals
from pirates.ai.HolidayDates import *

class Msgs:
    __module__ = __name__
    Launch = 50
    Escaped = 51
    Defeated = 52


class ConfigIds:
    __module__ = __name__
    Test_Maw = 89
    Test_Crush = 92
    Test_Grab = 94
    Test_DDG = 99


KrakenHolidayConfigs = {ConfigIds.Test_Maw: {'id': ConfigIds.Test_Maw, 'name': 'Kraken (Maw Test)', 'launchMsg': Msgs.Launch, 'escapedMsg': Msgs.Escaped, 'defeatedMsg': Msgs.Defeated}, ConfigIds.Test_Crush: {'id': ConfigIds.Test_Crush, 'name': 'Kraken (Crush Test)', 'launchMsg': Msgs.Launch, 'escapedMsg': Msgs.Escaped, 'defeatedMsg': Msgs.Defeated}, ConfigIds.Test_Grab: {'id': ConfigIds.Test_Grab, 'name': 'Kraken (Grab Test)', 'launchMsg': Msgs.Launch, 'escapedMsg': Msgs.Escaped, 'defeatedMsg': Msgs.Defeated}, ConfigIds.Test_DDG: {'id': ConfigIds.Test_DDG, 'name': 'Kraken (Duck Duck Goose Test)', 'launchMsg': Msgs.Launch, 'escapedMsg': Msgs.Escaped, 'defeatedMsg': Msgs.Defeated}}