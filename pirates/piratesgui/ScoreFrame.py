# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.ScoreFrame
from pirates.piratesgui.SheetFrame import SheetFrame

class ScoreFrame(SheetFrame):
    __module__ = __name__

    def __init__(self, w, h, holder, team, **kw):
        self.team = team
        title = holder.getTeamName(self.team)
        SheetFrame.__init__(self, w, h, title, holder, **kw)
        self.initialiseoptions(ScoreFrame)
        self.scoreChanged = False

    def getItemList(self):
        return self.holder.getItemList(self.team)

    def _handleItemChange(self):
        self.scoreChanged = True

    def show(self):
        if self.scoreChanged:
            self.scoreChanged = False
            self.redraw()
        SheetFrame.show(self)