# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.teleport.DistributedFSM
from direct.distributed.DistributedObject import DistributedObject
from pirates.teleport.DistributedFSMBase import DistributedFSMBase

class DistributedFSM(DistributedObject, DistributedFSMBase):
    __module__ = __name__

    def __init__(self, cr, name):
        DistributedFSMBase.__init__(self, name)
        DistributedObject.__init__(self, cr)

    @report(types=['args'], dConfigParam=['dteleport'])
    def setFSMState(self, stateContext, stateData):
        stateData = stateData[0]
        state = stateData[0]
        args = stateData[1:]
        result = self.request(state, *args)