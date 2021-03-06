# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.ai.GarbageLeakServerEventAggregator
from direct.showbase.DirectObject import DirectObject
from direct.showbase import GarbageReport

class GarbageLeakServerEventAggregator(DirectObject):
    __module__ = __name__

    def __init__(self, cr):
        self.cr = cr
        self._doLaterName = None
        self._sentLeakDesc2num = {}
        self._curLeakDesc2num = {}
        self.accept(GarbageReport.GarbageCycleCountAnnounceEvent, self._handleCycleCounts)
        return

    def destroy(self):
        self._stopSending()
        self.ignoreAll()
        del self.cr

    def _handleCycleCounts(self, desc2num):
        self._curLeakDesc2num = desc2num
        self._startSending()

    def _startSending(self):
        if not self._doLaterName:
            self._sendLeaks()
            self._doLaterName = uniqueName('%s-sendGarbageLeakInfo' % self.__class__.__name__)
            self.doMethodLater(60 * 60.0, self._sendLeaks, self._doLaterName)

    def _stopSending(self):
        if self._doLaterName:
            self.removeTask(self._doLaterName)
        self._doLaterName = None
        return

    def _sendLeaks(self, task=None):
        for desc, curNum in self._curLeakDesc2num.iteritems():
            self._sentLeakDesc2num.setdefault(desc, 0)
            num = curNum - self._sentLeakDesc2num[desc]
            if num > 0:
                self.cr.timeManager.d_setClientGarbageLeak(num, desc)
                self._sentLeakDesc2num[desc] = curNum

        if task:
            return task.again