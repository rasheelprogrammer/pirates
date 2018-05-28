# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.speedchat.SCSettings
from SCColorScheme import SCColorScheme
from otp.otpbase import OTPLocalizer

class SCSettings:
    __module__ = __name__

    def __init__(self, eventPrefix, whisperMode=0, colorScheme=None, submenuOverlap=OTPLocalizer.SCOsubmenuOverlap, topLevelOverlap=None):
        self.eventPrefix = eventPrefix
        self.whisperMode = whisperMode
        if colorScheme is None:
            colorScheme = SCColorScheme()
        self.colorScheme = colorScheme
        self.submenuOverlap = submenuOverlap
        self.topLevelOverlap = topLevelOverlap
        return