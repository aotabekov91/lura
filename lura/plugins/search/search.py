#!/usr/bin/python3

import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Search(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings=settings
        self.name = 'textSearch'
        self.globalKeys= {
                '/': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.setup()

    def setup(self):

        self.shortcuts={v:k for k, v in self.s_settings['shortcuts'].items()}

        self.window.view.pageHasBeenJustPainted.connect(self.paintMatches)

        self.activated=False
        self.currentMatch=None
        self.matches=None

        self.editor=QLineEdit()
        self.editor.returnPressed.connect(self.search)
        label=QLabel('Search')
        self.widget=QWidget()
        layout=QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.editor)
        self.widget.setLayout(layout)

    def toggle(self):

        raise
        if not self.activated:

            self.window.activateStatusBar(self.widget)
            self.editor.setFocus()
            self.activated=True

        else:

            self.window.deactivateStatusBar(self.widget)
            self.activated=False


    def paintMatches(self, painter, options, widget, pageItem):
        if self.activated:
            if self.currentMatch is not None:
                painter.setPen(QPen(Qt.red, 0.0))
                painter.drawRect(self.currentMatch)


    def getMatches(self, text):
        found=[]
        for pageItem in self.window.view.m_pageItems:
            matches=pageItem.search(text)
            for match in matches:
                match=pageItem.mapToItem(match)[0]
                found+=[(pageItem, match)]
        return found

    def search(self):
        
        text=self.editor.text()
        if text == '': return

        matches=self.getMatches(text)

        if len(matches) == 0: 
            self.toggle()
            return 

        self.show()
        self.setFocus()

        self.matches=matches
        self.currentIndex=-1
        self.jumpToNext()
        
    def keyPressEvent(self, event):
        key=event.text()

        if key in self.shortcuts:
            func=getattr(self, self.shortcuts[key])
            func()

        elif event.key()==Qt.Key_Escape:
            self.toggle()


    def jumpToNext(self):

        if self.matches is not None:

            self.currentIndex+=1
            if self.currentIndex>=len(self.matches):
                self.currentIndex=0

            pageItem=self.matches[self.currentIndex][0]
            self.currentMatch=self.matches[self.currentIndex][1]
            self.window.view.jumpToPage(pageItem.m_index)

    def jumpToPrevious(self):

        if self.matches is not None:

            self.currentIndex-=1
            if self.currentIndex<0:
                self.currentIndex=len(self.matches)-1

            pageItem=self.matches[self.currentIndex][0]
            self.currentMatch=self.matches[self.currentIndex][1]
            self.window.view.jumpToPage(pageItem.m_index)

