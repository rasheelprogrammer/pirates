# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.distributed.ObjectServer
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject

class ObjectServer(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('ObjectServer')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def setName(self, name):
        self.name = name