# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.seapatch.LerpSeaPatchInterval
from libpirates import CLerpSeaPatchInterval

class LerpSeaPatchInterval(CLerpSeaPatchInterval):
    __module__ = __name__
    lerpNum = 1

    def __init__(self, name, duration, blendType, patch, initial, target):
        if name == None:
            name = 'LerpSeaPatchInterval-%d' % self.lerpNum
            LerpSeaPatchInterval.lerpNum += 1
        blendType = self.stringBlendType(blendType)
        if target == None:
            target = SeaPatchRoot()
        CLerpSeaPatchInterval.__init__(self, name, duration, blendType, patch, initial, target)
        return