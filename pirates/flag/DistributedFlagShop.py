# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.flag.DistributedFlagShop
from pandac.PandaModules import *
from direct.distributed.DistributedObject import DistributedObject
import FlagGlobals
from Flag import Flag

class DistributedFlagShop(DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedFlagShop')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)