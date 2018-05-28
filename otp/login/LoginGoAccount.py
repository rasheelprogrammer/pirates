# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.LoginGoAccount
from pandac.PandaModules import *
from direct.distributed.MsgTypes import *
from direct.directnotify import DirectNotifyGlobal
import LoginBase
from direct.distributed.PyDatagram import PyDatagram

class LoginGoAccount(LoginBase.LoginBase):
    __module__ = __name__

    def __init__(self, cr):
        LoginBase.LoginBase.__init__(self, cr)

    def createAccount(self, loginName, password, data):
        return 'Unsupported'

    def authorize(self, loginName, password):
        self.loginName = loginName
        self.password = password
        return

    def supportsRelogin(self):
        return 0

    def sendLoginMsg(self):
        cr = self.cr
        datagram = PyDatagram()
        datagram.addUint16(CLIENT_LOGIN_2)
        datagram.addString(self.password)
        datagram.addString(cr.serverVersion)
        datagram.addUint32(cr.hashVal)
        self.__addTokenType(datagram)
        datagram.addString(cr.validateDownload)
        datagram.addString(cr.wantMagicWords)
        cr.send(datagram)

    def resendPlayToken(self):
        pass

    def requestPwdReminder(self, email=None, acctName=None):
        return 0

    def getAccountData(self, loginName, password):
        return 'Unsupported'

    def supportsParentPassword(self):
        return 0

    def authenticateParentPassword(self, loginName, password, parentPassword):
        return (0, None)

    def supportsAuthenticateDelete(self):
        return 0

    def enableSecretFriends(self, loginName, password, parentPassword, enable=1):
        return (0, None)

    def __addTokenType(self, datagram):
        datagram.addInt32(CLIENT_LOGIN_2_BLUE)