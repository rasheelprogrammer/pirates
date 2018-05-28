# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.holiday.DistributedHolidayObject
from pandac.PandaModules import NodePath
from pirates.distributed.DistributedInteractive import DistributedInteractive

class DistributedHolidayObject(DistributedInteractive):
    __module__ = __name__

    def __init__(self, cr, proximityText):
        NodePath.__init__(self, self.__class__.__name__)
        DistributedInteractive.__init__(self, cr)
        self.holiday = ''
        self.interactRadius = 10
        self.interactMode = 0
        self.proximityText = proximityText

    def announceGenerate(self):
        DistributedInteractive.announceGenerate(self)

    def setHoliday(self, holiday):
        self.holiday = holiday

    def setInteractRadius(self, radius):
        self.interactRadius = radius
        self.diskRadius = radius * 2.0

    def setInteractMode(self, mode):
        if mode == 1 or mode == 2 and localAvatar.isGM():
            self.setInteractOptions(proximityText=self.proximityText, sphereScale=self.interactRadius, diskRadius=self.diskRadius)
        else:
            self.setInteractOptions(allowInteract=False)