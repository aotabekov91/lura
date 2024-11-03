from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Dock(QDockWidget):

    def __init__(self, docks, loc):

        super().__init__(docks.window)

        self.loc=loc
        self.widgets=[]
        self.docks=docks

        self.setUI()
        self.createTab()

    def setUI(self):

        self.style_sheet = '''
            QWidget{
                color: white;
                border-color: transparent; 
                background-color: transparent; 
                border-width: 0px;
                padding: 0px 0px 0px 0px;
                }
                '''
        self.setStyleSheet(self.style_sheet)

        self.setContentsMargins(0, 0, 0, 0)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def createTab(self):

        self.tab = QStackedWidget(self)
        self.setWidget(self.tab)

    def setFocus(self, widget=None):

        super().setFocus()

        if not widget: widget=self.current()
        if widget:
            self.docks.setCurrent(self)
            self.show()
            self.tab.setCurrentIndex(widget.index)
            self.tab.show()
            widget.setFocus()
            widget.focusGained.emit()

    def activate(self, widget): 

        if not self.widgets or self.widgets[-1]!=widget: self.widgets+=[widget]

        self.setFocus(widget)

        widget.show()

        widget.setFixedSize(self.tab.size())
        widget.prev_size=self.tab.size()
        widget.adjustSize()

        widget.dock.show()
        widget.dock.tab.show()
        widget.setFocus()
        widget.focusGained.emit()

        self.docks.adjustDocks()

    def deactivate(self, widget, restore=False):

        if widget in self.widgets: self.widgets.pop(self.widgets.index(widget))

        if restore and self.widgets:
            prev=self.widgets[-1]
            widget.dock.tab.setCurrentIndex(prev.index)
            self.activate(prev)
        else:
            self.hide()
            self.docks.adjustDocks()
            self.parent().display.setFocus()

        self.docks.adjustDocks()

    def event(self, event):

        if event.type()==QEvent.Enter:
            current=self.current()
            if current: current.focusGained.emit()
        if event.type()==QEvent.Leave:
            current=self.current()
            if current: current.focusLost.emit()
        return super().event(event)

    def current(self):

        if self.widgets: return self.widgets[-1]

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.tab.installEventFilter(listener)

    def resize(self, factor=1.2, widget=None, fullscreen=False, restore=False):

        if not widget: widget=self.current()

        if widget:
            if fullscreen:
                widget.prev_size=widget.dock.tab.size()
                self.parent().display.hide()
                widget.dock.tab.setFixedSize(self.parent().size())
                widget.setFixedSize(self.parent().size())
            elif restore:
                self.parent().display.show()
                widget.dock.tab.setFixedSize(widget.prev_size)
                widget.setFixedSize(widget.prev_size)
            else:
                w, h=widget.prev_size.width(), widget.prev_size.height()
                if self.loc in ['left', 'right']:
                    size=QSize(round(w*factor), h)
                else:
                    size=QSize(w, round(h*factor))
                widget.dock.tab.setFixedSize(size)
                widget.setFixedSize(size)
                widget.prev_size=widget.dock.tab.size()
