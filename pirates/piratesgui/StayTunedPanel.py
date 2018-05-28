# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.StayTunedPanel
from pirates.piratesgui import NonPayerPanel
from pirates.piratesbase import PLocalizer

class StayTunedPanel(NonPayerPanel.NonPayerPanel):
    __module__ = __name__

    def configurePanel(self):
        self.NUM_IMAGES = 0
        piccard = loader.loadModel('models/textureCards/velvetpics')
        self.gameImage = [
         (
          piccard.find('**/vr_combat'), piccard.find('**/vr_quest'))]
        self.gameCaption = [
         (
          PLocalizer.VR_Cap_StayTuned1, PLocalizer.VR_Cap_StayTuned2)]
        self.gameHeader = [
         PLocalizer.VR_Head_StayTuned1]
        self.gameDescript = [
         PLocalizer.VR_StayTuned1]

    def __init__(self, w=9.0, h=6.0):
        NonPayerPanel.NonPayerPanel.__init__(self, w, h, False)
        self.upgradeButton['command'] = self.hide
        self.upgradeButton['text'] = PLocalizer.lClose
        self.clickHereButton.hide()
        self.titleText['text'] = PLocalizer.VR_StayTuned
        self.scrollRight.hide()
        self.scrollLeft.hide()
        self.underText.setZ(2.75)
        self.fullText.setZ(2.67)