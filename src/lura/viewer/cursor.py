from PyQt5.QtCore import QObject, Qt 

class Cursor(QObject):

    def __init__(self, view): 

        super().__init__(view)

        self.start=None

        view.itemMouseMoveOccured.connect(self.on_mouseMove)
        view.itemMousePressOccured.connect(self.on_mousePress)
        view.itemMouseReleaseOccured.connect(self.on_mouseRelease)
        view.itemMouseDoubleClickOccured.connect(self.on_doubleClick)

    def move(self, event, item):

        point=item.mapToPage(event.pos(), unify=False)
        current=item.page().getRow(point)

        if self.start and current:

            selection=item.page().getRows(
                    self.start['box'][0], current['box'][0])
            item.select([selection])

    def on_mousePress(self, view, item, event):

        item.prev_cursor=item.cursor()
        item.setCursor(Qt.IBeamCursor)

        point=item.mapToPage(event.pos(), unify=False)
        self.start=item.page().getRow(point)

    def on_mouseMove(self, view, item, event): self.move(event, item)

    def on_mouseRelease(self, view, item, event): item.setCursor(item.prev_cursor)

    def on_doubleClick(self, view, item, event):

        selection=[]
        point=item.mapToPage(event.pos(), unify=False)
        data=item.page().getRow(point)
        if data: selection+=[data] 
        item.select(selection)
