import shlex
import argparse

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Filter(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.m_parent=parent
        self.m_tree=parent.m_view
        self.setup()

    def setup(self):


        self.m_label=QLabel('Filter')
        self.m_edit=CQLineEdit()
        layout=QHBoxLayout(self)
        layout.addWidget(self.m_label)
        layout.addWidget(self.m_edit)

        self.m_edit.returnPressed.connect(self.act)
        self.createParser()

        self.hide()

    def createParser(self):
        self.m_parser=argparse.ArgumentParser()
        self.m_parser.add_argument('-t,', '--tag')
        self.m_parser.add_argument('-f,', '--function')
        self.m_parser.add_argument('-d,', '--date')
        self.m_parser.add_argument('-D,', '--Date')
        self.m_parser.add_argument('--title')

    def act(self):
        self.toggle()
        text=self.m_edit.text()
        if text=='': return
        conditions= self.m_parser.parse_known_args(shlex.split(text))[0]
        self.resetByConditions(conditions)

    def resetByConditions(self, conditions):
        parent=self.m_tree.currentItem()
        if parent is None: self.m_tree.model().invisibleRootItem()

        for index in range(parent.rowCount()):
            child=parent.child(index)

            if conditions.tag:
                print(conditions.tag)
                print(child.itemData().tags())
                if not conditions.tag in child.itemData().tags():
                    self.m_tree.filterOut(child)

            if conditions.title:
                if not conditions.title in child.itemData().title().lower():
                    self.m_tree.filterOut(child)

        self.m_tree.updatePosition()
        self.m_tree.setFocus()

    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.m_tree.resetFilter()
            self.show()
            self.m_edit.setFocus()

class CQLineEdit(QLineEdit):

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.parent().setFocus()
            self.parent().toggle()
        else:
            super().keyPressEvent(event)

