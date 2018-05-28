# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.teleport.TeleportGlobals
from pirates.teleport.DistributedFSMBase import DistributedFSMErrors

class TeleportErrors(DistributedFSMErrors):
    __module__ = __name__
    Undefined = DistributedFSMErrors.Undefined
    Timeout = Undefined
    Undefined += 1
    Disconnect = Undefined
    Undefined += 1
    Aborted = Undefined
    Undefined += 1
    Interrupted = Undefined
    Undefined += 1