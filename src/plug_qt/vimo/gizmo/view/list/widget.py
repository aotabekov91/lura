from PyQt6 import QtCore

from plug import tag
from plug_qt import vimo, widget
from plug_qt.vimo.mixin import view


class ListWidgetView(
    view.WidgetGo,
    vimo.View,
    widget.ListWidget,
):
    include = {}
    exclude = {}
    widget_map = {}
    widget_class = widget.TableWidget
    list_item_class = widget.ListWidgetItem
    widgetDataChanged = QtCore.pyqtSignal(object)

    def updateKlass(self):
        super().updateKlass()
        inc = self.m_kwargs.get("include", self.include)
        self.include = inc.copy()
        exc = self.m_kwargs.get("exclude", self.exclude)
        self.exclude = exc.copy()
        wm = self.m_kwargs.get(
            "widget_map", self.widget_map
        )
        self.widget_map = wm.copy()

    def setModel(self, model=None, **kwargs):
        if id(self.m_model) != id(model):
            self.reconnectModel("disconnect")
            # self.cleanUp() #todo
            # self.clear()
            super().setModel(model)
            elems = model.elements()
            for i, e in elems.items():
                if self.include:
                    for i, j in self.include.items():
                        d = e.data()
                        v = d.get(i)
                        if not v in j:
                            break
                        self.addElement(e)
                else:
                    self.addElement(e)
            self.reconnectModel()

    def cleanUp(self):
        super().clear()
        model = self.m_model
        if model:
            current_item = self.currentItem()
            # for i in range(m.rowCount()):
            for i in range(model.count()):
                idx = model.index(i, 0)
                item = model.itemFromIndex(idx)
                element=item.element()
                list_item = element.listItem()
                list_item.setHidden(True)
                if current_item == list_item:
                    list_item.m_current_idx = True 

    def getWidgetMap(self, element):
        return self.widget_map

    def addElement(self, element):
        wmap = self.getWidgetMap(element)
        list_item = self.list_item_class()
        list_item.setElement(element)
        widget = self.widget_class(
            item=list_item,
            view=self,
            element=element,
            wmap=wmap,
        )
        self.addItem(list_item)
        self.setItemWidget(list_item, widget)
        self.resized.emit(self)

    def updateElement(self, e):
        for i in range(self.count()):
            i = self.item(i)
            if i.element() == e:
                w = self.itemWidget(i)
                w.updateData()

    def removeElement(self, e):
        for i in range(self.count()):
            item = self.item(i)
            if item.element() == e:
                return self.takeItem(i)

    def selectElement(self, element):
        for row in range(self.count()):
            item = self.item(row)
            if item.element() == element:
                return self.setCurrentItem(item)

    def reconnectModel(self, kind="connect"):
        m = self.m_model
        if not m:
            return
        if kind == "connect":
            m.elementAdded.connect(self.addElement)
            m.elementRemoved.connect(self.removeElement)
            m.elementWanted.connect(self.selectElement)
        else:
            m.elementAdded.disconnect(self.addElement)
            m.elementRemoved.disconnect(self.removeElement)
            m.elementWanted.disconnect(self.selectElement)

    @tag("<escape>(normal)[^]")
    def octivateMe(self):
        super().octivate(recursive_octivate=True)

    def sizeHint(self):
        height = 0
        hint = super().sizeHint()
        if self.m_model:
            count = self.m_model.count()
            for row in range(count):
                height += self.sizeHintForRow(row)
            hint.setHeight(height)
        return hint
