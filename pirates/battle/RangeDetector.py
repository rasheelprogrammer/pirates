# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.battle.RangeDetector
from pandac.PandaModules import *
from pirates.battle import WeaponGlobals

class RangeDetector(NodePath):
    __module__ = __name__

    def __init__(self):
        NodePath.__init__(self, 'rangeDetector')
        self.spheres = []
        for radius in WeaponGlobals.Ranges:
            sphere = CollisionSphere(0, 0, 0, 1.0)
            sphere.setTangible(0)
            sphereNode = CollisionNode('rangeDetector-%s' % radius)
            sphereNode.addSolid(sphere)
            sphereNodePath = self.attachNewNode(sphereNode)
            self.spheres.append(sphereNodePath)