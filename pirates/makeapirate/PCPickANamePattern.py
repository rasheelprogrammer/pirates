# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.makeapirate.PCPickANamePattern
from direct.showbase.PythonUtil import listToItem2index
from otp.namepanel.PickANamePattern import PickANamePatternTwoPartLastName
from pirates.piratesbase.PiratesGlobals import maleNames, femaleNames, lastNamePrefixesCapped

class PCPickANamePattern(PickANamePatternTwoPartLastName):
    __module__ = __name__
    NameParts = None

    def _getNameParts(self, gender):
        if PCPickANamePattern.NameParts is None:
            PCPickANamePattern.NameParts = {}
            maleNameParts = []
            for nameList in maleNames:
                maleNameParts.append(listToItem2index(nameList))

            femaleNameParts = []
            for nameList in femaleNames:
                femaleNameParts.append(listToItem2index(nameList))

            PCPickANamePattern.NameParts['m'] = maleNameParts
            PCPickANamePattern.NameParts['f'] = femaleNameParts
        return PCPickANamePattern.NameParts[gender]

    def _getLastNameCapPrefixes(self):
        return lastNamePrefixesCapped