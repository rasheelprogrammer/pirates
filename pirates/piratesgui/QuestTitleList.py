# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.QuestTitleList
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemGui
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import WeaponGlobals
from pirates.quest import QuestLadderDB
from pirates.quest import QuestDB, Quest
from pirates.quest import QuestDNA
from pirates.quest import QuestLadderDNA
from pirates.quest.QuestTaskDNA import *
from pirates.piratesgui import QuestTitleTiers
from pirates.piratesbase import Freebooter

class QuestTitleNode:
    __module__ = __name__

    def __init__(self, questDNA, hideButton=False):
        self.questDNA = questDNA
        self.hideButton = hideButton
        if questDNA:
            self.questId = questDNA.getQuestId()
        else:
            self.questId = None
        self.children = {}
        return

    def getChildren(self):
        if isinstance(self.questDNA, QuestLadderDNA.QuestBranchDNA):
            firstQuestId = self.questDNA.getFirstQuestId()
            children = self.children.values()
            firstChild = self.children.get(firstQuestId)
            if not firstChild:
                return self.children.values()
            else:
                if firstChild in children:
                    children.remove(firstChild)
            return [
             firstChild] + children
        return self.children.values()

    def hasChild(self, questId):
        return questId in self.children

    def addChild(self, node):
        return self.children.setdefault(node.questId, node)


class QuestTitleList(DirectScrolledFrame):
    __module__ = __name__
    charGui = None
    compassGui = None
    chapter4Lockout = False
    questButton = None
    questButtonSelected = None

    def __init__(self):
        self.width = 0.95
        self.height = 0.54
        self.loadButtonGui()
        if not base.config.GetBool('enable-next-chapter', 0):
            self.chapter4Lockout = True
        if not self.charGui:
            self.charGui = loader.loadModel('models/gui/char_gui')
            self.compassGui = loader.loadModel('models/gui/compass_main')
        DirectScrolledFrame.__init__(self, relief=None, state=DGG.NORMAL, manageScrollBars=0, autoHideScrollBars=1, frameSize=(0, self.width, 0, self.height), canvasSize=(0, self.width - 0.05, 0.025, self.height - 0.025), verticalScroll_relief=None, verticalScroll_image=self.charGui.find('**/chargui_slider_small'), verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, self.height), verticalScroll_image_scale=(self.height + 0.05, 1, 0.75), verticalScroll_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                90), verticalScroll_image_pos=(self.width - PiratesGuiGlobals.ScrollbarSize * 0.5 - 0.004, 0, self.height * 0.5), verticalScroll_image_color=(0.61,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              1), verticalScroll_thumb_image=(self.charGui.find('**/chargui_slider_node'), self.charGui.find('**/chargui_slider_node_down'), self.charGui.find('**/chargui_slider_node_over')), verticalScroll_thumb_relief=None, verticalScroll_thumb_image_scale=0.4, verticalScroll_resizeThumb=0, horizontalScroll_relief=None, sortOrder=5)
        self.initialiseoptions(QuestTitleList)
        self.verticalScroll.incButton.destroy()
        self.verticalScroll.decButton.destroy()
        self.horizontalScroll.incButton.destroy()
        self.horizontalScroll.decButton.destroy()
        self.horizontalScroll.hide()
        self.trees = {}
        self.buttons = []
        self.selectedButton = None
        self.accept('press-wheel_up-%s' % self.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.guiId, self.mouseWheelDown)
        return

    def mouseWheelUp(self, task=None):
        if self.verticalScroll.isHidden():
            return
        amountScroll = 0.05
        if self.verticalScroll['value'] > 0:
            self.verticalScroll['value'] -= amountScroll

    def mouseWheelDown(self, task=None):
        if self.verticalScroll.isHidden():
            return
        amountScroll = 0.05
        if self.verticalScroll['value'] < 1.0:
            self.verticalScroll['value'] += amountScroll

    def destroy(self):
        del self.trees
        for button in self.buttons:
            button.destroy()

        del self.buttons
        DirectScrolledFrame.destroy(self)

    def repack(self):
        z = 0
        for button in self.buttons:
            if button.indent == 0:
                z -= 0.08
            else:
                z -= 0.042
            button.setPos(0, 0, z)

        self['canvasSize'] = (
         0, self.width - 0.05, z, 0)

    def update(self, questIdList, quest, newQuest):
        if quest and isinstance(quest, Quest.Quest):
            if newQuest:
                localAvatar.questStatus.assignQuest(quest)
                container = localAvatar.questStatus.getContainer(quest.questId)
                if not container:
                    container = localAvatar.getQuestById(quest.questId)
                container.viewedInGUI = False
        for button in self.buttons:
            button.destroy()

        self.buttons = []
        self.trees = {}
        for questId in questIdList:
            path = QuestLadderDB.getFamePath(questId)
            if path:
                pathName = path[0].getName()
                tree = self.trees.get(pathName)
                self.trees[pathName] = self.__makeTree(path, tree)
            else:
                path = QuestLadderDB.getFortunePath(questId)
                if path:
                    pathName = path[0].getName()
                    tree = self.trees.get(pathName)
                    self.trees[pathName] = self.__makeTree(path, tree)
                else:
                    path = [
                     QuestDB.QuestDict.get(questId)]
                    self.trees[questId] = self.__makeTree(path, tree=None)

        treeList = self.orderTrees()
        for tree in treeList:
            self.__makeButtons(self.getCanvas(), tree)

        self.repack()
        return

    def orderTrees(self):
        newList = []
        qTier1 = []
        qTier1b = []
        qTier2 = []
        qTier3 = []
        qTier4 = []
        qTier5 = []
        qTier6 = []
        qTier7 = []
        qTier8 = []
        for tree in self.trees.keys():
            treeObject = self.trees[tree]
            if QuestTitleTiers.firstTier.count(tree):
                qTier1.append(treeObject)
            elif QuestTitleTiers.storyTier.count(tree):
                qTier1b.append(treeObject)
            elif QuestTitleTiers.secondTier.count(tree):
                qTier2.append(treeObject)
            elif QuestTitleTiers.thirdTier.count(tree):
                qTier3.append(treeObject)
            elif QuestTitleTiers.fourthTier.count(tree):
                qTier4.append(treeObject)
            elif QuestTitleTiers.fifthTier.count(tree):
                qTier5.append(treeObject)
            elif QuestTitleTiers.sixthTier.count(tree):
                qTier6.append(treeObject)
            elif QuestTitleTiers.seventhTier.count(tree):
                qTier7.append(treeObject)
            else:
                qTier8.append(treeObject)

        newList.extend(qTier1)
        newList.extend(qTier1b)
        newList.extend(qTier2)
        newList.extend(qTier3)
        newList.extend(qTier4)
        newList.extend(qTier5)
        newList.extend(qTier6)
        newList.extend(qTier7)
        newList.extend(qTier8)
        return newList

    def __makeTree(self, path, tree):
        if not tree:
            tree = QuestTitleNode(None)
        parent = tree
        for node in path:
            if node:
                if self.chapter4Lockout and node.getQuestId() == 'c4.1visitValentina':
                    pass
                else:
                    parent = parent.addChild(QuestTitleNode(node, node.hideButton))

        return tree

    def __graphWalker(self, node, indent=-1):
        yield (node, indent)
        for child in node.getChildren():
            if child.hideButton:
                for result in self.__graphWalker(child, indent):
                    yield result

            else:
                for result in self.__graphWalker(child, indent + 1):
                    yield result

    def __getContainer(self, questId):
        localAvatar.questStatus.forceInit()
        container = localAvatar.questStatus.getContainer(questId)
        if container:
            return container
        quest = localAvatar.getQuestById(questId)
        return quest

    def __getText(self, indent, questId, isContainer=False):
        text = '    ' * (indent - 1)
        localizerText = None
        if not isContainer:
            localizerText = PLocalizer.QuestStrings.get(questId)
            if localizerText:
                text += localizerText.get('title', questId)
            else:
                text += questId
        else:
            if indent == 0:
                format = '\x01questTitle2\x01%s\x02'
            else:
                format = '%s'
            localizerText = PLocalizer.QuestStrings.get(questId)
            if localizerText:
                text += format % localizerText.get('title', questId)
            else:
                text += format % questId
        localAvatar.questStatus.forceInit()
        container = localAvatar.questStatus.getContainer(questId)
        if not container:
            container = localAvatar.getQuestById(questId)
        if not container:
            return text
        if container.isComplete(showComplete=True):
            quest = localAvatar.getQuestById(container.getQuestId())
            if quest:
                if quest.getTasks():
                    not filter(lambda x: isinstance(quest.getTasks()[0], x), [VisitTaskDNA, DeliverItemTaskDNA]) and text += '   \x01questComplete\x01' + PLocalizer.QuestTitleComplete + '\x02'
            container.viewedInGUI or text += '   \x01questNew\x01' + PLocalizer.QuestTitleNew + '\x02'
        if not isContainer:
            progressList = container.getTaskProgress()
            for prog in progressList:
                progress = prog[0]
                goal = prog[1]
                if progress < goal:
                    quest = localAvatar.getQuestById(container.getQuestId())
                    if goal > 1:
                        quest and quest.getTasks() and not isinstance(quest.getTasks()[0], DowsingRodTaskDNA) and text += '   \x01questPercent\x01%d of %d\x02' % (progress, goal)
                else:
                    text += '   \x01questComplete\x01' + PLocalizer.QuestTitleComplete + '\x02'

        else:
            if container.isChoice():
                count, total, length = container.getProgress(showComplete=True)
                if total == length:
                    text += '   \x01questPercent\x01%d of %d\x02' % (count, total)
                else:
                    text += '   \x01questPercent\x01%d of %d (of %d)\x02' % (count, total, length)
                format = ' \x01questPercent\x01%s\x02'
                if localizerText:
                    text += format % localizerText.get('items', 'Items')
                else:
                    text += format % 'Items'
            else:
                for quest in localAvatar.getQuests():
                    if container.hasQuest(quest.getQuestId()):
                        questId = quest.getQuestId()
                        break

                compCont, cont = QuestLadderDB.getPercentComplete(container.getName(), questId)
                compNum = 0
                if compCont > 0 and cont > 0:
                    compNum = int(float(compCont) / float(cont) * 100.0)
                    text += '   \x01questPercent\x01%d%%\x02' % compNum
        return text

    def __makeButtons(self, guiParent, tree):
        i = 0
        for node, indent in self.__graphWalker(tree):
            if not node.questId:
                continue
            if node.hideButton:
                continue
            isContainer = isinstance(node.questDNA, QuestLadderDNA.QuestContainerDNA)
            text = self.__getText(indent, node.questId, isContainer)
            text_scale = PiratesGuiGlobals.TextScaleLarge
            frameSize = (0, 0.92, 0, 0.042)
            text_pos = (0.06, 0.01)
            textFg = PiratesGuiGlobals.TextFG1
            if indent == 0:
                text_pos = (0.01, 0.01)
            button = DirectButton(parent=guiParent, relief=None, frameSize=frameSize, borderWidth=(0.005,
                                                                                                   0.005), text=text, text_fg=textFg, text_scale=text_scale, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=text_pos, command=self.select, extraArgs=[node.questId])
            questDNA = QuestDB.QuestDict.get(node.questId)
            if questDNA:
                if questDNA.getVelvetRoped():
                    if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                        subCard = loader.loadModel('models/gui/toplevel_gui')
                        appendMe = DirectFrame(parent=button, relief=None, pos=(self.width - 0.98, 0, -0.03), state=DGG.DISABLED, geom=subCard.find('**/pir_t_gui_gen_key_subscriber'), geom_scale=0.1, geom_pos=(0.06,
                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                  0.06))
                        subCard.removeNode()
            button.accept('press-wheel_up-%s' % button.guiId, self.mouseWheelUp)
            button.accept('press-wheel_down-%s' % button.guiId, self.mouseWheelDown)
            button.indent = indent
            button.questId = node.questId
            self.updateButton(button)
            self.buttons.append(button)
            i += 1

        return

    def updateButton(self, button, selected=False):
        titleTextLen = len(PLocalizer.QuestStrings.get(button.questId).get('title'))
        indentLen = 4 * button.indent
        button['image'] = QuestTitleList.questButtonSelected
        if not selected:
            button['image'] = QuestTitleList.questButton
        button['image_color'] = Vec4(0.5, 0.08, 0.018, 1)
        if not indentLen:
            button['image_scale'] = (
             titleTextLen * 0.057, 0.38, 0.38)
            button['image_pos'] = ((titleTextLen + indentLen) * 0.0122, 0, 0.023)
        else:
            button['image_scale'] = (
             titleTextLen * 0.052, 0.36, 0.36)
            button['image_pos'] = ((titleTextLen + indentLen) * 0.01, 0, 0.023)

    def showTracked(self, questId):
        for button in self.buttons:
            if button.questId == questId:
                button['geom'] = self.compassGui.find('**/icon_objective_grey')
                button['geom_color'] = Vec4(1, 1, 0, 1)
                button['geom_scale'] = 0.14
                button['geom_pos'] = (0.02, 0, 0.025)
            else:
                button['geom'] = None

        return

    def select(self, questId):
        messenger.send('questGuiSelect', [questId])
        if self.selectedButton:
            self.updateButton(self.selectedButton, selected=False)
            self.selectedButton = None
        for button in self.buttons:
            if button.questId == questId:
                self.updateButton(button, selected=True)
                self.selectedButton = button
                break

        if self.selectedButton is None:
            return
        container = localAvatar.questStatus.getContainer(questId)
        if not container:
            container = localAvatar.getQuestById(questId)
        if container:
            if not container.viewedInGUI:
                container.viewedInGUI = True
                self.selectedButton['text'] = self.__getText(self.selectedButton.indent, questId)
        return

    def loadButtonGui(self):
        if QuestTitleList.questButton:
            return
        gui = loader.loadModel('models/gui/toplevel_gui')
        buttons = (gui.find('**/pir_t_gui_but_quest'), gui.find('**/pir_t_gui_but_quest_down'), gui.find('**/pir_t_gui_but_quest_over'))
        QuestTitleList.questButton = (
         None, buttons[1], buttons[2])
        QuestTitleList.questButtonSelected = buttons
        return


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                 unary_not (2)
#                      0. expr
#                         call (4)
#                              0. expr
#                                            322  LOAD_GLOBAL          21  'filter'
#                              1. expr
#                                 _mklambda
#                                     mklambda (3)
#                                          0. load_closure
#                                                        325  LOAD_CLOSURE          0  'quest'
#                                          1.            328  LOAD_LAMBDA              '<code_object <lambda>>'
#                                          2.            331  MAKE_CLOSURE_0        0  None
#                              2. expr
#                                 list (3)
#                                      0. expr
#                                                    334  LOAD_GLOBAL          22  'VisitTaskDNA'
#                                      1. expr
#                                                    337  LOAD_GLOBAL          23  'DeliverItemTaskDNA'
#                                      2.            340  BUILD_LIST_2          2  None
#                              3.            343  CALL_FUNCTION_2       2  None
#                      1.            346  UNARY_NOT        
#              1. jmp_false (2)
#                  0.            347  JUMP_IF_FALSE        25  'to 375'
#                  1.            350  POP_TOP          
#              2. expr
#                 L. 301     351  LOAD_FAST             5  'text'
#              3. come_from_opt
#      1. expr
#         binary_expr (3)
#              0. expr
#                 binary_expr (3)
#                      0. expr
#                                    354  LOAD_CONST            9  '   \x01questComplete\x01'
#                      1. expr
#                         attribute (2)
#                              0. expr
#                                            357  LOAD_GLOBAL           5  'PLocalizer'
#                              1.            360  LOAD_ATTR            24  'QuestTitleComplete'
#                      2. binary_op
#                                    363  BINARY_ADD       
#              1. expr
#                            364  LOAD_CONST           10  '\x02'
#              2. binary_op
#                            367  BINARY_ADD       
#      2. inplace_op
#                    368  INPLACE_ADD      
#      3. store
#                    369  STORE_FAST            5  'text'
# improper augmented assigment (e.g. +=, *=, ...):
#	aug_assign1 (4)
#      0. expr
#         and (4)
#              0. expr
#                            514  LOAD_DEREF            0  'quest'
#              1. jmp_false (2)
#                  0.            517  JUMP_IF_FALSE        64  'to 584'
#                  1.            520  POP_TOP          
#              2. expr
#                 and (4)
#                      0. expr
#                         call (2)
#                              0. expr
#                                 attribute (2)
#                                      0. expr
#                                                    521  LOAD_DEREF            0  'quest'
#                                      1.            524  LOAD_ATTR            20  'getTasks'
#                              1.            527  CALL_FUNCTION_0       0  None
#                      1. jmp_false (2)
#                          0.            530  JUMP_IF_FALSE        51  'to 584'
#                          1.            533  POP_TOP          
#                      2. expr
#                         and (4)
#                              0. expr
#                                 unary_not (2)
#                                      0. expr
#                                         call (4)
#                                              0. expr
#                                                            534  LOAD_GLOBAL          32  'isinstance'
#                                              1. expr
#                                                 subscript (3)
#                                                      0. expr
#                                                         call (2)
#                                                              0. expr
#                                                                 attribute (2)
#                                                                      0. expr
#                                                                                    537  LOAD_DEREF            0  'quest'
#                                                                      1.            540  LOAD_ATTR            20  'getTasks'
#                                                              1.            543  CALL_FUNCTION_0       0  None
#                                                      1. expr
#                                                                    546  LOAD_CONST            4  0
#                                                      2.            549  BINARY_SUBSCR    
#                                              2. expr
#                                                            550  LOAD_GLOBAL          33  'DowsingRodTaskDNA'
#                                              3.            553  CALL_FUNCTION_2       2  None
#                                      1.            556  UNARY_NOT        
#                              1. jmp_false (2)
#                                  0.            557  JUMP_IF_FALSE        24  'to 584'
#                                  1.            560  POP_TOP          
#                              2. expr
#                                 L. 314     561  LOAD_FAST             5  'text'
#                              3. come_from_opt
#                      3. come_from_opt
#              3. come_from_opt
#      1. expr
#         binary_expr (3)
#              0. expr
#                            564  LOAD_CONST           12  '   \x01questPercent\x01%d of %d\x02'
#              1. expr
#                 tuple (3)
#                      0. expr
#                                    567  LOAD_FAST            11  'progress'
#                      1. expr
#                                    570  LOAD_FAST             7  'goal'
#                      2.            573  BUILD_TUPLE_2         2  None
#              2. binary_op
#                            576  BINARY_MODULO    
#      2. inplace_op
#                    577  INPLACE_ADD      
#      3. store
#                    578  STORE_FAST            5  'text'