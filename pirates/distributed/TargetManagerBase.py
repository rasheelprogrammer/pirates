# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.distributed.TargetManagerBase


class TargetManagerBase:
    __module__ = __name__

    def __init__(self):
        self.objectDict = {}

    def delete(self):
        del self.objectDict

    def getUniqueId(self, obj):
        return obj.id()

    def addTarget(self, nodePathId, obj):
        self.objectDict[nodePathId] = obj

    def removeTarget(self, nodePathId):
        if self.objectDict.has_key(nodePathId):
            del self.objectDict[nodePathId]

    def getObjectFromNodepath(self, nodePath):
        target = nodePath.getNetPythonTag('MonstrousObject')
        if not target:
            target = self.objectDict.get(nodePath.id(), None)
        return target