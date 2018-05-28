# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.MinigameFSM
from direct.fsm import FSM

class MinigameFSM(FSM.FSM):
    __module__ = __name__

    def __init__(self, gameFSM):
        self.gameFSM = gameFSM
        FSM.FSM.__init__(self, 'MinigameFSM')
        self.defaultTransitions = {'Init': ['Intro', 'Idle', 'Final'], 'Idle': ['Intro', 'Idle', 'Final'], 'Intro': ['MainGame', 'Idle', 'Final'], 'MainGame': ['Outro', 'Idle', 'Final'], 'Outro': ['Reward', 'Idle', 'Final'], 'Reward': ['Idle', 'Final'], 'Final': []}

    def destroy(self):
        del self.gameFSM

    def enterInit(self):
        print 'minigameFSM init'

    def exitInit(self):
        pass

    def enterIntro(self):
        pass

    def exitIntro(self):
        pass

    def enterIdle(self):
        pass

    def exitIdle(self):
        pass

    def enterMainGame(self):
        pass

    def exitMainGame(self):
        pass

    def enterOutro(self):
        pass

    def exitOutro(self):
        pass

    def enterReward(self):
        pass

    def exitReward(self):
        pass

    def enterFinal(self):
        pass

    def exitFinal(self):
        pass