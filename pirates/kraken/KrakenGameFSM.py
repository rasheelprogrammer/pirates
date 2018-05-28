# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.kraken.KrakenGameFSM
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

class bp:
    __module__ = __name__
    kraken = bpdb.bpPreset(cfg='krakenfsm', static=1)
    krakenCall = bpdb.bpPreset(cfg='krakenfsm', call=1, static=1)


class KrakenGameFSM(FSM):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenGameFSM')

    def __init__(self, av):
        FSM.__init__(self, 'KrakenGameFSM')
        self.av = av

    @bp.krakenCall()
    def enterRam(self):
        pass

    @bp.krakenCall()
    def exitRam(self):
        pass

    @bp.krakenCall()
    def enterGrab(self):
        self.av.emergeInterval.pause()
        self.av.submergeInterval.start()

    @bp.krakenCall()
    def exitGrab(self):
        pass