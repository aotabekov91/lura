from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import watch, Configure

class Docks(QWidget):

    keyPressEventOccurred=pyqtSignal(object)

    def __init__(self, window):
        super().__init__(window)
        self.window=window
        self.state={}
        self.m_widget=None
        self.createDocks()

    def createDocks(self):
        locs = {
                'left': Qt.LeftDockWidgetArea,
                'bottom': Qt.BottomDockWidgetArea,
                'top': Qt.TopDockWidgetArea,
                'right': Qt.RightDockWidgetArea,
                }
        for name, loc in locs.items():
            dockWidget = QDockWidget(self.window)
            stackWidget= QStackedWidget(self.window)
            if name=='right':
                stackWidget.setFixedWidth(300)
            elif name=='left':
                stackWidget.setFixedWidth(300)
            dockWidget.setWidget(stackWidget)
            self.window.addDockWidget(loc, dockWidget)
            setattr(self, '{}Stack'.format(name), stackWidget)
            setattr(self, '{}Dock'.format(name), dockWidget)

        self.window.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.window.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.window.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)
        self.window.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.hideAllDocks()

    def setActions(self):
        self.configuration=Configure(self.window.app, 'Docks', self)

    @watch(widget='window', context=Qt.WindowShortcut)
    def toggle(self):
        if not self.setFocus():
            statusbar=self.window.statusBar()
            statusbar.setDetailInfo(self.configuration.name)
            statusbar.show()
            self.show()
            self.setFocus()
        else:
            self.deactivate()

    @watch(widget='own', context=Qt.WidgetShortcut)
    def toggleFullSize(self):
        self.deactivate()
        w=self.currentWidget()
        if self.window.display.isVisible():
            self.hideAllDocks(exclude=w.m_d)
            self.window.display.hide()
            self.resize(fullscreen=True)
            w.setFocus()
        else:
            if hasattr(w, 'm_prev_size'):
                self.resize(size=w.m_prev_size)
            self.window.display.show()

    def deactivate(self):
        statusbar=self.window.statusBar()
        statusbar.setDetailInfo('')
        statusbar.hide()
        self.hide()
        self.window.display.focusCurrentView()

    @watch(widget='own', context=Qt.WidgetShortcut)
    def left(self):
        self.deactivate()
        self.focus('left')

    @watch(widget='own', context=Qt.WidgetShortcut)
    def top(self):
        self.deactivate()
        self.focus('top')

    @watch(widget='own', context=Qt.WidgetShortcut)
    def bottom(self):
        self.deactivate()
        self.focus('bottom')

    @watch(widget='own', context=Qt.WidgetShortcut)
    def right(self):
        self.deactivate()
        self.focus('right')

    @watch(widget='own', context=Qt.WidgetShortcut)
    def increaseSize(self):
        self.resize(1.1)

    @watch(widget='own', context=Qt.WidgetShortcut)
    def decreaseSize(self):
        self.resize(0.9)

    def focus(self, position):
        dock=getattr(self, f'{position}Dock')
        stack=getattr(self, f'{position}Stack')
        con=dock.isVisible() and dock in self.state and len(self.state[dock])>0
        if con:
            widget=self.state[dock][-1]
            self.setCurrentWidget(widget)
            widget.setFocus()

    def setCurrentWidget(self, widget):
        self.m_widget=widget

    def currentWidget(self):
        return self.m_widget

    def deactivateTabWidget(self, w):
        self.state[w.m_d].pop(self.state[w.m_d].index(w))
        if len(self.state[w.m_d])==0:
            w.m_d.hide()
            w.m_s.hide()
            self.setCurrentWidget(None)
        else:
            oldWidget=self.state[w.m_d][-1]
            w.m_s.setCurrentIndex(oldWidget.m_i)
            self.setCurrentWidget(oldWidget)

    def saveState(self, widget):
        if not widget.m_d in self.state:
            self.state[widget.m_d]=[]
        self.state[widget.m_d]+=[widget]

    def activateTabWidget(self, widget):
        self.saveState(widget)
        widget.m_d.setTitleBarWidget(widget.m_l)
        widget.m_s.setCurrentIndex(widget.m_i)
        widget.m_d.show()
        widget.m_s.show()
        widget.show()
        widget.setFixedSize(widget.m_s.size())
        widget.adjustSize()
        widget.setFocus()
        self.setCurrentWidget(widget)

    def setTabLocation(self, widget, location, title):
        widget.m_loc=location
        widget.m_l=QLabel(title.title())
        widget.m_s=getattr(self, '{}Stack'.format(location))
        widget.m_d=getattr(self, '{}Dock'.format(location))
        widget.m_i=widget.m_s.addWidget(widget)

    def hideAllDocks(self, exclude=None):
        for dock in ['right', 'top', 'bottom', 'left']:
            dockWidget=getattr(self, f'{dock}Dock')
            if dockWidget!=exclude: 
                dockWidget.hide()

    def resize(self, factor=1.2, fullscreen=False, size=None):
        widget=self.currentWidget()
        if widget:
            s=widget.m_s.size()
            widget.m_prev_size=s
            if size:
                widget.m_s.setFixedSize(size)
            else:
                w, h=s.width(), s.height()
                if not fullscreen:
                    if widget.m_loc in ['left', 'right']:
                        widget.m_s.setFixedSize(round(w*factor), h)
                    else:
                        widget.m_s.setFixedSize(w, round(h*factor))
                else:
                    widget.m_s.setFixedSize(self.window.size())
