# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.teleport.DoorTeleportActorOV
from pirates.piratesbase import PiratesGlobals
from pirates.teleport.AreaTeleportActorOV import AreaTeleportActorOV

class DoorTeleportActorOV(AreaTeleportActorOV):
    __module__ = __name__

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name='DoorTeleportActorOV'):
        AreaTeleportActorOV.__init__(self, cr, name)

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterCompleteShow(self, *args):
        base.cr.loadingScreen.show()
        self.b_requestFSMState(None, 'ShowComplete')
        return