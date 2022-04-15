from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Quickmark(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.m_tree=parent.m_view
        self.setup()
        
    def setup(self):

        self.markActions={}

        self.m_table=CQListView(self)

        self.m_widget=QWidget()
        self.m_editor=QLineEdit()
        self.m_label=QLabel('Quickmark')
        self.m_editor.textChanged.connect(lambda: self.get(initial=False))

        layout=QHBoxLayout(self.m_widget)
        layout.addWidget(self.m_label)
        layout.addWidget(self.m_editor)

        self.m_layout=QVBoxLayout(self)
        self.m_layout.addWidget(self.m_table)
        self.m_layout.addWidget(self.m_widget)

        self.m_model=QStandardItemModel()
        self.m_table.setModel(self.m_model)

        self.m_widget.hide()
        self.m_table.hide()
        self.hide()

    def set(self):
        self.show()
        self.m_table.show()
        self.m_table.setFocus()

    def toggle(self):
        if self.isVisible():
            self.hide()
            self.m_tree.setFocus()
        else:
            self.show()
            self.m_edit.setFocus()

    def get(self, initial=True):

        if initial:

            self.show()
            self.m_widget.show()
            self.m_editor.setFocus()

        else:

            self.m_widget.hide()
            self.hide()

            key=self.m_editor.text()
            self.m_editor.textChanged.disconnect()
            self.m_editor.clear()
            self.m_editor.textChanged.connect(lambda: self.get(initial=False))

            self.markActions[key]=self.m_tree.currentItem()
            self.m_model.clear()
            for k, a in self.markActions.items():
                title=a.itemData().title()
                self.m_model.appendRow(QStandardItem(f'{k} - {title}'))

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.toggle()

    def setActions(self, clear=False):

        m_action=QAction()
        m_action.setShortcut(Qt.Key_Escape)
        m_action.setShortcutContext(Qt.WidgetShortcut)
        m_action.triggered.connect(self.toggleTable)
        self.m_table.quit_action=m_action
        self.m_table.addAction(m_action)


    def jump(self, key):
        self.m_table.hide()
        self.hide()
        if key in self.markActions:
            self.m_tree.setCurrentItem(self.markActions[key])

class CQListView(QListView):

    def __init__(self, parent):
        super().__init__()
        self.m_parent=parent

    def keyPressEvent(self, event):
        self.m_parent.jump(event.text())
