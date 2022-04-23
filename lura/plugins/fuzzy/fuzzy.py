from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core.miscel import *

class Fuzzy(MapTree):

    fuzzySelected=pyqtSignal(object, object)

    def __init__(self, parent, settings):

        super().__init__(parent, parent)
        self.window = parent
        self.s_settings=settings
        self.location = 'bottom' 
        self.name = 'fuzzy'

        self.setup()

    def setup(self):

        self.callFunc=None

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.window.setTabLocation(self, self.location, self.name)

    def activate(self, callFunc, data, names=None):
        self.callFunc=callFunc
        if names is None: names = data

        model=ItemModel()
        for r, i in enumerate(names):
            item=Item('container', None, self.window, i)
            item.m_data=data[r]
            model.appendRow(item)

        self.setModel(model)
        if len(names)>0:
            index=self.model().invisibleRootItem().child(0).index()
            self.setCurrentIndex(index)
        self.window.activateTabWidget(self)
        self.setFocus()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Return:
            if self.callFunc is not None:
                item=self.currentItem()
                self.callFunc(item)
                self.callFunc=None
            self.window.deactivateTabWidget(self)
        else:
            super().keyPressEvent(event)
