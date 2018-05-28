# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.leveleditor.worldData.dataToText
import direct, sys
dataFileName = sys.argv[1]
textFileName = sys.argv[2]
dataModule = dataFileName.split('.py')[0]
print 'Parsing %s.py --> %s\n' % (dataModule, textFileName)
exec 'from pirates.leveleditor.worldData.%s import *' % dataModule
lines = []
for mainUid in objectStruct['Objects']:
    mainObj = objectStruct['Objects'][mainUid]
    lines.append('Name:\t%s\t%s\nType:\t%s\n\n' % (mainObj['Name'], mainUid, mainObj['Type']))
    for uid in mainObj['Objects']:
        object = mainObj['Objects'][uid]
        lines.append('%s\t%s\t%s\n' % (uid, object['Type'], `(object['Pos'])`))

    lines.append('\n')

textFile = file(textFileName, 'w')
textFile.writelines(lines)
textFile.close()