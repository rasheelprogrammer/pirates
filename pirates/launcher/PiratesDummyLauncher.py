# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.launcher.PiratesDummyLauncher
from otp.launcher.DummyLauncherBase import DummyLauncherBase
from pirates.launcher.PiratesQuickLauncher import PiratesQuickLauncher

class PiratesDummyLauncher(DummyLauncherBase, PiratesQuickLauncher):
    __module__ = __name__

    def __init__(self):
        DummyLauncherBase.__init__(self)
        self.setPhaseComplete(1, 100)
        self.setPhaseComplete(2, 100)
        self.firstPhase = 3
        self.startFakeDownload()