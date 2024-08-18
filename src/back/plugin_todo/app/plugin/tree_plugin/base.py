from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import Plugin
from ...utils import register
from ....widget import InputTree

class TreePlugin(Plugin):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.setUI()
        self.m_follow_index=True

    def setUI(self):

        super().setUI()

        self.ui.addWidget(InputTree(), 'main', main=True)

        self.ui.main.tree.clicked.connect(self.on_outlineClicked)
        self.ui.main.tree.itemChanged.connect(self.on_itemChanged)
        self.ui.main.tree.expanded.connect(self.on_outlineExpanded)
        self.ui.main.tree.openWanted.connect(self.on_outlineClicked)
        self.ui.main.tree.indexChanged.connect(self.on_indexChanged)
        self.ui.main.tree.collapsed.connect(self.on_outlineCollapsed)
        self.ui.main.tree.returnPressed.connect(self.on_outlineClicked)

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    def activate(self):

        self.activated=True
        self.ui.activate()

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()

    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    @register('i')
    def openBelow(self): 

        self.open(how='below', focus=False)
        self.ui.show()

    @register('I')
    def openBelowFocus(self): 

        self.open(how='below', focus=True)

    @register('o')
    def openReset(self): 

        self.open(how='reset', focus=False)
        self.ui.show()

    @register('O')
    def openResetFocus(self): self.open(how='reset', focus=True)
    
    @register('L')
    def openAndDeactivate(self): 

        self.open(how='reset', focus=True)
        self.deactivate()

    @register('s')
    def center(self):

        if not self.m_follow_index:
            self.m_follow_index=True
            self.ui.main.tree.indexChanged.disconnect(self.on_outlineClicked)
        else:
            self.m_follow_index=False
            self.ui.main.tree.indexChanged.connect(self.on_outlineClicked)

    def open(self, how, focus, *args, **kwargs): 

        if focus:
            self.app.modes.setMode('normal')
        else:
            self.ui.show()

    def on_outlineCollapsed(self, index): pass

    def on_outlineExpanded(self, index): pass

    def on_outlineClicked(self, index=None): pass

    def setData(self): pass

    def on_indexChanged(self, index): pass

    def on_itemChanged(self, item): pass

    def on_viewChanged(self, view): self.setData()

    def find(self, item, model, parent=None):

        root=model.invisibleRootItem()
        if root.rowCount()>0: 
            if not parent: parent=model.indexFromItem(root.child(0,0))

            for row in range(model.rowCount(parent)):
                index=model.index(row, 0, parent)
                if index==model.indexFromItem(item): return index
            for row in range(model.rowCount(parent)):
                index=model.index(row, 0, parent)
                match=self.sync(item, model, index)
                if match.isValid(): return match
            if root.rowCount()>0:
                return model.indexFromItem(root.child(0,0))
