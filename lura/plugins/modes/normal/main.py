from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Mode

class Normal(Mode):

    def __init__(self, app):

        super(Normal, self).__init__(app, 
                                     name='Normal',
                                     listen_leader='n', 
                                     listen_widget=app.window,
                                     hide_bar_on_execution=False,
                                     show_statusbar=False,
                                    )
        self.listen()

    def delisten(self):
        super().delisten()
        self.listening=True

    def mark(self): self.app.manager.quickmark.mark()

    def gotoMark(self): self.app.manager.quickmark.goto()

    def gotoPage(self, digit=1):

        self.app.window.display.view.jumpToPage(digit)

    def gotoEnd(self):

        document=self.app.window.display.view.document()
        self.app.window.display.view.jumpToPage(document.numberOfPages())

    def gotoBegin(self):

        self.app.window.display.view.jumpToPage(1)

    def nextPage(self, digit=1): 

        for d in range(digit): self.app.window.display.view.nextPage()
    
    def prevPage(self, digit=1): 

        for d in range(digit): self.app.window.display.view.prevPage()

    def pageUp(self, digit=1): 

        for d in range(digit): self.app.window.display.view.pageUp()

    def pageDown(self, digit=1): 

        for d in range(digit): self.app.window.display.view.pageDown()

    def incrementUp(self, digit=1): 

        for d in range(digit): self.app.window.display.view.incrementUp()

    def incrementDown(self, digit=1): 

        for d in range(digit): self.app.window.display.view.incrementDown()

    def incrementLeft(self, digit=1): 

        for d in range(digit): self.app.window.display.view.incrementLeft()

    def incrementRight(self, digit=1): 

        for d in range(digit): self.app.window.display.view.incrementRight()

    def zoomIn(self, digit=1): 
        
        for d in range(digit): self.app.window.display.view.zoomIn()

    def zoomOut(self, digit=1): 
        
        for d in range(digit): self.app.window.display.view.zoomOut()

    def close(self): self.app.window.close()

    def saveDocument(self): self.app.window.display.view.save()

    def updateView(self): self.app.window.display.view.updateAll()

    def toggleStatusbar(self): 

        self.show_statusbar=not self.show_statusbar
        if self.show_statusbar:
            self.hide_bar_on_execution=False
            self.app.window.bar.show()
        else:
            self.app.window.bar.hide()

    def fitToPageWidth(self): self.app.window.display.view.fitToPageWidth()

    def fitToPageHeight(self): self.app.window.display.view.fitToPageHeight()

    def toggleContinuousMode(self): self.app.window.display.view.toggleContinuousMode()

    def decreaseDockSize(self): self.app.window.docks.resize(0.9)

    def increaseDockSize(self): self.app.window.docks.resize(1.1)

    def toggleDockFullscreen(self): self.app.window.docks.toggleFullscreen()
        # self.adjustSize()
