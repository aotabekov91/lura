from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Menu(QListWidget):

    def __init__(self, parent, mapping=None, commando=None):
        super().__init__(parent)
        self.m_parent=parent
        self.setMapping(mapping, commando)
        self.setActions()
        self.hide()

    def setMapping(self, mapping, commando):
        if mapping is not None:
            self.m_mapping=mapping
        else:
            self.m_mapping={getattr(self, f):v for f,v in commando.items()}

    def clearActions(self):
        for action in self.m_actions:
            action.disconnect()

    def setHeight(self, height):
        self.setFixedHeight(height)

    def setWidth(self, width):
        self.setFixedWidth(width)

    def setActions(self, mapping=None):

        if mapping is None: mapping=self.m_mapping

        self.m_actions=[]
        self.m_funcs={}

        self.addActions(mapping)

        m_action=QAction()
        m_action.setShortcut(Qt.Key_Escape)
        m_action.setShortcutContext(Qt.WidgetShortcut)
        self.m_actions+=[m_action]
        m_action.triggered.connect(self.hide)
        self.addAction(m_action)

    def setFunction(self, name, func):
        setattr(self, name, func)

    def addActions(self, mapping):

        for func, key in mapping.items():

            name=func.__name__
            m_action=QAction(f'({key}) {name}')
            if key.isupper(): key=f'Shift+{key}'
            m_action.setShortcut(QKeySequence(key))
            m_action.setShortcutContext(Qt.WidgetShortcut)
            self.m_actions+=[m_action]
            m_action.triggered.connect(func)
            self.addAction(m_action)
            self.addItem(m_action.text())
            self.m_funcs[m_action.text()]=func

    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.setFocus()

    def mouseDoubleClickEvent(self, event):
        item=self.currentItem()
        if item is None: return
        self.m_funcs[item.text()]()
