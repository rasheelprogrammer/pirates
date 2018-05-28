# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.Distributed7StudTable
from pirates.minigame import PlayingCardGlobals
from pirates.minigame import DistributedPokerTable
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import Point3, Vec3
from pirates.piratesbase import PLocalizer

class Distributed7StudTable(DistributedPokerTable.DistributedPokerTable):
    __module__ = __name__

    def __init__(self, cr):
        DistributedPokerTable.DistributedPokerTable.__init__(self, cr, '7stud', numRounds=6)
        self.maxCommunityCards = 0
        self.maxHandCards = 7
        self.gameType = 1

    def getGameType(self):
        return PlayingCardGlobals.SevenStud

    def getInteractText(self):
        return PLocalizer.InteractTable7StudPoker

    def getSitDownText(self):
        return PLocalizer.PokerSitDown7StudPoker

    def dealerAnim(self, round):
        deals = Sequence()
        if round == 0:
            if self.isLocalAvatarSeated():
                self.gui.disableAction()
                self.gui.clearTable()
            for card in self.PocketCards:
                card.hide()

        if round == 1:
            deals.append(self.dealPlayerCards(numCards=3))
        if round in [2, 3, 4, 5]:
            deals.append(self.dealPlayerCards(numCards=1))
        return deals

    def checkForVisiblePair(self):
        return self.sevenStudCheckForVisiblePair(self.playerHands)