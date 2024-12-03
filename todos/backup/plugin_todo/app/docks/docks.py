from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .dock import Dock
from ..utils import register
from ..plugin import Configure

class Docks(QObject):

    keyPressEventOccurred=pyqtSignal(object)

    def __init__(self, window):

        super(Docks, self).__init__(window)

        self.prev=None
        self.current=None
        self.fullscreen=False

        self.window=window
        self.window.installEventFilter(self)

        self.createDocks()

        self.configure=Configure(window.app, 'Docks', self,
                                 mode_keys={'command':'d', 'normal':'d'})

    def createDocks(self):

        self.window.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.window.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.window.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.window.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

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

    def eventFilter(self, widget, event):

        if event.type()==QEvent.Resize:
            self.adjustDocks()
            return True
        else:
            return super().eventFilter(widget, event)

    def focus(self, position): getattr(self, f'{position}').setFocus()

    def resize(self, ratio): 

        if self.current: self.current.resize(ratio)

    def setTab(self, w, loc): 

        w.dock=getattr(self, f'{loc}')
        w.index=w.dock.tab.addWidget(w)

    def delTab(self, w): 

        if self.current==w.dock: self.current.hide()
        w.dock.tab.removeWidget(w)

    def toggleFullscreen(self, dock=None):

        if not dock: dock=self.current

        if dock:

            self.setCurrent(dock)

            if not self.fullscreen:
                self.fullscreen=True
                self.current.resize(fullscreen=True)
            else:
                self.fullscreen=False
                self.window.display.show()
                self.current.resize(restore=True)

            # self.current.current().focusGained.emit()
            self.focus(self.current.loc)

    def adjustDocks(self): 

        width=self.window.size().width()

        if self.left.isVisible():
            width-=self.left.size().width()
        if self.right.isVisible():
            width-=self.right.size().width()

        # print(self.window.size().width(), width)

        for position in ['top', 'bottom']: 
            dock=getattr(self, f'{position}')
            if dock.isVisible():
                dock.tab.setFixedWidth(width-5)
                widget=dock.current()
                if widget: 
                    size=dock.tab.size()
                    widget.setFixedSize(size)
                    widget.adjustSize()

    #             area=self.window.corner(Qt.BottomLeftCorner)
    #             dock.tab.setFixedWidth(self.window.display.view.size().width())
    #             # if position in ['top', 'bottom']:
    #             #     tab_size=dock.tab.size()
    #             #     tab_size.setHeight(self.window.display.size().height())
    #             #     height=tab_size.height()
    #             #     if self.bottom.isVisible():
    #             #         height-=self.bottom.size().height()
    #             #     if self.top.isVisible():
    #             #         height-=self.top.size().height()
    #             #     tab_size.setHeight(height)
    #             #     dock.tab.setFixedSize(tab_size)

    def hideAll(self):

        for dock in ['right', 'top', 'bottom', 'left']: getattr(self, f'{dock}').hide()

    def setCurrent(self, dock):

        if self.current!=dock:
            self.prev=self.current
            self.current=dock

    def zoom(self, kind='in', digit=1): 

        if self.current:

            if kind=='in': 
                factor=1.1**digit
            else:
                factor=.9**digit
            self.current.resize(factor=factor)
            self.current.setFocus()

    @register('h', modes=['command', 'normal'])
    def focusLeftDock(self): 

        self.window.app.modes.command.delisten_wanted=None
        self.focus('left')

    @register('l', modes=['command', 'normal'])
    def focusRightDock(self): 

        self.window.app.modes.command.delisten_wanted=None
        self.focus('right')

    @register('k', modes=['command', 'normal'])
    def focusTopDock(self): 

        self.window.app.modes.command.delisten_wanted=None
        self.focus('top')

    @register('j', modes=['command', 'normal'])
    def focusBottomDock(self): 

        self.window.app.modes.command.delisten_wanted=None
        self.focus('bottom') 

    @register('f', modes=['command', 'normal'])
    def toggleDockFullscreen(self): 

        self.window.app.modes.command.delisten_wanted=None
        self.toggleFullscreen()

    @register('zi', modes=['command', 'normal'])
    def zoomInDock(self, digit=1): 

        self.window.app.modes.command.delisten_wanted=None
        self.zoom('in', digit)

    @register('zo', modes=['command', 'normal'])
    def zoomOutDock(self, digit=1): 

        self.window.app.modes.command.delisten_wanted=None
        self.zoom('out', digit)
