from PyQt6 import QtGui

from plug import Plug, Element, Model, Factory

class HelpOutline(Plug):

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
            holder.addAgent('HelpView', self)

    def getOutline(self, model):
        outline=self.m_outlines.get(model, None)
        if outline is None:
            outline=self.loadOutline(model)
            self.m_outlines[model]=outline
        return outline

    def loadOutline(self, model):
        mklass = Factory(QtGui.QStandardItemModel, Model)
        outline = mklass(name="outline")
        converter=model.converter()
        toc=converter.toc_tokens
        root = outline.invisibleRootItem()
        for element in toc:
            self.loadItems(element, root)
        return outline

    def loadItems(self, element, parent):
        title=element['name']
        children=element.pop('children')
        item = QtGui.QStandardItem(title)
        item.setData(element)
        for child in children:
            self.loadItems(child, item)
        parent.appendRow(item)
