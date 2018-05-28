# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.DistributedRepairGameBase
from direct.distributed.GridChild import GridChild
from RepairBracingGame import RepairBracingGame
from RepairCareeningGame import RepairCareeningGame
from RepairHammeringGame import RepairHammeringGame
from RepairPitchingGame import RepairPitchingGame
from RepairPumpingGame import RepairPumpingGame
from RepairSawingGame import RepairSawingGame
GAME_OPEN = -1
GAME_IN_USE = 0
GAME_COMPLETE = 100
AT_SEA = 0
ON_LAND = 1
DIFFICULTY_MAX = 9
GAME_ORDER = (
 (
  RepairPumpingGame, RepairSawingGame, RepairBracingGame, RepairHammeringGame, RepairPitchingGame), (RepairCareeningGame, RepairSawingGame, RepairBracingGame, RepairHammeringGame, RepairPitchingGame))

class DistributedRepairGameBase(GridChild):
    __module__ = __name__

    def __init__(self, location=0):
        GridChild.__init__(self)
        self.location = location

    def getGameCount(self):
        return len(GAME_ORDER[self.location])