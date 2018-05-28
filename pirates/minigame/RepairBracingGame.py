# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.minigame.RepairBracingGame
import random, math
from pandac.PandaModules import NodePath
from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from RepairMincroGame import RepairMincroGame
from RepairGridPiece import RepairGridPiece, GOAL_HORIZ_1, GOAL_HORIZ_2, GOAL_VERT_1, GOAL_CROSS_1_1
from RepairGridPiece import TOP, BOTTOM, LEFT, RIGHT
import RepairGlobals
SPACING = 0.15
GRID_SIZE = 4

class RepairBracingGame(RepairMincroGame):
    __module__ = __name__
    moveSound = None
    lineCompleteSound = None

    def __init__(self, repairGame):
        self.config = RepairGlobals.Bracing
        RepairMincroGame.__init__(self, repairGame, 'bracing', PLocalizer.Minigame_Repair_Bracing_Start)

    def _initVars(self):
        RepairMincroGame._initVars(self)
        self.currentGridDimensionAndLineCount = self.config.difficultyLevels[0]
        self.linesComplete = 0

    def _initAudio(self):
        if not self.moveSound:
            RepairBracingGame.moveSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_BRACE_PIECEMOVE)
            RepairBracingGame.lineCompleteSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_BRACE_LINECOMPLETE)
        RepairMincroGame._initAudio(self)

    def _initVisuals(self):
        RepairMincroGame._initVisuals(self)
        self.model = loader.loadModel('models/gui/pir_m_gui_srp_bracing_main')
        self.background = self.model.find('**/background')
        self.background.reparentTo(self)
        self.background.setZ(0.175)
        self.gridParent = self.attachNewNode('gridParent')
        self.grid = []
        for xpos in range(GRID_SIZE):
            col = []
            for ypos in range(GRID_SIZE):
                allWoodSquaresGeom = NodePath('wood_squares')
                for i in range(self.model.find('**/wood_squares').getNumChildren()):
                    self.model.find('**/wood_squares').getChild(i).copyTo(allWoodSquaresGeom)

                tempGeom = NodePath('tempGeom')
                self.model.find('**/wood_squares').getChild(0).copyTo(tempGeom)
                selectedOutlineGeom = NodePath('selectedOutlineGeom')
                self.model.find('**/selected').copyTo(selectedOutlineGeom)
                selectedOutlineGeom.setScale(0.9)
                piece = RepairGridPiece(name='piece%i' % (xpos * GRID_SIZE + ypos), parent=self.gridParent, allWoodSquaresGeom=allWoodSquaresGeom, selectedOutlineGeom=selectedOutlineGeom, scale=(0.9,
                                                                                                                                                                                                   0.9,
                                                                                                                                                                                                   0.9), pos=(-0.22 + xpos * SPACING, 0.0, -0.03 + ypos * SPACING), command=self.onPiecePressed, location=[xpos, ypos], clickSound=None, pressEffect=0, geom=tempGeom, relief=None)
                col.append(piece)

            self.grid.append(col)

        self.createGoalPieces()
        return

    def reset(self):
        RepairMincroGame.reset(self)
        self.randomizeBoard()
        tutorialIndex = 0
        self.linesComplete = 0
        self.lastLineCompleteTime = globalClock.getRealTime()
        if len(self.currentGridDimensionAndLineCount[1]) > 1:
            tutorialIndex = 1
        self.repairGame.gui.setTutorial(self.name, tutorialIndex)
        self.repairGame.gui.setTitle(self.name)

    def destroy(self):
        RepairMincroGame.destroy(self)

    def setDifficulty(self, difficulty):
        RepairMincroGame.setDifficulty(self, difficulty)
        percent = difficulty / self.repairGame.difficultyMax
        difIndex = int(math.floor(percent * (len(self.config.difficultyLevels) - 1)))
        self.currentGridDimensionAndLineCount = self.config.difficultyLevels[difIndex]

    def getRandomGridCoords(self):
        xpos = random.randint(0, GRID_SIZE - 1)
        ypos = random.randint(0, GRID_SIZE - 1)
        return (
         xpos, ypos)

    def iterateCoordsAndPieces(self):
        result = []
        for xpos in range(GRID_SIZE):
            for ypos in range(GRID_SIZE):
                result.append((xpos, ypos, self.grid[xpos][ypos]))

        return result

    def randomizeBoard(self):
        for xpos, ypos, piece in self.iterateCoordsAndPieces():
            piece.request('Blank')
            piece.unstash()
            piece.setEnabled(False)

        self.createGoalPieces()
        for i in range(self.currentGridDimensionAndLineCount[0]):
            self.removePiece()

    def createGoalPieces(self):
        for pieceType in self.currentGridDimensionAndLineCount[1]:
            availableYSpots = []
            for i in range(GRID_SIZE):
                availableYSpots.append(i)

            goalCount = GRID_SIZE
            if GOAL_VERT_1 in self.currentGridDimensionAndLineCount[1]:
                goalCount -= 1
            for xpos in range(goalCount):
                randIndex = random.randint(0, len(availableYSpots) - 1)
                index = availableYSpots[randIndex]
                countout = 0
                while self.grid[xpos][index].isGoalPiece():
                    randIndex = random.randint(0, len(availableYSpots) - 1)
                    index = availableYSpots[randIndex]
                    countout += 1
                    if 1 or countout >= 20:
                        for j in range(GRID_SIZE):
                            if not self.grid[xpos][j].isGoalPiece():
                                index = j
                                break

                if index in availableYSpots:
                    availableYSpots.remove(index)
                self.grid[xpos][index].request('Goal', pieceType)

        if GOAL_VERT_1 in self.currentGridDimensionAndLineCount[1]:
            xpos, ypos = self.getRandomGridCoords()
            piece = self.grid[xpos][ypos]
            countout = 0
            while piece.isGoalPiece():
                xpos, ypos = self.getRandomGridCoords()
                piece = self.grid[xpos][ypos]
                countout += 1
                if countout >= 200:
                    for x in range(GRID_SIZE):
                        for y in range(GRID_SIZE):
                            if not self.grid[x][y].isGoalPiece():
                                piece = self.grid[x][y]
                                break

                    break

            piece.request('Goal', GOAL_CROSS_1_1)

    def removePiece(self):
        xpos, ypos = self.getRandomGridCoords()
        piece = self.grid[xpos][ypos]
        countout = 0
        while piece.isGoalPiece() or piece.isEmptyPiece():
            xpos, ypos = self.getRandomGridCoords()
            piece = self.grid[xpos][ypos]
            countout += 1
            if countout >= 200:
                break

        piece.request('Empty')

    def onPiecePressed(self, xpos, ypos, dir=None):
        if self.getCurrentOrNextState() in ['Game']:
            dirx = dir[0]
            diry = dir[1]
            if xpos + dirx >= GRID_SIZE or xpos + dirx < 0:
                return False
            if ypos + diry >= GRID_SIZE or ypos + diry < 0:
                return False
            if self.grid[xpos + dirx][ypos + diry].isEmptyPiece():
                self.moveSound.play()
                self.swapPieces(xpos, ypos, xpos + dirx, ypos + diry)
                self.checkWin()
                return True
        return False

    def swapPieces(self, pieceAxpos, pieceAypos, pieceBxpos, pieceBypos):
        pieceA = self.grid[pieceAxpos][pieceAypos]
        pieceB = self.grid[pieceBxpos][pieceBypos]
        posA = pieceA.getPos()
        posB = pieceB.getPos()
        locationA = pieceA.location[:]
        pieceA.setGridLocation(pieceB.location[:], posB)
        pieceB.setGridLocation(locationA, posA)
        self.grid[pieceAxpos][pieceAypos] = pieceB
        self.grid[pieceBxpos][pieceBypos] = pieceA

    def checkWin(self):
        percentages = []
        solved = []
        usedYpos = -1
        for i in range(len(self.currentGridDimensionAndLineCount[1])):
            solved.append(False)
            percentages.append(0.0)
            type = self.currentGridDimensionAndLineCount[1][i]
            if type == GOAL_HORIZ_1 or type == GOAL_HORIZ_2:
                bestGoalCount = 0
                for ypos in range(GRID_SIZE):
                    if ypos == usedYpos:
                        continue
                    goalCount = 0
                    for xpos in range(GRID_SIZE):
                        if self.grid[xpos][ypos].isGoalPiece():
                            (self.grid[xpos][ypos].pieceType == type or self.grid[xpos][ypos].pieceType == GOAL_CROSS_1_1) and goalCount += 1

                    if goalCount > bestGoalCount:
                        bestGoalCount = goalCount
                        if i == 0:
                            usedYpos = ypos

                percent = int((bestGoalCount - 1.0) / (GRID_SIZE - 1) * 100)
                percentages[-1] = percent
                if bestGoalCount == GRID_SIZE:
                    solved[-1] = True
            elif type == GOAL_VERT_1:
                bestGoalCount = 0
                for xpos in range(GRID_SIZE):
                    goalCount = 0
                    for ypos in range(GRID_SIZE):
                        if self.grid[xpos][ypos].isGoalPiece():
                            (self.grid[xpos][ypos].pieceType == type or self.grid[xpos][ypos].pieceType == GOAL_CROSS_1_1) and goalCount += 1

                    bestGoalCount = max(bestGoalCount, goalCount)

                percent = int((bestGoalCount - 1.0) / (GRID_SIZE - 1.0) * 100)
                percentages[-1] = percent
                if bestGoalCount == GRID_SIZE:
                    solved[-1] = True

        linesComplete = 0
        for lineComplete in solved:
            if lineComplete == True:
                linesComplete += 1

        rating = 0
        if linesComplete > self.linesComplete:
            self.lineCompleteSound.play()
            completeTime = globalClock.getRealTime()
            timeToBrace = self.lastLineCompleteTime - completeTime
            rating = math.ceil(max(0, self.config.repairTimeframe - timeToBrace) / (self.config.repairTimeframe / 5.0))
            self.lastLineCompleteTime = completeTime
        self.linesComplete = linesComplete
        percent = sum(percentages) / len(percentages)
        self.repairGame.d_reportMincroGameProgress(percent, rating)
        if sum(solved) == len(solved):
            self.request('Outro')

    def enterGame(self):
        RepairMincroGame.enterGame(self)
        for xpos, ypos, piece in self.iterateCoordsAndPieces():
            if not piece.isEmptyPiece():
                piece.setEnabled(True)
                piece.request('Active')

    def exitGame(self):
        RepairMincroGame.exitGame(self)
        for xpos, ypos, piece in self.iterateCoordsAndPieces():
            piece.setEnabled(False)

    def enterOutro(self):
        RepairMincroGame.enterOutro(self)
        self.repairGame.d_reportMincroGameScore(150)

    def exitOutro(self):
        RepairMincroGame.exitOutro(self)
        for xpos, ypos, piece in self.iterateCoordsAndPieces():
            piece.request('Idle')


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 or (4)
#                      0. expr
#                         compare
#                             compare_single (3)
#                                  0. expr
#                                     attribute (2)
#                                          0. expr
#                                             subscript (3)
#                                                  0. expr
#                                                     subscript (3)
#                                                          0. expr
#                                                             attribute (2)
#                                                                  0. expr
#                                                                                213  LOAD_FAST             0  'self'
#                                                                  1.            216  LOAD_ATTR            18  'grid'
#                                                          1. expr
#                                                                        219  LOAD_FAST             3  'xpos'
#                                                          2.            222  BINARY_SUBSCR    
#                                                  1. expr
#                                                                223  LOAD_FAST             9  'ypos'
#                                                  2.            226  BINARY_SUBSCR    
#                                          1.            227  LOAD_ATTR            20  'pieceType'
#                                  1. expr
#                                                230  LOAD_FAST            13  'type'
#                                  2.            233  COMPARE_OP            2  '=='
#                      1. jmp_true (2)
#                          0.            236  JUMP_IF_TRUE         27  'to 266'
#                          1.            239  POP_TOP          
#                      2. expr
#                         compare
#                             compare_single (3)
#                                  0. expr
#                                     attribute (2)
#                                          0. expr
#                                             subscript (3)
#                                                  0. expr
#                                                     subscript (3)
#                                                          0. expr
#                                                             attribute (2)
#                                                                  0. expr
#                                                                                240  LOAD_FAST             0  'self'
#                                                                  1.            243  LOAD_ATTR            18  'grid'
#                                                          1. expr
#                                                                        246  LOAD_FAST             3  'xpos'
#                                                          2.            249  BINARY_SUBSCR    
#                                                  1. expr
#                                                                250  LOAD_FAST             9  'ypos'
#                                                  2.            253  BINARY_SUBSCR    
#                                          1.            254  LOAD_ATTR            20  'pieceType'
#                                  1. expr
#                                                257  LOAD_GLOBAL          21  'GOAL_CROSS_1_1'
#                                  2.            260  COMPARE_OP            2  '=='
#                      3.          263_0  COME_FROM           236  '236'
#              1. jmp_false (2)
#                  0.            263  JUMP_IF_FALSE        14  'to 280'
#                  1.            266  POP_TOP          
#              2. expr
#                 L. 284     267  LOAD_FAST            10  'goalCount'
#              3. come_from_opt
#      1. expr
#                    270  LOAD_CONST            2  1
#      2. inplace_op
#                    273  INPLACE_ADD      
#      3. store
#                    274  STORE_FAST           10  'goalCount'
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 or (4)
#                      0. expr
#                         compare
#                             compare_single (3)
#                                  0. expr
#                                     attribute (2)
#                                          0. expr
#                                             subscript (3)
#                                                  0. expr
#                                                     subscript (3)
#                                                          0. expr
#                                                             attribute (2)
#                                                                  0. expr
#                                                                                491  LOAD_FAST             0  'self'
#                                                                  1.            494  LOAD_ATTR            18  'grid'
#                                                          1. expr
#                                                                        497  LOAD_FAST             3  'xpos'
#                                                          2.            500  BINARY_SUBSCR    
#                                                  1. expr
#                                                                501  LOAD_FAST             9  'ypos'
#                                                  2.            504  BINARY_SUBSCR    
#                                          1.            505  LOAD_ATTR            20  'pieceType'
#                                  1. expr
#                                                508  LOAD_FAST            13  'type'
#                                  2.            511  COMPARE_OP            2  '=='
#                      1. jmp_true (2)
#                          0.            514  JUMP_IF_TRUE         27  'to 544'
#                          1.            517  POP_TOP          
#                      2. expr
#                         compare
#                             compare_single (3)
#                                  0. expr
#                                     attribute (2)
#                                          0. expr
#                                             subscript (3)
#                                                  0. expr
#                                                     subscript (3)
#                                                          0. expr
#                                                             attribute (2)
#                                                                  0. expr
#                                                                                518  LOAD_FAST             0  'self'
#                                                                  1.            521  LOAD_ATTR            18  'grid'
#                                                          1. expr
#                                                                        524  LOAD_FAST             3  'xpos'
#                                                          2.            527  BINARY_SUBSCR    
#                                                  1. expr
#                                                                528  LOAD_FAST             9  'ypos'
#                                                  2.            531  BINARY_SUBSCR    
#                                          1.            532  LOAD_ATTR            20  'pieceType'
#                                  1. expr
#                                                535  LOAD_GLOBAL          21  'GOAL_CROSS_1_1'
#                                  2.            538  COMPARE_OP            2  '=='
#                      3.          541_0  COME_FROM           514  '514'
#              1. jmp_false (2)
#                  0.            541  JUMP_IF_FALSE        14  'to 558'
#                  1.            544  POP_TOP          
#              2. expr
#                 L. 304     545  LOAD_FAST            10  'goalCount'
#              3. come_from_opt
#      1. expr
#                    548  LOAD_CONST            2  1
#      2. inplace_op
#                    551  INPLACE_ADD      
#      3. store
#                    552  STORE_FAST           10  'goalCount'