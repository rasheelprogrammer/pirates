# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.leveleditor.LevelEntity
from pandac.PandaModules import *

class LevelEntity(NodePath):
    __module__ = __name__

    def __init__(self):
        NodePath.NodePath.__init__(self, 'LevelEntity')

    def setProperty(self, propertyName, propertyValue):
        if propertyName == 'None':
            pass

    def cleanUp(self):
        pass