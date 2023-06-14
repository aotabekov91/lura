from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Cursor(QObject):

    def __init__(self, view): 

        super().__init__(view)

        self.start=None

        view.mouseMoveEventOccured.connect(self.on_mouseMove)
        view.mousePressEventOccured.connect(self.on_mousePress)
        view.mouseReleaseEventOccured.connect(self.on_mouseRelease)
        view.mouseDoubleClickOccured.connect(self.on_doubleClick)

    def move(self, event, item):

        point=item.mapToPage(event.pos(), unify=False)
        current=item.page().getRow(point)

        if self.start and current:

            selection=item.page().getRows(
                    self.start['box'][0], current['box'][0])
            item.setSelection([selection])

    def on_mousePress(self, event, item):

        item.prev_cursor=item.cursor()
        item.setCursor(Qt.IBeamCursor)

        point=item.mapToPage(event.pos(), unify=False)
        self.start=item.page().getRow(point)

    def on_mouseMove(self, event, item): self.move(event, item)

    def on_mouseRelease(self, event, item): item.setCursor(item.prev_cursor)

    def on_doubleClick(self, event, item):

        selection=[]
        point=item.mapToPage(event.pos(), unify=False)
        data=item.page().getRow(point)
        if data: selection+=[data] 
        item.setSelection(selection)
