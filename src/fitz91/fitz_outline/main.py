import fitz
from PyQt6 import QtCore, QtGui

from plug import Plug, Element, Model, Factory

class FitzOutline(Plug):

    def setup(self):
        super().setup()
        self.m_outlines={}
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('Outline')
        if holder:
            holder.addAgent('FitzView', self)

    def getOutline(self, model):
        outline=self.m_outlines.get(model, None)
        if outline is None:
            outline=self.loadOutline(model)
            self.m_outlines[model]=outline
        return outline

    def loadOutline(self, model):
        eklass = Factory(
                QtGui.QStandardItem, Element)
        mklass = Factory(
                QtGui.QStandardItemModel, Model)
        outline = mklass(
            name="outline", element_class=eklass)
        data=model.modelData()
        raw_outline = data.outline
        root = outline.invisibleRootItem()
        try:
            self.loadItems(raw_outline, root, data)
        except:
            pass
        return outline

    def loadItems(self, outline, root, data):
        if not outline:
            return
        title = outline.title
        item = QtGui.QStandardItem(title)
        item.setFlags(
                QtCore.Qt.ItemFlag.ItemIsEnabled 
                | QtCore.Qt.ItemFlag.ItemIsSelectable)
        destination=outline.destination(data)
        if destination!= fitz.LINK_NONE:
            page = destination.page + 1
            top_right=destination.lt.abs_unit
            x=top_right.x
            y=top_right.y
            data={'xrange': [page], 'x': x, 'y': y}
            item.setData(data)
            clone_item = item.clone()
            clone_item.setText(str(page))
            clone_item.setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignRight)
            root.appendRow([item, clone_item])
        else:
            root.appendRow(item)
        if outline.next != 0:
            self.loadItems(outline.next, root, data)
        if outline.down != 0:
            self.loadItems(outline.down, item, data)
