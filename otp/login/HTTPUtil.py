# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.HTTPUtil
from pandac.PandaModules import *

class HTTPUtilException(Exception):
    __module__ = __name__

    def __init__(self, what):
        Exception.__init__(self, what)


class ConnectionError(HTTPUtilException):
    __module__ = __name__

    def __init__(self, what, statusCode):
        HTTPUtilException.__init__(self, what)
        self.statusCode = statusCode


class UnexpectedResponse(HTTPUtilException):
    __module__ = __name__

    def __init__(self, what):
        HTTPUtilException.__init__(self, what)


def getHTTPResponse(url, http, body=''):
    if body:
        hd = http.postForm(url, body)
    else:
        hd = http.getDocument(url)
    if not hd.isValid():
        raise ConnectionError('Unable to reach %s' % url.cStr(), hd.getStatusCode())
    stream = hd.openReadBody()
    sr = StreamReader(stream, 1)
    response = sr.readlines()
    for i in xrange(len(response)):
        if response[i][-1] == '\n':
            response[i] = response[i][:-1]

    return response