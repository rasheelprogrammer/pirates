# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.map.Mappable


class Mappable:
    __module__ = __name__

    def __init__(self):
        pass

    def getMapNode(self):
        return


class MappableArea(Mappable):
    __module__ = __name__

    def getMapName(self):
        return ''

    def getZoomLevels(self):
        return ((100, 200, 300), 1)

    def getFootprintNode(self):
        return

    def getShopNodes(self):
        return ()

    def getCapturePointNodes(self, holidayId):
        return ()


class MappableGrid(MappableArea):
    __module__ = __name__

    def getGridParamters(self):
        return ()