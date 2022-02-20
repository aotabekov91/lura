from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .model import QuickmarkModel
from .table import QuickmarksTable

class Quickmarks(QWidget):

    def __init__(self, parent, settings):
        super().__init__()
        self.window=parent
        self.s_settings=settings
        self.name='quickmarks'
        self.location='right'
        self.globalKeys={
                'Ctrl+m': (
                    self.get, 
                    self.window.display,
                    Qt.WidgetWithChildrenShortcut,
                    ),
                '`': (
                    self.toggleTable,
                    self.window.display,
                    Qt.WidgetWithChildrenShortcut,
                    ), 
                }
        self.setup()
        
    def setup(self):

        self.activated=False
        self.currentView=None

        self.markActions={}

        self.m_table=CQTableView(self, self.window)

        self.window.plugin.tables.addTable(QuickmarksTable)
        self.db=self.window.plugin.tables.quickmarks

        self.editor=QLineEdit()
        self.set=lambda: self.get(initial=False)
        self.editor.textChanged.connect(self.set)
        self.label=QLabel('Quickmark')

        layout=QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.editor)

        self.window.setTabLocation(self.m_table, self.location, self.name)

    def toggle(self):
        if not self.activated:
            self.window.activateStatusBar(self)
            self.activated=True
        else:
            self.window.deactivateStatusBar(self)
            self.activated=False

    def get(self, initial=True):
        if not self.window.view().__class__.__name__ in ['DocumentView', 'BrowserView']: return

        if initial:

            self.toggle()
            self.editor.setFocus()

        else:

            self.toggle()

            key=self.editor.text()
            self.editor.textChanged.disconnect(self.set)
            self.editor.clear()
            self.editor.textChanged.connect(self.set)
        
            page=self.window.view().currentPage()
            left, top=self.window.view().saveLeftAndTop()

            data={'did': self.window.view().document().id(),
                    'page':page, 
                    'left': left,
                    'top': top,
                    'key':key}
            
            conditions=[{'field':f, 'value':v} for f, v in data.items() if f!='key']
            marks=self.db.getRow(conditions)
            if len(marks)>0: 
                self.db.updateRow({'field':'id','value':marks[0]['id']}, data)
            else:
                self.db.writeRow(data)

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.toggle()

    def setActions(self, clear=False):

        condition={'field':'did', 'value':self.window.view().document().id()}
        self.markActions={}
        for mark in self.db.getRow(condition):
            self.markActions[mark['key']]=dict(mark)

        m_action=QAction()
        m_action.setShortcut(Qt.Key_Escape)
        m_action.setShortcutContext(Qt.WidgetShortcut)
        m_action.triggered.connect(self.toggleTable)
        self.m_table.quit_action=m_action
        self.m_table.addAction(m_action)

        self.m_table.setModel(QuickmarkModel(self))
        self.m_table.sortByColumn(0, Qt.AscendingOrder)
        self.m_table.setColumnWidth(0, 40)
        self.m_table.setColumnWidth(1, self.width()-40)

    def jump(self, key):
        if not self.window.view().__class__.__name__ in ['DocumentView', 'BrowserView']: return

        self.toggleTable()
        if not key in self.markActions: return 
        page=self.markActions[key]['page']
        left=self.markActions[key]['left']
        top=self.markActions[key]['top']

        self.window.view().jumpToPage(page, left, top)
        self.window.view().setFocus()

    def toggleTable(self):

        if not self.m_table.isVisible():

            self.window.activateTabWidget(self.m_table)
            self.setActions()
            self.m_table.setFocus()

        else:

            self.window.deactivateTabWidget(self.m_table)

class CQTableView(QTableView):

    def __init__(self, parent, window):
        super().__init__(window)
        self.m_parent=parent

    def keyPressEvent(self, event):
        self.m_parent.jump(event.text())
