# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.LoginDISLTokenAccount
from direct.showbase.ShowBaseGlobal import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginBase
from direct.distributed.PyDatagram import PyDatagram

class LoginDISLTokenAccount(LoginBase.LoginBase):
    __module__ = __name__

    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def supportsRelogin(self):
        return 0

    def authorize(self, loginName, password):
        self.loginName = loginName
        self.DISLToken = password

    def sendLoginMsg(self):
        cr = self.cr
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_LOGIN_3)
        datagram.addString(self.DISLToken)
        datagram.addString(cr.serverVersion)
        datagram.addUint32(cr.hashVal)
        datagram.addInt32(CLIENT_LOGIN_3_DISL_TOKEN)
        datagram.addString(cr.validateDownload)
        datagram.addString(cr.wantMagicWords)
        cr.send(datagram)

    def supportsParentPassword(self):
        return 0

    def supportsAuthenticateDelete(self):
        return 0