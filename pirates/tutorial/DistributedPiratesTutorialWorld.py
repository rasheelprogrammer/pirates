# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.tutorial.DistributedPiratesTutorialWorld
import time
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.actor import Actor
from direct.task import Task
from direct.showbase.PythonUtil import report
from pirates.npc import Skeleton
from pirates.pirate import Pirate
from pirates.pirate import HumanDNA
from pirates.quest import QuestParser
from pirates.makeapirate import MakeAPirate
from pirates.piratesbase import PiratesGlobals
from pirates.instance import DistributedInstanceBase
from pirates.cutscene import CutsceneData
from pirates.piratesbase import TimeOfDayManager

class DistributedPiratesTutorialWorld(DistributedInstanceBase.DistributedInstanceBase):
    __module__ = __name__
    notify = directNotify.newCategory('DistributedPiratesTutorialWorld')