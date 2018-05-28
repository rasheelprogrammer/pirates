# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.NPCManager
from direct.showbase import DirectObject

class NPCManager(DirectObject.DirectObject):
    __module__ = __name__

    def __int__(self):
        self.clearNpcData()

    def clearNpcData(self):
        self.npcData = {}

    def addNpcData(self, data):
        for currKey in data.keys():
            self.npcData.setdefault(currKey, {}).update(data[currKey])

    def getNpcData(self, uid):
        return self.npcData.get(uid, {})