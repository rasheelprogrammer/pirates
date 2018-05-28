# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.tutorial.PiratesTutorialManager
from direct.distributed import DistributedObject

class PiratesTutorialManager(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = directNotify.newCategory('PiratesTutorialManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)

    def disable(self):
        self.ignoreAll()
        DistributedObject.DistributedObject.disable(self)

    def enterTutorial(self, tutorialZone):
        messenger.send('startTutorial', [self.doId, tutorialZone])