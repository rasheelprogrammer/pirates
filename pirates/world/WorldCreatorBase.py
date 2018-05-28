# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.WorldCreatorBase
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
from pirates.piratesbase import TODGlobals
import os, re, imp, types
from pirates.world.WorldGlobals import LevelObject

class WorldCreatorBase:
    __module__ = __name__

    def __init__(self, repository, worldFile=None):
        self.parentWorlds = []
        self.creatingInstance = False
        self.creatingInstanceParams = None
        self.repository = repository
        self.fileDicts = {}
        self.fileObjs = {}
        self.uidVisTables = {}
        self.uidAdjTables = {}
        self.uidTodSettings = {}
        self.uidEnvSettings = {}
        self.uidVisZoneMinimaps = {}
        self.uidVisZoneTunnels = {}
        self.uidMinimapPrefix = {}
        self.footstepTable = {}
        self.environmentTable = {}
        return

    def makeMainWorld(self, worldFile):
        self.worldType = PiratesGlobals.INSTANCE_MAIN
        if worldFile is not None:
            self.loadObjectsFromFile(worldFile, self.repository)
        self.worldType = None
        return

    def loadObjectsFromFile(self, filename, parent, parentIsObj=False):
        fileDict = self.openFile(filename)
        self.fileDicts[filename] = fileDict
        objDict = fileDict.get('Objects')
        parentUid = None
        if hasattr(parent, 'getUniqueId'):
            parentUid = parent.getUniqueId()
        objects = self.loadObjectDict(objDict, parent, parentUid, dynamic=0, parentIsObj=parentIsObj, fileName=re.sub('.py', '', filename))
        return [
         fileDict, objects]

    def getFieldFromUid(self, uid, field):
        objectInfo = self.getObjectDataByUid(uid, None)
        return objectInfo.get(field, '')

    def getModelPathFromFile(self, file):
        fileDict = self.openFile(file + '.py')
        return fileDict['Objects'].values()[0]['Visual']['Model']

    @report(types=['args'], dConfigParam=['dteleport'])
    def loadFileDataRecursive(self, file):
        fileDict = self.openFile(file)
        objects = fileDict.get('Objects')
        if objects:
            self.rFindFile(objects)
        self.fileDicts[file] = fileDict

    def rFindFile(self, objSet):
        for obj in objSet.values():
            fileName = obj.get('File')
            if fileName:
                self.loadFileDataRecursive(fileName + '.py')
            objects = obj.get('Objects')
            if objects:
                self.rFindFile(objects)

    def getObjectsOfType(self, uid, objType):
        finalObjs = []
        data = self.getObjectDataByUid(uid, None)
        objRoot = LevelObject(uid, data)
        self.rGetObjects(objRoot, data.get('Objects', []), finalObjs, objType)
        fileName = data.get('File')
        if fileName:
            fileDict = self.openFile(fileName + '.py')
            self.rGetObjects(objRoot, fileDict.get('Objects', []), finalObjs, objType)
        return finalObjs

    def rGetObjects(self, parentObj, subObjs, finalObjs, objType):
        for i in subObjs:
            data = subObjs[i]
            levelObj = LevelObject(i, data)
            levelObj.transform = parentObj.transform.compose(levelObj.transform)
            objList = data.get('Objects')
            if objList:
                self.rGetObjects(levelObj, objList, finalObjs, objType)
            if objType == data.get('Type'):
                finalObjs.append(levelObj)

    def loadObjectDict(self, objDict, parent, parentUid, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        objects = []
        for objKey in objDict.keys():
            newObj = self.loadObject(objDict[objKey], parent, parentUid, objKey, dynamic, parentIsObj=parentIsObj, fileName=fileName, actualParentObj=actualParentObj)
            if newObj:
                objects.append(newObj)

        return objects

    def loadInstancedObject(self, object, parent, parentUid, objKey, instanceParams=[]):
        self.creatingInstance = True
        self.creatingInstanceParams = instanceParams
        newObj = self.loadObject(object, parent, parentUid, objKey, False)
        self.creatingInstance = False
        self.creatingInstanceParams = None
        return newObj

    def loadObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        if not self.isObjectInCurrentGamePhase(object):
            return
        prevWorld = self.world
        newObjInfo = self.createObject(object, parent, parentUid, objKey, dynamic, parentIsObj=parentIsObj, fileName=fileName, actualParentObj=actualParentObj)
        if newObjInfo:
            newObj, newActualParent = newObjInfo
        else:
            return
        instanced = object.get('Instanced')
        if instanced:
            self.world.setCanBePrivate(instanced)
        objDict = object.get('Objects')
        if objDict:
            if newObj == None:
                newObj = parent
                if hasattr(newObj, 'getUniqueId'):
                    objKey = newObj.getUniqueId()
            self.loadObjectDict(objDict, newObj, objKey, dynamic, fileName=fileName, actualParentObj=newActualParent)
        self._restoreWorld(prevWorld)
        return newObj

    def _restoreWorld(self, prevWorld):
        parentWorld = None
        if self.parentWorlds:
            parentWorld = self.parentWorlds[-1]
        if parentWorld:
            if prevWorld is not self.world:
                self.world = self.parentWorlds.pop()
        else:
            self.world = prevWorld
        return

    def createObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        objType = object.get('Type')
        self.notify.debug('createObject: type = %s' % objType)
        if dynamic and object.get('ExtUid'):
            return objType
        childFilename = object.get('File')
        if childFilename and object['Type'] != 'Building Exterior' and object['Type'] != 'Island Game Area':
            self.loadObjectsFromFile(childFilename + '.py', parent)
            return
        return objType

    def openFile(self, filename):
        objectStruct = None
        moduleName = filename[:-3]
        try:
            obj = __import__('pirates.leveleditor.worldData.' + moduleName)
        except ImportError:
            obj = None
        except ValueError, e:
            self.notify.error('%s when loading %s' % (e, filename))
        else:
            for symbol in ['leveleditor', 'worldData', moduleName, 'objectStruct']:
                if obj:
                    obj = getattr(obj, symbol, None)

            if not obj:
                self.notify.warning('Loading old-style file %s' % filename)
                spfSearchPath = DSearchPath()
                spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/leveleditor/worldData')))
                spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/src/leveleditor/worldData')))
                spfSearchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/leveleditor/worldData')))
                spfSearchPath.appendDirectory(Filename('.'))
                pfile = Filename(filename)
                found = vfs.resolveFilename(pfile, spfSearchPath)
                data = vfs.readFile(pfile, 1)
                data = data.replace('\r', '')
                try:
                    obj = eval(data)
                except SyntaxError:
                    obj = None

        return obj

    def getObjectDataByUid(self, uid, fileDict=None):
        fileDict = fileDict or self.fileDicts
        objectInfo = None
        for fileData in fileDict.itervalues():
            if uid in fileData['ObjectIds']:
                getSyntax = 'objectInfo = fileData' + fileData['ObjectIds'][uid]
                exec getSyntax
                if not objectInfo.has_key('File') or objectInfo.get('File') == '':
                    break

        return objectInfo

    def getObjectDataFromFileByUid(self, uid, fileName, getParentUid=False):
        objectInfo = None
        if fileName:
            if '.py' not in fileName:
                fileName += '.py'
            if self.isObjectDefined(uid, fileName):
                fileData = self.fileDicts[fileName]
                if getParentUid:
                    notFollowedBy = '(?!.*\\[".*\\[".*\\[".*)'
                    isFollowedBy = '(?=.*\\[".*\\[".*)'
                    match = re.search('(\\[")' + notFollowedBy + isFollowedBy + '.*?[\\]]', fileData['ObjectIds'][uid])
                    if match and match.end() - match.start() > 4:
                        return fileData['ObjectIds'][uid][match.start() + 2:match.end() - 2]
                    self.notify.warning('getObjectDataFromFileByUid: could not extract parentId from %s' % fileData['ObjectIds'][uid])
                    getSyntax = 'objectInfo = None'
                else:
                    getSyntax = 'objectInfo = fileData' + fileData['ObjectIds'][uid]
                exec getSyntax
        return objectInfo

    def getFilelistByUid--- This code section failed: ---

 339       0  LOAD_CONST            0  None
           3  STORE_FAST           10  'objectInfo'

 340       6  LOAD_FAST             2  'fileDict'
           9  JUMP_IF_TRUE         13  'to 25'
        12_0  THEN                     26
          12  POP_TOP          

 341      13  LOAD_FAST             0  'self'
          16  LOAD_ATTR             4  'fileDicts'
          19  STORE_FAST            2  'fileDict'
          22  JUMP_FORWARD          1  'to 26'
        25_0  COME_FROM             9  '9'
          25  POP_TOP          
        26_0  COME_FROM            22  '22'

 342      26  LOAD_NAME             5  'set'
          29  CALL_FUNCTION_0       0  None
          32  STORE_FAST            4  'fileList'

 343      35  SETUP_LOOP          430  'to 468'
          38  LOAD_FAST             2  'fileDict'
          41  GET_ITER         
          42  FOR_ITER            422  'to 467'
          45  STORE_FAST           12  'name'

 344      48  LOAD_FAST             2  'fileDict'
          51  LOAD_FAST            12  'name'
          54  BINARY_SUBSCR    
          55  STORE_FAST            9  'fileData'

 345      58  LOAD_FAST             9  'fileData'
          61  LOAD_CONST            1  'ObjectIds'
          64  BINARY_SUBSCR    
          65  LOAD_ATTR             9  'has_key'
          68  LOAD_FAST             1  'uid'
          71  CALL_FUNCTION_1       1  None
          74  JUMP_IF_TRUE          7  'to 84'
        77_0  THEN                     85
          77  POP_TOP          

 346      78  CONTINUE             42  'to 42'
          81  JUMP_FORWARD          1  'to 85'
        84_0  COME_FROM            74  '74'
          84  POP_TOP          
        85_0  COME_FROM            81  '81'

 347      85  LOAD_CONST            2  'objectInfo = fileData'
          88  LOAD_FAST             9  'fileData'
          91  LOAD_CONST            1  'ObjectIds'
          94  BINARY_SUBSCR    
          95  LOAD_FAST             1  'uid'
          98  BINARY_SUBSCR    
          99  BINARY_ADD       
         100  STORE_FAST            7  'getSyntax'

 348     103  LOAD_FAST             7  'getSyntax'
         106  LOAD_CONST            0  None
         109  DUP_TOP          
         110  EXEC_STMT        

 349     111  LOAD_FAST             4  'fileList'
         114  LOAD_ATTR            12  'add'
         117  LOAD_FAST            12  'name'
         120  CALL_FUNCTION_1       1  None
         123  POP_TOP          

 350     124  LOAD_FAST            10  'objectInfo'
         127  LOAD_ATTR            13  'get'
         130  LOAD_CONST            3  'Objects'
         133  CALL_FUNCTION_1       1  None
         136  STORE_FAST            6  'objects'

 351     139  LOAD_FAST             6  'objects'
         142  JUMP_IF_FALSE       156  'to 301'
       145_0  THEN                     302
         145  POP_TOP          

 352     146  SETUP_LOOP          153  'to 302'
         149  LOAD_FAST             6  'objects'
         152  LOAD_ATTR            15  'values'
         155  CALL_FUNCTION_0       0  None
         158  GET_ITER         
         159  FOR_ITER            135  'to 297'
         162  STORE_FAST            3  'obj'

 353     165  LOAD_FAST             3  'obj'
         168  LOAD_ATTR            13  'get'
         171  LOAD_CONST            4  'Visual'
         174  CALL_FUNCTION_1       1  None
         177  STORE_FAST            5  'visual'

 354     180  LOAD_FAST             5  'visual'
         183  JUMP_IF_FALSE       107  'to 293'
         186  POP_TOP          

 355     187  LOAD_FAST             5  'visual'
         190  LOAD_ATTR            13  'get'
         193  LOAD_CONST            5  'Model'
         196  CALL_FUNCTION_1       1  None
         199  STORE_FAST           11  'model'

 356     202  LOAD_FAST            11  'model'
         205  JUMP_IF_FALSE        81  'to 289'
         208  POP_TOP          

 357     209  LOAD_NAME            19  'type'
         212  LOAD_FAST            11  'model'
         215  CALL_FUNCTION_1       1  None
         218  LOAD_NAME            20  'types'
         221  LOAD_ATTR            21  'ListType'
         224  COMPARE_OP            8  'is'
         227  JUMP_IF_FALSE        38  'to 268'
         230  POP_TOP          

 358     231  SETUP_LOOP           52  'to 286'
         234  LOAD_FAST            11  'model'
         237  GET_ITER         
         238  FOR_ITER             23  'to 264'
         241  STORE_FAST            8  'currModel'

 359     244  LOAD_FAST             4  'fileList'
         247  LOAD_ATTR            12  'add'
         250  LOAD_FAST             8  'currModel'
         253  LOAD_CONST            6  '.bam'
         256  BINARY_ADD       
         257  CALL_FUNCTION_1       1  None
         260  POP_TOP          
         261  JUMP_BACK           238  'to 238'
         264  POP_BLOCK        
         265  JUMP_ABSOLUTE       290  'to 290'
       268_0  COME_FROM           227  '227'
         268  POP_TOP          

 361     269  LOAD_FAST             4  'fileList'
         272  LOAD_ATTR            12  'add'
         275  LOAD_FAST            11  'model'
         278  LOAD_CONST            6  '.bam'
         281  BINARY_ADD       
         282  CALL_FUNCTION_1       1  None
         285  POP_TOP          
       286_0  COME_FROM           231  '231'
         286  JUMP_ABSOLUTE       294  'to 294'
       289_0  COME_FROM           205  '205'
         289  POP_TOP          
         290  JUMP_BACK           159  'to 159'
       293_0  COME_FROM           183  '183'
         293  POP_TOP          
         294  JUMP_BACK           159  'to 159'
         297  POP_BLOCK        
         298  JUMP_FORWARD          1  'to 302'
       301_0  COME_FROM           142  '142'
         301  POP_TOP          
       302_0  COME_FROM           146  '146'

 362     302  LOAD_FAST             9  'fileData'
         305  LOAD_ATTR            13  'get'
         308  LOAD_CONST            3  'Objects'
         311  CALL_FUNCTION_1       1  None
         314  STORE_FAST            6  'objects'

 363     317  LOAD_FAST             6  'objects'
         320  JUMP_IF_FALSE        96  'to 419'
       323_0  THEN                     420
         323  POP_TOP          

 364     324  SETUP_LOOP           93  'to 420'
         327  LOAD_FAST             6  'objects'
         330  LOAD_ATTR            15  'values'
         333  CALL_FUNCTION_0       0  None
         336  GET_ITER         
         337  FOR_ITER             75  'to 415'
         340  STORE_FAST            3  'obj'

 365     343  LOAD_FAST             3  'obj'
         346  LOAD_ATTR            13  'get'
         349  LOAD_CONST            4  'Visual'
         352  CALL_FUNCTION_1       1  None
         355  STORE_FAST            5  'visual'

 366     358  LOAD_FAST             5  'visual'
         361  JUMP_IF_FALSE        47  'to 411'
         364  POP_TOP          

 367     365  LOAD_FAST             5  'visual'
         368  LOAD_ATTR            13  'get'
         371  LOAD_CONST            5  'Model'
         374  CALL_FUNCTION_1       1  None
         377  STORE_FAST           11  'model'

 368     380  LOAD_FAST            11  'model'
         383  JUMP_IF_FALSE        21  'to 407'
         386  POP_TOP          

 369     387  LOAD_FAST             4  'fileList'
         390  LOAD_ATTR            12  'add'
         393  LOAD_FAST            11  'model'
         396  LOAD_CONST            6  '.bam'
         399  BINARY_ADD       
         400  CALL_FUNCTION_1       1  None
         403  POP_TOP          
         404  JUMP_ABSOLUTE       412  'to 412'
       407_0  COME_FROM           383  '383'
         407  POP_TOP          
         408  JUMP_BACK           337  'to 337'
       411_0  COME_FROM           361  '361'
         411  POP_TOP          
         412  JUMP_BACK           337  'to 337'
         415  POP_BLOCK        
         416  JUMP_FORWARD          1  'to 420'
       419_0  COME_FROM           320  '320'
         419  POP_TOP          
       420_0  COME_FROM           324  '324'

 371     420  LOAD_FAST            10  'objectInfo'
         423  LOAD_ATTR             9  'has_key'
         426  LOAD_CONST            7  'File'
         429  CALL_FUNCTION_1       1  None
         432  UNARY_NOT        
         433  JUMP_IF_TRUE         22  'to 458'
         436  POP_TOP          
         437  LOAD_FAST            10  'objectInfo'
         440  LOAD_ATTR            13  'get'
         443  LOAD_CONST            7  'File'
         446  CALL_FUNCTION_1       1  None
         449  LOAD_CONST            8  ''
         452  COMPARE_OP            2  '=='
       455_0  COME_FROM           433  '433'
         455  JUMP_IF_FALSE         5  'to 463'
         458  POP_TOP          

 374     459  BREAK_LOOP       
         460  JUMP_BACK            42  'to 42'
       463_0  COME_FROM           455  '455'
         463  POP_TOP          
         464  JUMP_BACK            42  'to 42'
         467  POP_BLOCK        
       468_0  COME_FROM            35  '35'

 375     468  LOAD_NAME            23  'list'
         471  LOAD_FAST             4  'fileList'
         474  CALL_FUNCTION_1       1  None
         477  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 286

    def getObjectIslandUid(self, objUid, fileDict=None):
        if not fileDict:
            fileDict = self.fileDicts
        found = False
        curUid = objUid
        isPrivate = False
        while curUid:
            curFile = None
            for name in fileDict:
                fileData = fileDict[name]
                if not fileData['ObjectIds'].has_key(str(curUid)):
                    continue
                if fileData['Objects'].has_key(str(curUid)):
                    if fileData['Objects'][str(curUid)].get('Type') == 'Island':
                        return (str(curUid), isPrivate)
                    continue
                objData = fileData['Objects'].values()[0]['Objects']
                if objData.has_key(str(curUid)):
                    if curUid == objUid:
                        if objData[str(curUid)].get('Private Status') == 'Private Only':
                            isPrivate = True
                    if objData[str(curUid)].get('Type') == 'Island':
                        return (str(curUid), isPrivate)
                curFile = fileData
                break

            if not curFile:
                return
            else:
                curUid = curFile.get('Objects', {}).keys()[0]
                if curFile['Objects'][str(curUid)].get('Type') == 'Island':
                    return (curUid, isPrivate)

        return

    def isObjectDefined(self, objUid, fileName):
        return fileName in self.fileDicts and objUid in self.fileDicts[fileName]['ObjectIds']

    def getObject(self, parentObj, key):
        data = parentObj.data['Objects'].get(key)
        if data:
            return LevelObject(key, data)
        return

    def loadTemplateObject(self, filename, gameArea, rootTransform):
        fileData = self.openFile(filename)
        fileObjUid = fileData['Objects'].keys()[0]
        fileObj = self.getObject(LevelObject(fileObjUid, fileData), fileObjUid)
        fileObj.transform = rootTransform.compose(fileObj.transform)
        for objKey in fileObj.data.get('Objects', []):
            obj = self.getObject(fileObj, objKey)
            obj.transform = fileObj.transform.compose(obj.transform)
            self.loadObj(obj, gameArea)

    def loadObj(self, levelObj, gameArea):
        newObj = self.createObj(levelObj, gameArea)
        for objKey in levelObj.data.get('Objects', []):
            obj = self.getObject(levelObj, objKey)
            obj.transform = levelObj.transform.compose(obj.transform)
            self.loadObj(obj, gameArea)

        templates = levelObj.data.get('AdditionalData', [])
        for file in templates:
            self.loadTemplateObject(file + '.py', gameArea, levelObj.transform)

        objFile = levelObj.data.get('File')
        if objFile:
            self.registerFileObject(objFile + '.py')

    def storeNecessaryAreaData(self, areaUid, areaData):
        visTable = areaData.get('Vis Table')
        if visTable:
            self.uidVisTables[areaUid] = visTable
        adjTable = areaData.get('Adj Table')
        if adjTable:
            self.uidAdjTables[areaUid] = adjTable
        self.uidVisZoneMinimaps[areaUid] = areaData.get('VisZone Minimaps', {})
        self.uidVisZoneTunnels[areaUid] = areaData.get('Tunnel Minimaps', {})
        if areaData.get('Minimap', False):
            self.uidMinimapPrefix[areaUid] = areaData.get('Minimap Prefix', '')
        environmentName = None
        footStepSound = None
        envSettings = None
        baseObject = None
        objectData = areaData.get('Objects')
        if objectData:
            baseObject = objectData.get(areaUid)
        if baseObject:
            environmentName = baseObject.get('Environment')
            if environmentName:
                self.environmentTable[areaUid] = environmentName
            footStepSound = baseObject.get('Footstep Sound')
            if footStepSound:
                self.footstepTable[areaUid] = footStepSound
        if envSettings == None:
            envSettings = areaData.get('LevelEnvironment')
            if envSettings:
                self.uidEnvSettings[areaUid] = envSettings
        return

    def registerFileObject(self, filename):
        fileData = self.openFile(filename)
        self.fileDicts[filename] = fileData
        fileObjUid = fileData['Objects'].keys()[0]
        self.storeNecessaryAreaData(fileObjUid, fileData)
        self.fileObjs[fileObjUid] = LevelObject(fileObjUid, fileData['Objects'][fileObjUid])
        self.registerSubObj(self.fileObjs[fileObjUid])

    def registerSubObj(self, levelObj):
        for objKey in levelObj.data.get('Objects', []):
            obj = self.getObject(levelObj, objKey)
            self.registerSubObj(obj)

        objFile = levelObj.data.get('File')
        if objFile:
            self.registerFileObject(objFile + '.py')

    def loadFileObjFromUid(self, uniqueId, gameArea, transformParent):
        levelObj = self.fileObjs[uniqueId]
        looseNum = len(levelObj.data.get('Objects', []))
        base.loadingScreen.beginStep('LoadingObjects', looseNum, 80)
        for objKey in levelObj.data.get('Objects', []):
            obj = self.getObject(levelObj, objKey)
            self.loadObj(obj, gameArea)
            base.loadingScreen.tick()

        base.loadingScreen.endStep('LoadingObjects')
        templates = levelObj.data.get('AdditionalData', [])
        for file in templates:
            self.loadTemplateObject(file + '.py', gameArea, levelObj.transform)

        self.storeNecessaryAreaData(uniqueId, levelObj.data)

    def getTodSettingsByUid(self, uniqueId):
        return self.uidTodSettings.get(uniqueId, None)

    def getEnvSettingsByUid(self, uniqueId):
        return self.uidEnvSettings.get(uniqueId, None)