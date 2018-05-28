# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.web.SettingsMgr
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.web.SettingsMgrBase import SettingsMgrBase

class SettingsMgr(DistributedObjectGlobal, SettingsMgrBase):
    __module__ = __name__
    notify = directNotify.newCategory('SettingsMgr')

    def announceGenerate(self):
        DistributedObjectGlobal.announceGenerate(self)
        SettingsMgrBase.announceGenerate(self)
        if not self.cr.isLive():
            self._sracs = None
            if self.cr.isConnected():
                self._scheduleChangedSettingRequest()
            self._crConnectEvent = self.cr.getConnectedEvent()
            self.accept(self._crConnectEvent, self._handleConnected)
        return

    def _handleConnected(self):
        self._scheduleChangedSettingRequest()

    def _scheduleChangedSettingRequest(self):
        if self._sracs:
            self._sracs.destroy()
        self._sracs = FrameDelayedCall('requestAllChangedSettings', self.sendRequestAllChangedSettings)

    def delete(self):
        self.ignore(self._crConnectEvent)
        if self._sracs:
            self._sracs.destroy()
        SettingsMgrBase.delete(self)
        DistributedObjectGlobal.delete(self)

    def sendRequestAllChangedSettings(self):
        self.sendUpdate('requestAllChangedSettings', [])

    def settingChange(self, settingName, valueStr):
        if valueStr == self._getCurrentValueRepr(settingName):
            return
        self.notify.info('got setting change: %s -> %s' % (settingName, valueStr))
        self._changeSetting(settingName, valueStr)