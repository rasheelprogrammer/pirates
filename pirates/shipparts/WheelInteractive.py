# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.shipparts.WheelInteractive
from pirates.interact.SimpleInteractive import SimpleInteractive
from pirates.piratesbase import PLocalizer

class WheelInteractive(SimpleInteractive):
    __module__ = __name__

    def __init__(self, ship):
        self.ship = ship
        wheel = ship.model.locators.find('**/location_wheel')
        if not wheel:
            wheel = ship.model.root.attachNewNode('dummyWheel')
        SimpleInteractive.__init__(self, wheel, 'wheel-%s' % ship.doId, PLocalizer.InteractWheel)

    def interactionAllowed(self, avId):
        return self.ship.canTakeWheel(avId)

    def requestInteraction(self, avId):
        self.ship.requestPilot(avId)