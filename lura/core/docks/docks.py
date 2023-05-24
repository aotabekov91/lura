from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .dock import Dock

class Docks(QObject):

    keyPressEventOccurred=pyqtSignal(object)

    def __init__(self, window):

        super(Docks, self).__init__(window)

        self.current=None
        self.fullscreen=False

        self.window=window
        self.createDocks()

    def createDocks(self):

        self.window.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.window.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.window.setCorner(Qt.BottomLeftCorner, Qt.BottomDockWidgetArea)
        self.window.setCorner(Qt.BottomRightCorner, Qt.BottomDockWidgetArea)

        locs = {
                'top': Qt.TopDockWidgetArea,
                'bottom': Qt.BottomDockWidgetArea,
                'left': Qt.LeftDockWidgetArea,
                'right': Qt.RightDockWidgetArea,
                }

        for loc, area in locs.items():

            dock = Dock(self, loc)
            dock.setTitleBarWidget(QWidget())

            # if loc=='left':
            #     dock.setAllowedAreas(Qt.LeftDockWidgetArea)
            # elif loc=='right':
            #     dock.setAllowedAreas(Qt.RightDockWidgetArea)
            # elif loc=='bottom':
            #     dock.setAllowedAreas(Qt.BottomDockWidgetArea)

            if loc in ['right', 'left']:
                dock.tab.setFixedWidth(300)
            elif loc in ['top', 'bottom']:
                dock.tab.setFixedHeight(300)

            self.window.addDockWidget(area, dock)
            setattr(self, f'{loc}', dock)

        self.hideAll()

    def focus(self, position): getattr(self, f'{position}').setFocus()

    def resize(self, ratio): 

        if self.current: self.current.resize(ratio)

    def setTab(self, w, loc): 

        w.dock=getattr(self, f'{loc}')
        w.index=w.dock.tab.addWidget(w)

    def toggleFullscreen(self):

        if self.current:
            if not self.fullscreen:
                self.fullscreen=True
                self.current.resize(fullscreen=True)
            else:
                self.fullscreen=False
                self.window.display.show()
                self.current.resize(restore=True)

    def readjustAllDocks(self):

        for position in ['right', 'top', 'bottom', 'left']: 
            dock=getattr(self, f'{position}')
            if dock.isVisible(): 
                if position in ['left', 'right']:
                    tab_size=dock.tab.size()
                    tab_size.setHeight(self.window.display.size().height())
                    height=tab_size.height()
                    if self.bottom.isVisible():
                        height-=self.bottom.size().height()
                    if self.top.isVisible():
                        height-=self.top.size().height()
                    tab_size.setHeight(height)
                    dock.tab.setFixedSize(tab_size)

    def hideAll(self):

        for dock in ['right', 'top', 'bottom', 'left']: getattr(self, f'{dock}').hide()
