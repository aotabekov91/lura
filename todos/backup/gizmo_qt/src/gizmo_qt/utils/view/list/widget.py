from PyQt6 import QtCore

from gizmo_qt import vimo, widget
from gizmo_qt.mixin import view
from gizmo.utils import tag


class ElementListView(
    view.Hint,
    view.Input,
    view.WidgetGo,
    view.InputHint,
    view.ListWidgetInput,
    view.ListWidgetFilter,
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
            self.cleanUp()
            super().setModel(model)
            elems = model.elements()
            for i, e in elems.items():
                if self.include:
                    for (
                        i,
                        j,
                    ) in self.include.items():
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
        m = self.m_model
        if not m:
            return
        ci = self.currentItem()
        for i in range(m.rowCount()):
            r = m.index(i, 0)
            e = m.itemFromIndex(r).element()
            l = e.listItem()
            l.setHidden(True)
            l.m_current_idx = ci == l

    def getWidgetMap(self, element):
        return self.widget_map

    def addElement(self, e):
        wmap = self.getWidgetMap(e)
        i = self.list_item_class()
        i.setElement(e)
        w = self.widget_class(
            item=i,
            view=self,
            element=e,
            wmap=wmap,
        )
        self.addItem(i)
        self.setItemWidget(i, w)
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

    def selectElement(self, e):
        for j in range(self.count()):
            i = self.item(j)
            if i.element() == e:
                return self.setCurrentItem(i)

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
        super().octivate(recursive=True)

    def sizeHint(self):
        h = 0
        hint = super().sizeHint()
        n = self.m_model.count()
        for i in range(n):
            h += self.sizeHintForRow(i)
        hint.setHeight(h)
        return hint
